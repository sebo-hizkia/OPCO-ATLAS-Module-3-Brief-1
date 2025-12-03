from loguru import logger

# Configuration du logger
logger.add("logs/predict_api.log", rotation="100 MB", level="INFO")

# Logger global accessible partout
app_logger = logger
