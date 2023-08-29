[![Python application](https://github.com/sciomage-lab/DontScroll/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/sciomage-lab/DontScroll/actions/workflows/python-app.yml)

# DontScroll
Don’t scroll : AI를 활용한 이미지에 특화된 파일검색 엔진 플러그인 

# How to setup
```sh
pip install -r requirements.txt
```
> For Development
```sh
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Before commit 
Use `isort`` to reorder package import and reformat using autu linter `black``.
Use `pylint` for static code analysis
```sh
isort <Project-Root-Path>
black <Project-Root-Path>
pylint
```

# How to start

## Slack bot setup

Create your own Slack bot.
We need a bot to help extract and retrieve messages.
For detailed settings, see the [documentation.](./) (to be written)

## Run docker

This repo requires postgresql. Please refer to the [documentation.](./docker/postgres/README.md)
Check the running status of the postgresql container.

## Check the config file

Perhaps the config file is empty the first time you run it. 
The default settings file is located at `~/.config/dont_scroll/config.toml`.

Set environment variables for your environment. (variables such as slack bot secret and token)

## Extract message history

The Slack bot extracts the message history and stores it in a database.

In particular, it analyzes media files. 
It may take a long time if there are a lot of messages because it involves downloading through the network.

```bash
python dont_scroll/slack_message_fetcher.py
```

## Run webhook server

Executes a webhook that responds to the `/find` command.
Retrieve message history by query.
The webhook server must always be running in order to respond to user commands.

```bash
python dont_scroll/webhook/slack_command.py
```

## Use slack command

Send a message in a channel with a Slack bot.

`/find 3D graph image`
Then, it will probably find a 3D graph image.

# TODO 

```sh
python main.py
```

## Options
```sh
python main.py --help
```
```txt
options:
  -h, --help     show this help message and exit
  --debug        Show more detail
  --port NUMBER
  --config PATH  Config file path
  ```

## Config file template
Our configuration file follows the TOML format.
```toml
SLACK_SIGNING_SECRET = "<Your slack SINGING_SECRET_KEY>"
```
