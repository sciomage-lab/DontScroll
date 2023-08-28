#!/bin/bash
set -e

# PostgreSQL 서버를 시작합니다.
pg_ctl start

# PostgreSQL 설정 파일의 listen_addresses 줄 수정
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /var/lib/postgresql/data/postgresql.conf

# 사용자가 존재하지 않을 경우, 생성하고 비밀번호를 설정합니다.
psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
    DO \$\$
    BEGIN
        IF NOT EXISTS (
            SELECT FROM pg_roles
            WHERE rolname = '$POSTGRES_USER') THEN

            CREATE ROLE $POSTGRES_USER LOGIN SUPERUSER CREATEDB PASSWORD '$POSTGRES_PASSWORD';
        ELSE
            ALTER ROLE $POSTGRES_USER WITH LOGIN SUPERUSER CREATEDB PASSWORD '$POSTGRES_PASSWORD';
        END IF;
    END
    \$\$;
 
    -- 데이터베이스 생성
    CREATE DATABASE dont_scroll_db;

    -- 사용자에게 권한 부여
    GRANT ALL PRIVILEGES ON DATABASE dont_scroll_db TO $POSTGRES_USER;
EOSQL

psql -d dont_scroll_db -v ON_ERROR_STOP=1 --username $POSTGRES_USER <<-EOSQL
    -- 활성화하는 cube 확장
    CREATE EXTENSION IF NOT EXISTS cube;

    CREATE TABLE IF NOT EXISTS public.slack_message (
        id SERIAL PRIMARY KEY,
        vector CUBE,
        client_msg_id TEXT UNIQUE, -- 고유해야 하므로 UNIQUE 제약 조건을 추가
        text TEXT,
        file_url TEXT
    );
    ALTER TABLE public.slack_message OWNER to $POSTGRES_USER;
EOSQL



echo "host all  all    0.0.0.0/0  md5" >> /var/lib/postgresql/data/pg_hba.conf

# PostgreSQL 서버를 중지합니다.
pg_ctl stop

# PostgreSQL 서버를 포그라운드에서 시작합니다.
exec postgres
