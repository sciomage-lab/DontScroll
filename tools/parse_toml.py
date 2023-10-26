# Copyright (c) 2023 SciomageLAB
#
# This file is part of a project licensed under the Sciomage LAB Public License.
# 
# You are free to copy, modify, and distribute this file for commercial and non-commercial purposes,
# provided that you adhere to the license terms and conditions.
# 
# For more information, see the Sciomage LAB Public License which should accompany this project.


import os
import toml
import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        add_help=True,
        description=r"""
            Please provide SLACK_SIGNING_SECRET key through environment variable or config file
            Config file is located in $HOMEDIR/.config/dont_scroll/config.toml
            """,
    )

    parser.add_argument(
        "-c",
        "--config",
        help="Config file path",
        metavar="PATH",
        required=True,
        type=str,
    )
    args = parser.parse_args()

    if os.path.exists(args.config):
        config = toml.load(args.config)
    else:
        print("[fail] Not exist .toml config file")
        exit()

    for key, value in config.items():
        print(f"export {key.upper()}={value}")
