# !/bin/bash

# cria container docker, baseado na imagem linux alpine, na rede dockernet 
# configura ip estático e volume compartilhado para o container
docker run --net dockernet --ip $1 -v recursos:/recursos -it --name $2 alpine:latest /bin/sh

