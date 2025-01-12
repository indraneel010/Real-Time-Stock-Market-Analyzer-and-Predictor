import unittest
import requests

class TestApiPredict(unittest.TestCase):

    BASE_URL = "http://127.0.0.1:5000"

    def setUp(self):
        # Mock raw stock data for testing
        self.mock_data = [
            {"time": "2025-01-11T10:00:00", "open": 100.5, "close": 102.3},
            {"time": "2025-01-11T11:00:00", "open": 102.3, "close": 103.8},
            {"time": "2025-01-11T12:00:00", "open": 103.8, "close": 101.2},
            {"time": "2025-01-11T13:00:00", "open": 101.2, "close": 100.0},
        ]

    def test_predict_endpoint(self):
        """
        Test the `/api/predict` endpoint for correct functionality.
        """
        response = requests.post(f"{self.BASE_URL}/api/predict", json=self.mock_data)
        self.assertEqual(response.status_code, 200)

        # Check response format and content
        data = response.json()
        self.assertIn("predictions", data)
        self.assertEqual(len(data["predictions"]), len(self.mock_data))

        # Ensure predictions are -1 or 1 (mock logic)
        for pred in data["predictions"]:
            self.assertIn(pred, [-1, 1])

if __name__ == "__main__":
    unittest.main()
