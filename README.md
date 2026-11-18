# DataSciecne_Project_forcasting

Run `python main.py` from the project directory to ingest, validate, and transform the sales data, train the Random Forest, and evaluate it with MLflow tracking on DagsHub. Set the tracking credentials below before running the full pipeline.

## Model evaluation

With the trained model and transformed test data in `artifacts/`, run Stage 05 by itself.

```bash
python -m src.forcastingproject.pipeline.model_evaluation_pipeline --local-only
```

The evaluation writes RMSE, MAE, and R² to `artifacts/model_evaluation/metrics.json`.

For DagsHub tracking, set `MLFLOW_TRACKING_USERNAME` to your DagsHub username and `MLFLOW_TRACKING_PASSWORD` to an access token with write access to the repository. Use the same Python environment for training and evaluation.

```bash
python -m src.forcastingproject.pipeline.model_evaluation_pipeline
```

The command uses the tracking URI in `config/config.yaml`. Set `MLFLOW_TRACKING_URI` to use a different tracking server. The run logs the fitted model's parameters, metrics, and model signature and registers the model as `sales-forecasting`.

## DVC pipeline and storage

Run the pipeline from the project directory with the environment from `requirements.txt` active. On a fresh checkout, configure DagsHub credentials and run `dvc pull` first to retrieve the source data and cached artifacts.

```bash
dvc dag
dvc repro
dvc metrics show
dvc push
```

DVC tracks the source dataset through `data.dvc` and records the five pipeline stages in `dvc.lock`. Editing the `model_trainer` settings in `params.yaml` starts reproduction at model training. DVC runs evaluation with `--local-only` so cache operations do not create MLflow runs. Use the standalone tracking command above to publish a run.

The default remote is the project's DagsHub DVC storage. Configure `access_key_id` and `secret_access_key` for the `dagshub` remote in the Git-ignored `.dvc/config.local` using `dvc remote modify --local` or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in your shell environment. Keep credentials in local configuration.

## Predict sales for one store

Use the preprocessor and model artifacts produced by Stages 03 and 04. If they are missing, fetch them with `dvc pull` or build them with `dvc repro model_training`.

```bash
python -m src.forcastingproject.pipeline.prediction_pipeline \
  '{"Store":1,"Date":"2015-07-31","Open":1,"Promo":1,"StateHoliday":"0","SchoolHoliday":1,"StoreType":"c","Assortment":"a","Promo2":0}'
```

The command prints one predicted sales value. Provide competition and recurring promotion details when known. The optional fields are `CompetitionDistance`, `CompetitionOpenSinceMonth`, `CompetitionOpenSinceYear`, `Promo2SinceWeek`, `Promo2SinceYear`, and `PromoInterval`. The pipeline derives calendar features from `Date` and applies the fitted preprocessor. In Python, create a `PredictionPipeline()` once and pass a dictionary or a `CustomData` instance to its `predict()` method for each request.

## Run the forecast web app

With the model artifacts available, run `flask --app app run` from the project directory and open `http://127.0.0.1:5000/`. The web form and JSON API accept the same fields as Stage 07.

```bash
curl http://127.0.0.1:5000/api/predict \
  -H 'Content-Type: application/json' \
  -d '{"Store":1,"Date":"2015-07-31","Open":1,"Promo":1,"StateHoliday":"0","SchoolHoliday":1,"StoreType":"c","Assortment":"a","Promo2":0}'
```

A successful response contains `sales` as a number. Invalid requests return HTTP 400 with an error message. Missing model artifacts return HTTP 503.
