"""基于loguru的日志器。"""
import os
import re
import sys

from loguru import logger

from core.config import config
from core.constants.path import logs_path


debug = config('debug', False)

if not os.path.exists(logs_path):
    os.mkdir(logs_path)

bot_name = re.split(r'[/\\]', sys.path[0])[-1].title()

args = sys.argv
if 'subprocess' in args:
    bot_name = args[-1].title()
if args[0].lower() == 'console.py':
    bot_name = 'Console'


def basic_logger_format(bot_name: str):
    return f"<cyan>[{bot_name.title()}]</cyan>"\
        "<yellow>[{name}:{function}:{line}]</yellow>"\
        "<green>[{time:YYYY-MM-DD HH:mm:ss}]</green>"\
        "<level>[{level}]:{message}</level>"


class LoggingLogger:
    def __init__(self, name):
        self.log = logger
        self.log.remove()
        self.info = None
        self.error = None
        self.debug = None
        self.warning = None
        self.exception = None
        self.critical = None

        self.rename(name)

        if debug:
            self.log.warning("Debug mode is enabled.")

    def rename(self, name):
        self.log.remove()
        self.log.add(
            sys.stderr,
            format=basic_logger_format(name),
            level="DEBUG" if debug else "INFO",
            colorize=True
        )

        log_file_path = os.path.join(logs_path, f"{name}_{{time:YYYY-MM-DD}}.log")
        self.log.add(
            log_file_path,
            format=basic_logger_format(name),
            retention="10 days",
            encoding="utf8"
        )
        self.info = self.log.info
        self.error = self.log.error
        self.debug = self.log.debug
        self.warning = self.log.warning
        self.exception = self.log.exception
        self.critical = self.log.critical


Logger = LoggingLogger(bot_name)
