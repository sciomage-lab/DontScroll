#!/bin/bash
# Copyright (c) 2023 SciomageLAB
#
# This file is part of a project licensed under the Sciomage LAB Public License.
#
# You are free to copy, modify, and distribute this file for commercial and non-commercial purposes,
# provided that you adhere to the license terms and conditions.
#
# For more information, see the Sciomage LAB Public License which should accompany this project.


export PYTHONPATH="${PYTHONPATH}:${pwd}"
ls -al
echo $PYTHONPATH

./save_envs.sh

mkdir -p models
echo "Download gguf file..."
wget -q -nc -O models/llama-2-7b-arguments.Q4_K_M.gguf https://huggingface.co/TheBloke/llama-2-7B-Arguments-GGUF/resolve/main/llama-2-7b-arguments.Q4_K_M.gguf
echo "Download gguf file done."

python dont_scroll/slack_message_fetcher.py

python dont_scroll/webhook/slack_command.py

# Keep container running
tail -f /dev/null
