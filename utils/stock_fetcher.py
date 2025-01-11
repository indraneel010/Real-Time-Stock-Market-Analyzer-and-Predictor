import requests
import logging
import os
from utils.logger import setup_logger

# Initialize logger for stock_fetcher
logger = setup_logger("stock_fetcher", log_file="logs/stock_fetcher.log")

def fetch_stock_data(symbol):
    """
    Fetch real-time stock data for a given symbol using a stock market API.

    Args:
        symbol (str): Stock ticker symbol.
    
    Returns:
        list: List of dictionaries containing stock data (time, open, close).
    
    Raises:
        Exception: If the API call fails or the symbol is invalid.
    """
    # Example API (use your preferred provider)
    API_KEY = os.getenv("STOCK_API_KEY", "demo")  # Replace 'demo' with a real API key
    BASE_URL = "https://www.alphavantage.co/query"
    
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "1min",
        "apikey": API_KEY,
    }

    logger.info(f"Fetching stock data for symbol: {symbol}")

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "Time Series (1min)" not in data:
            error_message = f"Invalid stock symbol or data not available for {symbol}."
            logger.error(error_message)
            raise ValueError(error_message)

        time_series = data["Time Series (1min)"]
        parsed_data = [
            {"time": time, "open": float(values["1. open"]), "close": float(values["4. close"])}
            for time, values in time_series.items()
        ]
        logger.info(f"Successfully fetched data for symbol: {symbol}")
        return parsed_data

    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP request error while fetching stock data: {str(e)}")
        raise Exception("Failed to fetch stock data due to an HTTP error.") from e
    except ValueError as e:
        logger.error(f"Data error: {str(e)}")
        raise e
    except Exception as e:
        logger.error(f"Unexpected error while fetching stock data: {str(e)}")
        raise e

# Mock function for testing purposes
def mock_stock_data(symbol):
    """
    Generate mock stock data for testing.

    Args:
        symbol (str): Stock ticker symbol.

    Returns:
        list: List of mock stock data (time, open, close).
    """
    logger.info(f"Generating mock data for symbol: {symbol}")
    return [
        {"time": "2025-01-11 15:00:00", "open": 100.5, "close": 101.2},
        {"time": "2025-01-11 15:01:00", "open": 101.2, "close": 102.0},
        {"time": "2025-01-11 15:02:00", "open": 102.0, "close": 101.8},
    ]
