# !/bin/bash

# starts container, runs the terminal and stops container at the end
sudo docker start container1
sudo docker exec -it container1 /bin/sh 
sudo docker stop container1
