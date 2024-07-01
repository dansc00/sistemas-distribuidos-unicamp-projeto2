# !/bin/bash

# inicia container, executa o script python e encerra
docker start container1
docker exec -it container1 /usr/bin/python3 /mutex/node1.py 
docker stop container1
