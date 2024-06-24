# !/bin/bash

# inicia container, roda o terminal sh e para o container no fim da execução
docker start container1
docker exec -it container1 /bin/sh #/usr/bin/python3 /home/lamport/node1.py 
docker stop container1
