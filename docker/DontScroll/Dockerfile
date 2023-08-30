FROM python:3.8.10
RUN python3 --version

# Update Python & Install wheel
RUN python3 -m pip install pip --upgrade
RUN python3 -m pip install wheel

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Git clone
RUN git clone https://github.com/sciomage-lab/DontScroll.git /app

# Set the working directory
WORKDIR /app

# Install requirements.txt
RUN pip install -r requirements.txt

# Set env
COPY save_envs.sh /app/save_envs.sh
RUN chmod +x /app/save_envs.sh && /app/save_envs.sh

# Copy main script
COPY keep_running.sh /app/keep_running.sh
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

RUN ls -al /app
RUN ls -al /app/keep_running.sh
CMD ["/app/keep_running.sh"]
