# !/bin/bash

# starts container, runs the terminal and stops container at the end
sudo docker start container3
sudo docker exec -it container3 /bin/sh 
sudo docker stop container3
