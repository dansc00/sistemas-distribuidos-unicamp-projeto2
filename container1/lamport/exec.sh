# !/bin/bash

# inicia container, executa script python e encerra
docker start container1
docker exec -it container1 /usr/bin/python3 /lamport/node1.py 
docker stop container1

