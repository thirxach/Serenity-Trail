#!/bin/bash
# cd to the directory of the script CHANGE IT
cd /root/wintec/Serenity-Trail/

# Pull the latest code
git pull

# Remove the old Docker container
docker rm -f serenity

# Remove the old Docker image
docker rmi serenity

# Build the Docker image
docker build -t serenity .

# Run the new Docker container
docker run -d --name serenity serenity
