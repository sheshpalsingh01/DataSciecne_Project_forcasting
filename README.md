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
