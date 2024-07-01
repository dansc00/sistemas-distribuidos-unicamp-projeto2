# !/bin/bash

# inicia container, executa o script python e encerra
docker start container2
docker exec -it container2 /usr/bin/python3 /leader_election/node2.py 
docker stop container2
