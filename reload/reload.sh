#!/bin/bash
sudo docker pull greenmoon56/private:latest
sudo docker rm -f cntrains-redis
sudo docker rm -f cntrains
sudo docker run --dns 8.8.8.8 --name cntrains-redis -d redis:2.8.17
sudo docker run --dns 8.8.8.8 --name cntrains -d -p 80:80 --dns 8.8.8.8 -d --link cntrains-redis:redis greenmoon55/private:latest
