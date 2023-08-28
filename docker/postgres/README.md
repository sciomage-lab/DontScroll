
## Start docker

`./start.sh`
```bash
# Build postgres:13
docker build -t cube-postgres:13 .

# Start docker
docker-compose up -d
```

## Stop docker

`./stop.sh`
```bash
# Stop docker
docker-compose down

# Remove docker volume
docker volume ls
docker volume rm postgres_pgadmin_data
docker volume rm postgres_postgresql_data
```

## Connect pgadmin

- URL : 127.0.0.1:8080
- mail : dont@scroll.com
- pw : secret

- localhost : postgresql
- user : dont_scroll
- pw : secret

## docker volume

```bash
docker volume ls
docker volume inspect {VOLUME NAME}
docker volume rm [VOLUME_NAME]
docker volume rm postgres_pgadmin_data
docker volume rm postgres_postgresql_data
docker volume prune
```
