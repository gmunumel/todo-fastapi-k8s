import logging

from pythonjsonlogger import jsonlogger

FORMAT = "%(asctime)s - %(thread)s - %(levelname)s - %(message)s"

# Configure JSON logging
log_handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter(FORMAT)
log_handler.setFormatter(formatter)

# Log to a file
file_handler = logging.FileHandler("todo-fastapi-k8s.log")
file_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)
logger.addHandler(file_handler)
