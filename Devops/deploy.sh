#!/bin/bash
# cd to the directory of the script CHANGE IT
cd ./

# Pull the latest code
git pull

# Build the Docker image
docker build -t serenity .

# Remove the old Docker container
docker rm -f serenity

# Remove the old Docker image
docker rmi serenity

# Run the new Docker container
docker run -d --name serenity serenity
