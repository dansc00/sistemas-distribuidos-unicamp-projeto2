# !/bin/bash

# inicia container, executa o script python e encerra
docker start container3
docker exec -it container3 /usr/bin/python3 /mutex/node3.py 
docker stop container3
