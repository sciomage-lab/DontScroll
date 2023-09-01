import os
import toml
import sys

config_path = os.path.join(os.path.expanduser("~"), ".config/dont_scroll/config.toml")
config = toml.load(config_path)

for key, value in config.items():
    print(f"export {key.upper()}={value}")
