# !/bin/bash

# starts container, runs the terminal and stops container at the end
docker start container1
docker exec -it container1 /bin/sh 
docker stop container1
