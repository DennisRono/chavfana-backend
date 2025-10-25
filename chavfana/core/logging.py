import logging
from datetime import datetime
import os
from pathlib import Path
from contextlib import contextmanager

# Create logs directory if it doesn't exist
logs_dir = Path("/tmp/logs")
logs_dir.mkdir(parents=True, exist_ok=True)

class GLibWarningFilter(logging.Filter):
    def filter(self, record):
        return not (record.getMessage().startswith('GLib-GIO-WARNING') and 
                   ('has no verbs' in record.getMessage() or 
                    'UWP app' in record.getMessage()))

# Configure logging
def setup_logging():
    log_file = logs_dir / f"bebewa_{datetime.now().strftime('%Y-%m-%d')}.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ],
    )
    
    for logger_name in [
        "weasyprint",
        "fontTools",
        "fontTools.subset",
        "fontTools.subset.timer",
        "fontTools.ttLib.ttFont",
        "PIL",
        "cssselect",
        "cffi",
        "cairocffi"
    ]:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.CRITICAL)  # 50
        logger.propagate = False  # Prevent propagation to parent loggers
        logger.addHandler(logging.NullHandler())
        logger.addFilter(GLibWarningFilter())

    # Create logger
    logger = logging.getLogger("provisioning_ms")
    return logger

os.environ['GIO_EXTRA_MODULES'] = ''

@contextmanager
def quiet_weasyprint():
    """Context manager to suppress WeasyPrint-related warnings"""
    import warnings
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        yield

logger = setup_logging()
