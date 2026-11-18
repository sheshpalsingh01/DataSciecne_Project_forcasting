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
