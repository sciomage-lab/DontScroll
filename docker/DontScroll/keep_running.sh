#!/bin/bash

export PYTHONPATH="${PYTHONPATH}:${pwd}"
ls -al
echo $PYTHONPATH

./save_envs.sh

mkdir models
wget -q -O models/llama-2-7b-arguments.Q4_K_M.gguf https://huggingface.co/TheBloke/llama-2-7B-Arguments-GGUF/resolve/main/llama-2-7b-arguments.Q4_K_M.gguf

python dont_scroll/slack_message_fetcher.py

python dont_scroll/webhook/slack_command.py

# Keep container running
tail -f /dev/null
