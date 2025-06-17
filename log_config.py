import logging
import os

def setup_logger (file_path: str = 'logs/app.log', level = logging.INFO):
    """
    Sets up a logger that writes logs to a file and the console.

    param file_path: The path of the log file. (default is 'data/app.log')
    param level: The logging level (default is INFO).
    """
    #Ensures the director is exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Creates a logger
    logger = logging.getLogger()
    
    if logger.handlers:
        # If the logger already has handlers, skip setting it up again
        return logger
    
    # Sets the logging level
    logger.setLevel(level)

    # Sets up a formatter
    formatter = logging.Formatter (
        "%(asctime)s - [%(levelname)s] - %(name)s : %(message)s"
    )

    # Creates a console handler
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Creates a file handler
    fh = logging.FileHandler(file_path)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    logging.info("long_config.py: Logging configuration created.")
    return logger