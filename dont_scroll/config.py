import os

import toml
from logger import applogger


def load(path: str):
    r"""
    Load config from TOML
    :return: dict
    """
    globals().update(os.environ)

    if os.path.exists(path):
        with open(path) as f:
            try:
                globals().update(toml.load(f))
                return True
            except ValueError:
                applogger.critical(
                    r"""
                    Config file contains invalid format data.
                """
                )

    if "SLACK_SIGNING_SECRET" not in globals().keys():
        applogger.critical(
            r"""
            Please provide SLACK_SIGNING_SECRET key
            through environment variable or config file.
        """
        )

        return False

    if "BOT_USER_OAUTH_TOKEN" not in globals().keys():
        applogger.critical(
            r"""
            Please provide BOT_USER_OAUTH_TOKEN key
            through environment variable or config file.
        """
        )

        return False
