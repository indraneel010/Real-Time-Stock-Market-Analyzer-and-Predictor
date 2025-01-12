from flask import Flask, jsonify, request
from utils.logger import setup_logger
from utils.stock_fetcher import fetch_stock_data_mock
from utils.data_processor import clean_stock_data, prepare_features
import os

# Initialize Flask app
app = Flask(__name__)

# Set up logger for the application
logger = setup_logger("app", log_file="logs/app.log")

# Root endpoint
@app.route("/")
def home():
    """
    Health check endpoint to verify the server is running.
    """
    logger.info("Health check endpoint accessed.")
    return jsonify({"status": "Server is running!"}), 200

# Endpoint to fetch stock data
@app.route("/api/stock", methods=["GET"])
def get_stock_data():
    """
    Fetch stock data using the stock fetcher utility.
    """
    try:
        # For now, we use the mock stock data function
        stock_data = fetch_stock_data_mock()
        logger.info(f"Fetched stock data: {stock_data}")
        return jsonify({"stock_data": stock_data}), 200

    except Exception as e:
        logger.error(f"Error fetching stock data: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Prediction endpoint
@app.route("/api/predict", methods=["POST"])
def predict_stock_trend():
    """
    Predict stock trend based on provided data.
    """
    try:
        # Extract raw data from the request
        raw_data = request.get_json()
        logger.info(f"Received data for prediction: {raw_data}")

        # Clean and preprocess data
        cleaned_data = clean_stock_data(raw_data)
        features = prepare_features(cleaned_data)
        logger.info(f"Cleaned and prepared data: {features.head()}")

        # Make prediction (mock example)
        # Replace with actual model prediction later
        predictions = [1 if change > 0 else -1 for change in features["price_change"]]
        logger.info(f"Generated predictions: {predictions}")

        # Return predictions as JSON
        return jsonify({"predictions": predictions}), 200

    except Exception as e:
        logger.error(f"Error in prediction endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Run the app
if __name__ == "__main__":
    # Ensure logs directory exists
    if not os.path.exists("logs"):
        os.makedirs("logs")

    logger.info("Starting Flask app.")
    app.run(debug=True, host="0.0.0.0", port=5000)
