#!/bin/bash
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get auto-remove -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
docker run -d -p 9001:9001 --name portainer_agent --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v /var/lib/docker/volumes:/var/lib/docker/volumes portainer/agent:latest
echo ""
echo "$(curl -s ifconfig.me):9001"
echo ""