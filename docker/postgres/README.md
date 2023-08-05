
## Build cude-postgres image

```bash
docker build -t cude-postgres:13 .
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
docker volume prune
```

