import os
import sys
import argparse
import toml
from flask import Flask
import config
from logger import applogger, set_all_logger_debug_mode


def initialize(args):
  r"""
  Find SLACK_SIGNING_SECRET key
  """
  global SLACK_SIGNING_SECRET
  return config.load(args.config)


# Start the server on port 3000
if __name__ == "__main__":
  parser = argparse.ArgumentParser(add_help=True, description=r"""
      Please provide SLACK_SIGNING_SECRET key through environment variable or config file.
      Config file is located in $HOMEDIR/.config/dont_scroll/config.toml
  """)
  parser.add_argument('--debug', action='store_true', help="Show more detail")
  parser.add_argument('--port', metavar="NUMBER", type=int, default=3000)
  parser.add_argument('--config', 
                      default=os.path.join(os.path.expanduser("~"), ".config/dont_scroll/config.toml"),
                      help="Config file path", metavar="PATH", type=str)
  args = parser.parse_args()

  if args.debug:
    set_all_logger_debug_mode()

  if initialize(args):
    app = Flask(__name__)

    import slack_event_listener
    app.register_blueprint(slack_event_listener.blueprint)

    app.run(port=args.port, debug=args.debug)
  else:
    applogger.critical("App cannot be started")

