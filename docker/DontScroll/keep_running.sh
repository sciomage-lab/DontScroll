#!/bin/bash

export PYTHONPATH="${PYTHONPATH}:${pwd}"
ls -al
echo $PYTHONPATH

./save_envs.sh

mkdir models
wget -q -O models/tinyllama-1.1b-1t-openorca.Q5_K_M.gguf https://huggingface.co/TheBloke/TinyLlama-1.1B-1T-OpenOrca-GGUF/resolve/main/tinyllama-1.1b-1t-openorca.Q5_K_M.gguf

python dont_scroll/slack_message_fetcher.py

python dont_scroll/webhook/slack_command.py

# Keep container running
tail -f /dev/null
