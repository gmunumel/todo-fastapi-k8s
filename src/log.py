import logging
import posixpath

from pythonjsonlogger import jsonlogger

FORMAT = "%(asctime)s %(levelname)s %(message)s %(thread)s"


# Custom JSON formatter to rename fields
class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record["@timestamp"] = log_record.pop(
            "asctime", None
        )  # Rename 'asctime' to '@timestamp'
        log_record["level"] = log_record.pop(
            "levelname", None
        )  # Rename 'levelname' to 'level'


# Configure JSON logging
log_handler = logging.StreamHandler()
formatter = CustomJsonFormatter(FORMAT)
log_handler.setFormatter(formatter)

# Log to a file
file_handler = logging.FileHandler(posixpath.join("logs", "todo-fastapi-k8s.log"))
file_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)
logger.addHandler(file_handler)
