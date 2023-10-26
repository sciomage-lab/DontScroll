# Copyright (c) 2023 SciomageLAB
#
# This file is part of a project licensed under the Sciomage LAB Public License.
# 
# You are free to copy, modify, and distribute this file for commercial and non-commercial purposes,
# provided that you adhere to the license terms and conditions.
# 
# For more information, see the Sciomage LAB Public License which should accompany this project.


import logging
import sys


class ColoredLogFormatter(logging.Formatter):
    
    COLOR_CODES = {
        'grey': "\x1b[38;20m",
        'yellow': "\x1b[33;20m",
        'red': "\x1b[31;20m",
        'bold_red': "\x1b[31;1m",
        'reset': "\x1b[0m",
    }

    DEFAULT_FORMAT = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    LEVEL_TO_COLOR = {
        logging.DEBUG: COLOR_CODES['grey'],
        logging.INFO: COLOR_CODES['grey'],
        logging.WARNING: COLOR_CODES['yellow'],
        logging.ERROR: COLOR_CODES['red'],
        logging.CRITICAL: COLOR_CODES['bold_red'],
    }

    def format(self, record):
        color_code = self.LEVEL_TO_COLOR.get(record.levelno, self.COLOR_CODES['reset'])
        log_format = f"{color_code}{self.DEFAULT_FORMAT}{self.COLOR_CODES['reset']}"
        formatter = logging.Formatter(log_format)
        return formatter.format(record)


applogger = logging.Logger("DontScroll App logger")

# Console stdout
stream_handler = logging.StreamHandler()

# Check Python version
if sys.version_info[:2] >= (3, 9):
    # Python version 3.9 or higher
    logging.basicConfig(encoding="utf-8", level=logging.INFO)
else:
    # Python version lower than 3.9
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stream_handler.setFormatter(ColoredLogFormatter())
    logging.basicConfig(level=logging.INFO, handlers=[stream_handler])

applogger.addHandler(stream_handler)


def set_all_logger_debug_mode():
    global applogger
    applogger.setLevel(logging.DEBUG)


if __name__ == "__main__":
    print("Logger Test")
    applogger.setLevel(level=logging.DEBUG)
    applogger.debug("Debug log")
    applogger.info("Info log")
    applogger.warning("Warning log")
    applogger.critical("Critical log")
