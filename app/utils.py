import os
from functools import lru_cache
from logging import DEBUG, Logger, getLogger

from dotenv import load_dotenv


@lru_cache
def get_logger() -> Logger:
    logger = getLogger()
    logger.setLevel(DEBUG)
    return logger


@lru_cache
def get_env_variable(env_var_name: str) -> str:
    load_dotenv()
    return os.getenv(env_var_name)
