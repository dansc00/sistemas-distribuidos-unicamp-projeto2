# !/bin/bash

# starts container, runs the terminal and stops container at the end
docker start container3
docker exec -it container3 /bin/sh 
docker stop container3
