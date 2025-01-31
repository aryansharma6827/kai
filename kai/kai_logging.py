import logging
import os

from kai.models.kai_config import KaiConfig

parent_log = logging.getLogger("kai")

# console_handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(levelname)s - %(asctime)s - %(name)s - [%(filename)20s:%(lineno)-4s - %(funcName)20s()] - %(message)s"
)


def process_log_dir_replacements(log_dir: str):
    ##
    # We want to replace $pwd with the location of the Kai project directory,
    # this is needed to help with specifying from configuration
    ##
    if log_dir.startswith("$pwd"):
        log_dir = log_dir.replace(
            "$pwd", os.path.join(os.path.dirname(os.path.realpath(__file__)), "../")
        )
    return log_dir


def setup_console_handler(logger, log_level: str = "INFO"):
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    print(f"Console logging for '{parent_log.name}' is set to level '{log_level}'")


def setup_file_handler(
    logger, log_file_name: str, log_dir: str, log_level: str = "DEBUG"
):
    # Ensure any needed log directories exist
    log_dir = process_log_dir_replacements(log_dir)
    log_file_path = os.path.join(log_dir, log_file_name)
    if log_dir.startswith("$pwd"):
        log_dir = os.path.join(os.getcwd(), log_dir[5:])
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    print(
        f"File logging for '{logger.name}' is set to level '{log_level}' writing to file: '{log_file_path}'"
    )


def initLogging(console_log_level, file_log_level, log_dir, log_file="kai_server.log"):
    setup_console_handler(parent_log, console_log_level)
    setup_file_handler(parent_log, log_file, log_dir, file_log_level)
    # Attempt to set the parent log level to
    # most permissive and allow child loggers to control what is filtered or not
    parent_log.setLevel("DEBUG")


def initLoggingFromConfig(config: KaiConfig):
    initLogging(config.log_level.upper(), config.file_log_level.upper(), config.log_dir)
