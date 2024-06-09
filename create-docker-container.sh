# !/bin/bash

# creates docker container, based on linux alpine image
sudo docker run -it --name $1 -v /bin/bash alpine:latest

