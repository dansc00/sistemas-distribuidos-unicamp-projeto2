# !/bin/bash

# creates docker container, based on linux alpine image 
#and configuring static ip
docker run --net dockernet --ip $1 -it --name $2 alpine:latest /bin/sh

