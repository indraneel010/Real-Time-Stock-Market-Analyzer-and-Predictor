import logging
import os

def setup_logger(name, log_file="logs/app.log", level=logging.INFO):
    """
    Set up a logger for the application.

    Args:
        name (str): Name of the logger.
        log_file (str): Path to the log file.
        level (int): Logging level (e.g., logging.INFO, logging.DEBUG).

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Ensure the logs directory exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # File handler to write logs to a file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)

    # Console handler to print logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
