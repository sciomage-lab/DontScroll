

```bash
./docker-build.sh
```

```bash
docker-compose -f ./docker-compose.yml up -d
```

## rm all <none> docker images

```
docker rmi $(docker images -f "dangling=true" -q)
```
