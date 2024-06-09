# !/bin/bash

# starts container, runs the terminal and stops container at the end
sudo docker start container2
sudo docker exec -it container2 /bin/sh 
sudo docker stop container2
