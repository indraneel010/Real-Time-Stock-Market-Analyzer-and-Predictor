from flask import Flask, jsonify, request
import pickle
import os
from utils.stock_fetcher import fetch_stock_data  # Utility to fetch stock data
from utils.logger import setup_logger  # Utility for logging

# Initialize Flask app
app = Flask(__name__)

# Set up logger
logger = setup_logger("stock_analyzer")

# Load pre-trained ML model
MODEL_PATH = "models/stock_model.pkl"
try:
    with open(MODEL_PATH, "rb") as model_file:
        model = pickle.load(model_file)
    logger.info("ML model loaded successfully.")
except FileNotFoundError:
    logger.error(f"Model file not found at {MODEL_PATH}.")
    raise FileNotFoundError("Model file not found! Make sure 'stock_model.pkl' exists.")

# Health check endpoint
@app.route("/", methods=["GET"])
def home():
    logger.info("Health check endpoint accessed.")
    return jsonify({"message": "Stock Analyzer API is running!"})

# Endpoint to fetch stock data
@app.route("/api/stock-data", methods=["GET"])
def stock_data():
    symbol = request.args.get("symbol")
    if not symbol:
        logger.warning("Stock symbol not provided.")
        return jsonify({"error": "Stock symbol is required"}), 400
    try:
        data = fetch_stock_data(symbol)
        logger.info(f"Stock data fetched for symbol: {symbol}")
        return jsonify({"symbol": symbol, "data": data})
    except Exception as e:
        logger.error(f"Error fetching stock data: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Endpoint to predict stock trends
@app.route("/api/predict", methods=["POST"])
def predict():
    request_data = request.get_json()
    if not request_data or "features" not in request_data:
        logger.warning("Prediction features not provided.")
        return jsonify({"error": "Features for prediction are required"}), 400
    features = request_data["features"]
    try:
        prediction = model.predict([features])
        logger.info("Prediction made successfully.")
        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        logger.error(f"Error making prediction: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
from utils.logger import setup_logger

# Initialize logger
logger = setup_logger("stock_analyzer")
