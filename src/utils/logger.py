from datetime import datetime
from os import getcwd
from os.path import join
from sys import stdout, exit

from loguru import logger

from .file_utils import check_directory
from ..config import config


def logger_init() -> None:
    check_directory(join(getcwd(), "logs"), create_if_not_exist=True)

    log_format = ("<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</> <light-red>|</> "
                  "<yellow>{thread:<5}</> <light-red>|</> "
                  "<magenta>{elapsed}</> <light-red>|</> "
                  "<level>{level:8}</> <light-red>|</> "
                  "<cyan>{name}<light-red>:</>{function}<light-red>:</>{line}</> "
                  "<light-red>-</> <level>{message}</>")
    logger.debug(f"Change logger level to {config.log_level.upper()}")
    logger.remove()
    if config.debug_mode:
        logger.add(stdout, format=log_format, level=config.log_level.upper())
    logger.add(join(getcwd(), f"./logs/output_{datetime.strftime(datetime.now(), '%Y-%m-%d')}.log"),
               format=log_format, rotation="00:00", compression="zip",
               level=config.log_level.upper())
    if config.log_level.upper() != "TRACE":
        logger.add(join(getcwd(), f"./logs/output_{datetime.strftime(datetime.now(), '%Y-%m-%d')}-full.log"),
                   format=log_format, rotation="00:00", compression="zip",
                   level="TRACE")
    logger.add(lambda _: exit(-1), level="CRITICAL")
