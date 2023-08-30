#!/bin/bash

mkdir -p ~/.config/dont_scroll
touch ~/.config/dont_scroll/config.toml
ls -al ~/.config/dont_scroll/config.toml
toml_config=~/.config/dont_scroll/config.toml
ls -al $toml_config

echo "SLACK_SIGNING_SECRET = \"$SLACK_SIGNING_SECRET\"" > $toml_config
echo "BOT_USER_OAUTH_TOKEN = \"$BOT_USER_OAUTH_TOKEN\"" >> $toml_config
echo "SLACK_APP_TOKEN = \"$SLACK_APP_TOKEN\"" >> $toml_config
echo "CHANNEL_ID = \"$CHANNEL_ID\"" >> $toml_config

echo "DB_HOST = \"$DB_HOST\"" >> $toml_config
echo "DB_PORT = $DB_PORT" >> $toml_config
echo "DB_USER = \"$DB_USER\"" >> $toml_config
echo "DB_PASSWORD = \"$DB_PASSWORD\"" >> $toml_config
echo "DB_NAME = \"$DB_NAME\"" >> $toml_config
echo "DB_TABLE = \"$DB_TABLE\"" >> $toml_config

echo "save toml config done."
