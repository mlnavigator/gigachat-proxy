#!/bin/bash
echo "start"
docker stop gigachat_proxy
docker rm gigachat_proxy
docker rmi gigachat_proxy
docker build -t gigachat_proxy .
docker run -d --restart=always -p 8078:8078 -v ./assets/:/proxy-app/assets/ --name=gigachat_proxy gigachat_proxy
echo "finished - run container gigachat_proxy"