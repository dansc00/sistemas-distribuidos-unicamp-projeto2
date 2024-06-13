# !/bin/bash

# starts container, runs the terminal and stops container at the end
docker start container2
docker exec -it container2 /bin/sh 
docker stop container2
