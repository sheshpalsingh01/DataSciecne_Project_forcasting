import logging
import os, sys
from datetime import datetime

# create a timestemp for the logging
LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"

# create the logs dir
LOG_DIR = os.path.join(os.getcwd(), "logs")

os.makedirs(LOG_DIR, exist_ok=True)

# create a complate log file
LOG_FILE_PATH = os.path.join(LOG_DIR,LOG_FILE)

# Configure logging with both file  console handlers
logging.basicConfig(
    format="[%(asctime)s] %(name)s %(levelname)s line %(lineno)d: %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler(sys.stdout)
    ]
)

# Create a reusable logger
logger = logging.getLogger("forcastingProject")