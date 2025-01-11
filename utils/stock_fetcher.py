import requests
import logging
import os

# Fetch stock data from an API (e.g., Alpha Vantage, Yahoo Finance)
def fetch_stock_data(symbol):
    """
    Fetch real-time stock data for a given symbol.
    
    Args:
        symbol (str): Stock ticker symbol.
    
    Returns:
        dict: Parsed stock data.
    
    Raises:
        Exception: If the API call fails or the symbol is invalid.
    """
    # Example API URL (replace with your preferred API provider)
    API_KEY = os.getenv("STOCK_API_KEY", "demo")  # Add your API key here
    BASE_URL = "https://www.alphavantage.co/query"
    
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": "1min",
        "apikey": API_KEY,
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "Time Series (1min)" not in data:
            raise ValueError(f"Invalid stock symbol or data not available for {symbol}")

        time_series = data["Time Series (1min)"]
        parsed_data = [
            {"time": time, "open": values["1. open"], "close": values["4. close"]}
            for time, values in time_series.items()
        ]
        return parsed_data
    except Exception as e:
        logging.error(f"Error fetching stock data for symbol {symbol}: {str(e)}")
        raise

# Mock function (for testing without API)
def mock_stock_data(symbol):
    """
    Generate mock stock data for testing.

    Args:
        symbol (str): Stock ticker symbol.

    Returns:
        list: Mocked stock data.
    """
    logging.info(f"Generating mock data for symbol: {symbol}")
    return [
        {"time": "2025-01-11 15:00:00", "open": 100.5, "close": 101.2},
        {"time": "2025-01-11 15:01:00", "open": 101.2, "close": 102.0},
        {"time": "2025-01-11 15:02:00", "open": 102.0, "close": 101.8},
    ]
