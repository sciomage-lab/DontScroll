#!/bin/bash

docker-compose down

docker volume ls

# docker volume rm dontscroll_dont_scroll_data
if docker volume ls -q | grep -q 'dontscroll_dont_scroll_data'; then
    docker volume rm dontscroll_dont_scroll_data
else
    echo "No volume dontscroll_dont_scroll_data"
fi
