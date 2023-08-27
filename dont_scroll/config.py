import os
import toml

from logger import applogger

<<<<<<< Updated upstream
=======
_CONFIGS = {
    "SLACK_SIGNING_SECRET": "<YOUR SIGING KEY>",
    "BOT_USER_OAUTH_TOKEN": "<YOUR AUTH TOKEN>",
    "SLACK_APP_TOKEN": "<YOUR BOT TOKEN>",
    "CHANNEL_ID": "<YOUR BOT TOKEN>",
}


>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
    if "SLACK_SIGNING_SECRET" not in globals().keys():
        applogger.critical(
            r"""
            Please provide SLACK_SIGNING_SECRET key
            through environment variable or config file.
        """
        )
=======
    # If file not exis on path, make config file on path
    else:
        os.makedirs(os.path.dirname(path), mode=0o700, exist_ok=True)
        with open(path, "w") as f:
            toml.dump(_CONFIGS, f)
>>>>>>> Stashed changes

        return False

<<<<<<< Updated upstream
    if "BOT_USER_OAUTH_TOKEN" not in globals().keys():
        applogger.critical(
            r"""
            Please provide BOT_USER_OAUTH_TOKEN key
            through environment variable or config file.
        """
        )

        return False
=======
    # Check all needed key and token provided and can be found on global
    for CONFIG in _CONFIGS.keys():
        if CONFIG not in globals().keys() or globals()[CONFIG] == "":
            msg = r"""
            Please provide {config} key
            through environment variable or config file.
            Check file {path}.
            """
            msg = msg.format(config=CONFIG, path=path)
            applogger.critical(msg)

            return False

    return True
>>>>>>> Stashed changes
