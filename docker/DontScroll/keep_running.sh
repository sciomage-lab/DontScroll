#!/bin/bash

export PYTHONPATH="${PYTHONPATH}:${pwd}"
ls -al
echo $PYTHONPATH

python dont_scroll/slack_message_fetcher.py

python dont_scroll/webhook/slack_command.py

# Keep container running
tail -f /dev/null