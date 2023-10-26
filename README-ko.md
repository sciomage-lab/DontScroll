[![Python application](https://github.com/sciomage-lab/DontScroll/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/sciomage-lab/DontScroll/actions/workflows/python-app.yml)

# DontScroll
Don’t scroll : AI를 활용한 이미지에 특화된 파일검색 엔진 플러그인 

# 사용법

## 1. Slack bot 설치

이미지를 검색하고 쿼리를 질문하는 `Don't scroll`을 사용하기 위해서 자기 소유의 Slack bot을 생성해야 합니다.

[Slack App](https://api.slack.com/apps)을 참고 하세요.

## 2. config file 확인

기본 설정 파일은 `~/.config/dont_scroll/config.toml`에 있습니다.
이 저장소를 clone 하면 설정파일은 비어 있습니다.
Slack 봇, 토큰 등 환경변수를 설정해야 합니다.

다음 커멘드를 따라서 기본 설정파일 템플릿을 복사하고 설정파일을 수정해서 올바른 Slack 토큰과 설정값을 지정합니다.

```bash
mkdir ~/.config/dont_scroll
cp ./tools/default.toml ~/.config/dont_scroll/config.toml
vim ~/.config/dont_scroll/config.toml
```

`./tools/set_env.sh` 스크립트는 toml 설정파일을 쉘 환경으로 가져옵니다.
다음 커멘드를 따라서 간편한 설치와 사용을 위해서 설정파일에 올바른 값을 입력하고 스크립트를 통해서 설정값을 쉘 환경변수로 가져옵니다.

```bash
. tools/set_env.sh
```

[문서](./tools/README.md)에서 자세한 정보를 확인할 수 있습니다.

## 3.1. Docker를 이용한 설치(추천)

### 3.1.1. postgres docker 실행

[이 문서](./docker/postgres/README.md)를 참고하세요.

다음 커멘드를 이용해서 docker 이미지를 빌드하고 실행하거나 중지 할 수 있습니다.

```bash
./docker/postgres/stop.sh
./docker/postgres/start.sh
```

### 3.1.2. DontScroll docker 실행

[이 문서](./docker/DontScroll/README.md)를 참고 하세요.

다음 커멘드를 이용해서 docker 이미지를 빌드하고 실행하거나 중지 할 수 있습니다.

```bash
./docker/DontScroll/stop.sh
./docker/DontScroll/start.sh
```

### 3.1.3. 기다리기와 로그 확인

`Don't Scroll` Docker가 실행되면 설정에 따라 워크스페이스 정보를 읽고 분석하는데 약 5분정도의 시간이 소요됩니다.
이 시간은 워크스페이스의 대화량, 이미지 개수, 컴퓨터 성능에 따라 달라질 수 있습니다.

다음 커멘드를 이용해서 로그를 확인하고 진행 상태를 볼 수 있습니다.  

```bash
docker ps -a
docker logs {docker_id}
```

## 3.2. 수동 실행(추천하지 않음)

### 3.2.1. 메시지 기록 분석

Slack 봇은 메시지 기록을 추출하여 데이터베이스에 저장합니다.
네트워크를 통해 다운로드하고 분석하기 때문에 메시지가 많을 경우 시간이 오래 걸릴 수 있습니다.

다음 커멘트를 이용해서 메세지 기록을 추출할 수 있습니다.

```bash
python dont_scroll/slack_message_fetcher.py
```

### 3.2.2 커멘드 server 실행

`/f`(find) 명령와 `/q`(query) 명령에 응답하는 서버를 실행합니다. 
사용자 명령에 응답하려면 커맨드 서버가 항상 실행 중이어야 합니다.

다음 커멘드를 이용해서 커멘드 서버를 실행할 수 있습니다.

```bash
python dont_scroll/webhook/slack_command.py
```

## 4. slack 커멘드 사용하기

### 4.1. 이미지 찾기

Slack 봇을 사용하여 찾고싶은 이미지를 채널에서 메시지를 보냅니다

`/f 3D graph image`
그러면, 3D 그래프 이미지 이미지를 찾을 것입니다.

### 4.2. Query Command

Slack 봇을 사용하여 묻고싶은 질문을 채널에서 메시지를 보냅니다

`/q Tell me the time of the next executive meeting`
그러면, 대화 내용을 기반으로 정확한 시간을 알려줄 것입니다.

## 라이센스
Don't Scroll은 [LICENSE](LICENSE.md) 파일에 있는 `Sciomage LAB 공개 라이센스`를 따릅니다.

## 3rd party 라이센스
3rd party licenses는 [문서](docs/license-list.md)를 참조하세요.
