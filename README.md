[![Python application](https://github.com/sciomage-lab/DontScroll/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/sciomage-lab/DontScroll/actions/workflows/python-app.yml)

# DontScroll
Don’t scroll : AI를 활용한 이미지에 특화된 파일검색 엔진 플러그인 

![Uploading diagram.png…]()

# How to start

clone
```bash
git clone --recursive https://github.com/sciomage-lab/DontScroll.git
```

## 1. Slack bot setup

Create your own Slack bot.
We need a bot to help extract and retrieve messages.

## 2. Check the config file

Perhaps the config file is empty the first time you run it. 
The default settings file is located at `~/.config/dont_scroll/config.toml`.

Set environment variables for your environment. (variables such as slack bot secret and token)

```bash
mkdir ~/.config/dont_scroll
cp ./tools/default.toml ~/.config/dont_scroll/config.toml
vim ~/.config/dont_scroll/config.toml
```

`./tools/set_env.sh` is a script that imports toml settings into the shell environment.
Please refer to the [documentation.](./tools/README.md) for more details.

```bash
. tools/set_env.sh
```

## 3.1. Running via Docker (recommended)

Install Docker

```
sudo apt install docker.io
sudo apt install docker-compose
```

Install venv
```bash
python -m venv .venv # or python3 -m venv .venv
. .venv/bin/activate
python -V
```
# How to setup

```sh
pip install -r requirements.txt
```

# Set `PYTHONPATH`

```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
echo $PYTHONPATH
```



### 3.1.1. Run postgres docker

Please refer to [this document.](./docker/postgres/README.md)

```bash
./docker/postgres/stop.sh
./docker/postgres/start.sh
```

### 3.1.2. Run DontScroll docker

Please refer to [this document.](./docker/DontScroll/README.md)

```bash
./docker/DontScroll/stop.sh
./docker/DontScroll/start.sh
```

### 3.1.3. Check log and wait

Wait about 5 mins...

```bash
docker ps -a
docker logs {docker_id}
```

## 3.2. Run manually (not recommended)

### 3.2.1. Extract message history

The Slack bot extracts the message history and stores it in a database.

In particular, it analyzes media files. 
It may take a long time if there are a lot of messages because it involves downloading through the network.

```bash
python dont_scroll/slack_message_fetcher.py
```

### 3.2.2 Run webhook server

Executes a webhook that responds to the `/f`(find) command.
Retrieve message history by query.
The webhook server must always be running in order to respond to user commands.

```bash
python dont_scroll/webhook/slack_command.py
```

## 4. Use slack command

### 4.1. Find images
Send a message in a channel with a Slack bot.

`/f 3D graph image`
Then, it will probably find a 3D graph image.

### 4.2. Query Command

`/q Tell me the time of the next executive meeting`

## License
DontScroll has a `Sciomage LAB Public license`, as found in the [LICENSE](LICENSE.md) file.

## 3rd party licenses
Please refer to the [documentation](docs/license-list.md) for 3rd party licenses.
