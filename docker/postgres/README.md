
## Build cube-postgres image

Build postgres:13
```bash
docker build -t cube-postgres:13 .
```

## run docker-compose
```bash
docker-compose up -d

docker-compose down
```

## Connect pgadmin

- URL : 127.0.0.1:8080
- mail : dont@scroll.com
- pw : secret

- localhost : postgresql
- user : dont_scroll
- pw : passwd

## docker volume

```bash
docker volume ls
docker volume inspect {VOLUME NAME}
docker volume rm [VOLUME_NAME]
docker volume rm postgres_pgadmin_data
docker volume rm postgres_postgresql_data
docker volume prune
```

