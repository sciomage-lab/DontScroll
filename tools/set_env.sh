#!/bin/bash

# TOML 파일을 파싱하여 환경 변수로 설정
eval $(python3 ./tools/parse_toml.py -c ./tools/default.toml)

# 이제 $DATABASE_USER와 $DATABASE_PASSWORD 환경 변수를 사용할 수 있습니다.
echo "SLACK_SIGNING_SECRET : $SLACK_SIGNING_SECRET"
echo "BOT_USER_OAUTH_TOKEN : $BOT_USER_OAUTH_TOKEN"
echo "SLACK_APP_TOKEN : $SLACK_APP_TOKEN"
echo "CHANNEL_ID : $CHANNEL_ID"
echo "DB_HOST : $DB_HOST"
echo "DB_PORT : $DB_PORT"
echo "DB_USER : $DB_USER"
echo "DB_PASSWORD : $DB_PASSWORD"
echo "DB_NAME : $DB_NAME"
echo "DB_TABLE : $DB_TABLE"
