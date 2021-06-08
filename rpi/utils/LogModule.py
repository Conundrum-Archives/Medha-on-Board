import logging

def init_logger():
  # init log module
  logging.basicConfig(
    format='%(asctime)-15s - %(levelname)8s - %(module)10s - %(message)s',
    level=logging.INFO,
    datefmt='%m/%d/%Y %I:%M:%S.%p',
    handlers=[
      logging.FileHandler("medha.log"),
      logging.StreamHandler()
    ]
  )
  return logging.getLogger(__name__)
