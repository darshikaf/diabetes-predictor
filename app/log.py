import logging
import sys

def get_logger(
    name: str = __name__, log_level: int = logging.INFO
) -> logging.Logger:
    """Use a custom logger to write logs to STDOUT. """
    # Set up default logging for submodules to use STDOUT
    logger = logging.getLogger(name)
    fmt = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    logging.basicConfig(stream=sys.stdout, level=log_level, format=fmt)

    return logger
