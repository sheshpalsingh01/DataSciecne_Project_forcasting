import unittest
from unittest.mock import patch

from app import app


class ForecastAppTest(unittest.TestCase):
    payload = {
        "Store": 1,
        "Date": "2015-07-31",
        "Open": 1,
        "Promo": 1,
        "StateHoliday": "0",
        "SchoolHoliday": 1,
        "StoreType": "c",
        "Assortment": "a",
        "Promo2": 0,
    }

    def setUp(self):
        self.client = app.test_client()

    def test_home_renders_forecast_form(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Predict sales", response.data)

    @patch("app.get_prediction_pipeline")
    def test_form_and_api_return_the_same_prediction(self, get_pipeline):
        pipeline = get_pipeline.return_value
        pipeline.predict.return_value = 7752.08

        api_response = self.client.post("/api/predict", json=self.payload)
        self.assertEqual(api_response.status_code, 200)
        self.assertEqual(api_response.json, {"sales": 7752.08})
        pipeline.predict.assert_called_once_with(self.payload)

        form_response = self.client.post("/predict", data=dict(self.payload, CompetitionDistance=""))
        self.assertEqual(form_response.status_code, 200)
        self.assertIn(b"7,752.08", form_response.data)
        pipeline.predict.assert_called_with({key: str(value) for key, value in self.payload.items()})

    @patch("app.get_prediction_pipeline")
    def test_invalid_payloads_return_bad_request(self, get_pipeline):
        self.assertEqual(self.client.post("/api/predict", json=[]).status_code, 400)
        get_pipeline.assert_not_called()

        get_pipeline.return_value.predict.side_effect = ValueError("Invalid date")
        self.assertEqual(self.client.post("/api/predict", json=self.payload).status_code, 400)
        self.assertEqual(self.client.post("/predict", data=self.payload).status_code, 400)

    @patch("app.get_prediction_pipeline")
    def test_readiness_checks_model_availability(self, get_pipeline):
        self.assertEqual(self.client.get("/health").json, {"status": "ready"})

        get_pipeline.side_effect = FileNotFoundError("model.joblib")
        self.assertEqual(self.client.get("/health").status_code, 503)
        self.assertEqual(self.client.post("/api/predict", json=self.payload).status_code, 503)
        self.assertEqual(self.client.post("/predict", data=self.payload).status_code, 503)
