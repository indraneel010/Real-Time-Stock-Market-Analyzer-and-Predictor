import unittest
from utils.data_processor import clean_stock_data, prepare_features

class TestDataProcessor(unittest.TestCase):

    def setUp(self):
        # Mock raw stock data
        self.raw_data = [
            {"time": "2025-01-11T10:00:00", "open": 100.5, "close": 102.3},
            {"time": "2025-01-11T11:00:00", "open": 102.3, "close": 103.8},
            {"time": "2025-01-11T12:00:00", "open": 103.8, "close": 101.2},
            {"time": "2025-01-11T13:00:00", "open": 101.2, "close": 100.0},
        ]

    def test_clean_stock_data(self):
        # Test data cleaning
        cleaned_data = clean_stock_data(self.raw_data)
        self.assertEqual(len(cleaned_data), 4)  # Ensure no rows were dropped
        self.assertIn("price_change", cleaned_data.columns)  # Ensure new feature is added
        self.assertTrue(all(cleaned_data["price_change"] == [1.8, 1.5, -2.6, -1.2]))

    def test_prepare_features(self):
        # Test feature preparation
        cleaned_data = clean_stock_data(self.raw_data)
        features = prepare_features(cleaned_data)
        self.assertEqual(features.shape[1], 1)  # Ensure only one feature column
        self.assertIn("price_change", features.columns)  # Ensure feature exists
        self.assertAlmostEqual(features["price_change"].mean(), 0, places=5)  # Normalization check

if __name__ == "__main__":
    unittest.main()
