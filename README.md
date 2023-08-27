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
