#!/bin/bash

# cria rede docker
docker network create --subnet=172.18.0.0/16 dockernet
