import os
from functools import lru_cache
from logging import Logger

from dotenv import load_dotenv


@lru_cache
def get_logger() -> Logger:
    from loguru import logger

    return logger


@lru_cache
def get_env_variable(env_var_name: str) -> str:
    load_dotenv()
    return os.getenv(env_var_name)
