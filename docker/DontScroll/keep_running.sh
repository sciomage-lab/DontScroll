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

mkdir models
wget -O models/tinyllama-1.1b-1t-openorca.Q5_K_M.gguf https://huggingface.co/TheBloke/TinyLlama-1.1B-1T-OpenOrca-GGUF/resolve/main/tinyllama-1.1b-1t-openorca.Q5_K_M.gguf

python dont_scroll/slack_message_fetcher.py

python dont_scroll/webhook/slack_command.py

# Keep container running
tail -f /dev/null
