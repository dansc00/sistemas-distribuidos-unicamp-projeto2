# !/bin/bash

# starts container, runs the terminal and stops container at the end
docker start container4
docker exec -it container4 /bin/sh 
docker stop container4
