# 0. 사전 준비 작업 & 환경 설정

```bash
. .venv/bin/activate
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
. tools/set_env.sh
```

# 1. 환경 설정

설정파일을 환경변수에 로드 할 수 있음

```bash
# 초기 상태 확인
echo $DB_HOST

# 환경변수 불러오기 & 테스트
. tools/set_env.sh
echo $DB_HOST

# 설정파일 변경 (DB_HOST 변경)
vim ~/.config/dont_scroll/config.toml

# 환경변수 불러오기 & 테스트
. tools/set_env.sh
echo $DB_HOST

# 설정파일 변경 (DB_HOST 복구)
vim ~/.config/dont_scroll/config.toml

# 환경변수 불러오기 & 테스트
. tools/set_env.sh
echo $DB_HOST
```

# 2. Docker

Docker 이미지를 빌드 할 수 있음 & 스크립트에 의해 컨테이너를 중지 및 실행할 수 있음 & 스크립트에 의해 컨테이너 리소스를 할당 및 해제할 수 있음

```bash
# 컨테이너 정지 & 컨테이너 확인 & 리소스 확인
./docker/postgres/stop.sh
docker ps -a
docker volume ls

# 컨테이너 빌드 및 실행 & 컨테이너 확인 & 리소스 확인
./docker/postgres/start.sh # 시간 소요
docker ps -a
docker volume ls

# 반복(정지 & 실행)
```

```bash
# postgres 컨테이너 확인
Web : http://xxx.xxx.xxx.xxx:8080
e-mail : dont@scroll.com
password : secret

[새 서버 추가]

localhost : postgresql
port : 5432
db : postgres
user : dont_scroll
pw : secret

[데이터베이스] -> [don’t_scroll_db] -> [스키마] -> [테이블] -> [slack_message] -> [우클릭] -> [자료 보기/편집] -> [모든 자료]
```

```bash
# 메인 프로그램은 같은 방식으로 실행 가능 하지만 
시간이 10분 이상 걸리고, 같은 방식이며, 하기 내용과 중복되기 때문에 따로 진행함
./docker/DontScroll/stop.sh
./docker/DontScroll/start.sh
```

# 3. 데이터 생성

대화 및 이미지를 다운로드 할 수 있음 & 이미지를 벡터화 할 수 있음 & 대화 및 이미지 벡터를 DB에 저장할 수 있음

```bash
# 벡터 DB 컨테이너 실행
./docker/postgres/stop.sh # 컨테이너 정지
./docker/postgres/start.sh # 컨테이너 빌드 및 실행
docker ps -a # 컨테이너 확인

# 웹페이지 pgadmin 확인

# 메시지를 다운받고 이미지 백터화, DB 저장
time python dont_scroll/slack_message_fetcher.py

# (진행 완료 후)웹페이지 pgadmin 확인
```

중복 데이터 검증하고 중복 저장을 통과할 수 있음

```bash
# (다시)메시지를 다운받고 이미지 백터화, DB 저장 -> 모두 skip
time python dont_scroll/slack_message_fetcher.py
```

쳇봇에 의해 수신한 텍스트를 벡터화 할 수 있음

```bash
# 쳇봇 실행 (최초 실행 시간 약 8코어 4분)
python dont_scroll/webhook/slack_command.py
```

# 4. 이미지 검색

벡터 DB를 검색하고 유사 이미지 URL을 반환할 수 있음

```bash
/f bird
/f ticket
```


# 5. 대화 검색

쳇봇에 의해 수신한 쿼리를 기반으로 프롬프트 템플릿을 생성할 수 있음 & 생성된 프롬프트를 프롬프팅하고 그 결과를 반환할 수 있음

```bash
/q Who is getting married?
/q Can I use room A?
```

