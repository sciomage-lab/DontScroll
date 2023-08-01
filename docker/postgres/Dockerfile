FROM debian:buster-slim

# 필요한 패키지를 설치합니다.
RUN apt-get update && apt-get install -y wget build-essential libreadline-dev zlib1g-dev flex bison libxml2-dev libxslt-dev libssl-dev

# 소스 코드를 다운로드하고 압축을 해제합니다.
WORKDIR /usr/src/postgresql
RUN wget https://ftp.postgresql.org/pub/source/v13.3/postgresql-13.3.tar.gz
RUN tar -xzf postgresql-13.3.tar.gz

# CUBE_MAX_DIM 값을 변경합니다.
WORKDIR /usr/src/postgresql/postgresql-13.3/contrib/cube
RUN sed -i 's/#define CUBE_MAX_DIM (100)/#define CUBE_MAX_DIM (512)/' cubedata.h

# PostgreSQL를 빌드합니다.
WORKDIR /usr/src/postgresql/postgresql-13.3
RUN ./configure --enable-cassert --prefix=/usr/local
RUN make world
RUN make install-world

# postgres 사용자를 추가합니다.
RUN useradd -ms /bin/bash postgres

# 환경 변수를 설정합니다.
ENV PATH="/usr/local/pgsql/bin:${PATH}"
ENV PGDATA="/var/lib/postgresql/data"

# docker-entrypoint.sh를 추가합니다.
COPY ./docker-entrypoint.sh /home/postgres/docker-entrypoint.sh
RUN chmod +x /home/postgres/docker-entrypoint.sh

# 데이터 디렉토리를 설정하고 PostgreSQL을 초기화합니다.
RUN mkdir -p "$PGDATA"
RUN chown -R postgres:postgres "$PGDATA"
USER postgres
RUN initdb

# cube 확장을 추가합니다.
RUN echo "shared_preload_libraries = 'cube'" >> /var/lib/postgresql/data/postgresql.conf

# PostgreSQL을 실행합니다.
CMD ["/home/postgres/docker-entrypoint.sh"]
