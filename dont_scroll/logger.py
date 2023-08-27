import logging
import sys


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
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
    stream_handler.setFormatter(CustomFormatter())
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