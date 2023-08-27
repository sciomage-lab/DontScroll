import os

import toml
from logger import applogger


_CONFIGS = {
    "SLACK_SIGNING_SECRET": "<YOUR SIGING KEY>", 
    "BOT_USER_OAUTH_TOKEN": "<YOUR AUTH TOKEN>"
    "SLACK_APP_TOKEN": "<YOUR BOT TOKEN>",
    "CHANNEL_ID": "<YOUR BOT TOKEN>"
}


def load(path: str):
    r"""
    Load config from TOML
    :return: dict
    """
    globals().update(os.environ)
    config_file = None

    # Load key and token for API on global scope variable
    if os.path.exists(path):
        with open(path) as f:
            try:
                globals().update(toml.load(f))
            except ValueError:
                applogger.critical(
                    r"""
                    Config file contains invalid format data.
                    """
                )

    # If file not exis on path, make config file on path
    else:
        os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
        with open(path, 'w') as f:
            toml.dump(_CONFIGS, f)

        applogger.info(f"Config file genated on path {path}")

    # Check all needed key and token provided and can be found on global
    for CONFIG in _CONFIGS.keys():
        if CONFIG not in globals().keys() or globals()[CONFIG] == "":
            msg =r"""
            Please provide {config} key
            through environment variable or config file.
            Check file {path}.
            """
            msg = msg.format(config=CONFIG, path=path)
            applogger.critical(msg)
 
            return False

    return True