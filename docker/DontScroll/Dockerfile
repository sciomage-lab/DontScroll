FROM python:3.10.16
RUN python3 --version

# Branch name (for github action script)
ARG BRANCH_NAME=main

# Update Python & Install wheel
RUN python3 -m pip install pip --upgrade
RUN python3 -m pip install wheel

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Git clone
COPY . /app

# Set the working directory
WORKDIR /app

# Install requirements.txt
RUN pip install -r requirements.txt

# Set env
COPY docker/DontScroll/save_envs.sh /app/save_envs.sh
RUN chmod +x /app/save_envs.sh && /app/save_envs.sh

# Copy main script
COPY docker/DontScroll/keep_running.sh /app/keep_running.sh
RUN chmod +x /app/keep_running.sh

# Set environment variables
ENV SLACK_SIGNING_SECRET="xxxx"
ENV BOT_USER_OAUTH_TOKEN="xxxx"
ENV SLACK_APP_TOKEN="xxxx"
ENV CHANNEL_ID="xxxx"

ENV DB_HOST = "127.0.0.1"
ENV DB_PORT = 5432
ENV DB_USER = "dont_scroll"
ENV DB_PASSWORD = "secret"
ENV DB_NAME = "dont_scroll_db"
ENV DB_TABLE = "public.slack_message"

CMD ["/app/keep_running.sh"]
