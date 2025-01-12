import pandas as pd
import logging
from utils.logger import setup_logger

# Set up logger for data processor
logger = setup_logger("data_processor", log_file="logs/data_processor.log")

def clean_stock_data(raw_data):
    """
    Clean and preprocess raw stock data.
    
    Args:
        raw_data (list): List of dictionaries containing raw stock data 
                         (e.g., [{"time": ..., "open": ..., "close": ...}, ...]).
    
    Returns:
        pd.DataFrame: Cleaned and preprocessed stock data as a DataFrame.
    """
    logger.info("Starting data cleaning process.")
    try:
        # Convert raw data to DataFrame
        df = pd.DataFrame(raw_data)
        logger.debug(f"Raw data converted to DataFrame: {df.head()}")

        # Ensure required columns exist
        required_columns = ["time", "open", "close"]
        if not all(col in df.columns for col in required_columns):
            missing_cols = set(required_columns) - set(df.columns)
            error_message = f"Missing columns in data: {missing_cols}"
            logger.error(error_message)
            raise ValueError(error_message)

        # Convert 'time' to datetime
        df["time"] = pd.to_datetime(df["time"])
        logger.debug("Converted 'time' column to datetime.")

        # Sort by time in ascending order
        df.sort_values(by="time", inplace=True)
        logger.info("Sorted data by time in ascending order.")

        # Add additional features (e.g., price change)
        df["price_change"] = df["close"] - df["open"]
        logger.info("Added 'price_change' feature.")

        # Drop rows with missing or invalid data
        initial_row_count = len(df)
        df.dropna(inplace=True)
        cleaned_row_count = len(df)
        logger.info(f"Dropped rows with missing values. Rows before: {initial_row_count}, after: {cleaned_row_count}.")

        logger.info("Data cleaning process completed successfully.")
        return df

    except Exception as e:
        logger.error(f"Error during data cleaning: {str(e)}")
        raise e

def prepare_features(df):
    """
    Prepare features from cleaned stock data for ML predictions.
    
    Args:
        df (pd.DataFrame): Cleaned stock data.
    
    Returns:
        pd.DataFrame: Features ready for ML model input.
    """
    logger.info("Starting feature preparation process.")
    try:
        # Select relevant columns for features
        features = df[["price_change"]].copy()
        logger.debug(f"Selected features: {features.head()}")

        # Normalize features (optional, based on model requirements)
        features["price_change"] = (features["price_change"] - features["price_change"].mean()) / features["price_change"].std()
        logger.info("Normalized 'price_change' feature.")

        logger.info("Feature preparation completed successfully.")
        return features

    except Exception as e:
        logger.error(f"Error during feature preparation: {str(e)}")
        raise e
