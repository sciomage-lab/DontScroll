
# Outline

DontScroll provides docker for convenient deployment.

- postgres (Database for data storage)
- DontScroll (Main service)

By default, both containers must be running. Set environment variables and run `start.sh` in each directory.

# Install Docker

```
sudo apt install docker.io
sudo apt install docker-compose
```

```
sudo groupadd docker
sudo usermod -aG docker ${USER}
sudo service docker restart
# exit
```
