
# Getting Started

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

# Setting environment variables

Please refer to [this document.](./tools/README.md)

```bash
mkdir ~/.config/dont_scroll
cp ./tools/default.toml ~/.config/dont_scroll/config.toml
vim ~/.config/dont_scroll/config.toml
```

XXX : Set API Key to `~/.config/dont_scroll/default.toml`

```bash
. tools/set_env.sh
```

# Run docker

## Run postgres docker

Please refer to [this document.](./docker/postgres/README.md)

```bash
cd docker/postgres
./stop.sh
./start.sh
```

## Run DontScroll docker

Please refer to [this document.](./docker/DontScroll/README.md)

```bash
cd docker/DontScroll
./stop.sh
./start.sh
```

```bash
docker ps -a
docker logs {docker_id}
```

Wait about 5 mins...
