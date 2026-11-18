from functools import lru_cache

from flask import Flask, jsonify, render_template, request

from src.forcastingproject.pipeline.prediction_pipeline import PredictionPipeline


app = Flask(__name__)

OPTIONAL_FIELDS = (
    "CompetitionDistance",
    "CompetitionOpenSinceMonth",
    "CompetitionOpenSinceYear",
    "Promo2SinceWeek",
    "Promo2SinceYear",
    "PromoInterval",
)
UNAVAILABLE_MESSAGE = "Forecasts are unavailable because the trained artifacts are missing."


@lru_cache(maxsize=1)
def get_prediction_pipeline() -> PredictionPipeline:
    return PredictionPipeline()


@app.get("/")
def index():
    return render_template("index.html", values={})


@app.get("/health")
def health():
    try:
        get_prediction_pipeline()
    except FileNotFoundError as exc:
        app.logger.warning("%s", exc)
        return jsonify(status="unavailable"), 503

    return jsonify(status="ready")


@app.post("/predict")
def predict():
    values = request.form.to_dict()
    payload = {
        field: value for field, value in values.items()
        if field not in OPTIONAL_FIELDS or value.strip()
    }

    try:
        sales = get_prediction_pipeline().predict(payload)
    except (TypeError, ValueError) as exc:
        return render_template("index.html", values=values, error=str(exc)), 400
    except FileNotFoundError as exc:
        app.logger.warning("%s", exc)
        return render_template("index.html", values=values, error=UNAVAILABLE_MESSAGE), 503

    return render_template("index.html", values=values, sales=sales)


@app.post("/api/predict")
def predict_api():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Send a JSON object with the store and date fields."), 400

    try:
        sales = get_prediction_pipeline().predict(payload)
    except (TypeError, ValueError) as exc:
        return jsonify(error=str(exc)), 400
    except FileNotFoundError as exc:
        app.logger.warning("%s", exc)
        return jsonify(error=UNAVAILABLE_MESSAGE), 503

    return jsonify(sales=sales)


if __name__ == "__main__":
    app.run()
