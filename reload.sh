#!/bin/bash
sudo docker pull greenmoon55/private:latest
docker stop cntrains
docker rm cntrains
docker run --name cntrains -d -p 80:80 greenmoon55/private:latest
