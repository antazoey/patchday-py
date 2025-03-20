import logging
import sys
from functools import cached_property


class PDLogger:
    @cached_property
    def logger(self) -> logging.Logger:
        logger = logging.getLogger("patchday")
        if logger.hasHandlers():
            return logger

        # Create logger for the first time.
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def info(self, msg: str) -> None:
        self.logger.info(msg)

    def error(self, msg: str) -> None:
        self.logger.error(msg)

    def debug(self, msg: str) -> None:
        self.logger.debug(msg)


logger = PDLogger()
