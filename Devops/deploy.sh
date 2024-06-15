#!/bin/bash
# cd to the directory of the script CHANGE IT
mkdir /tmp/serenity
cd /tmp/serenity

# Pull the latest code
git clone https://github.com/Bend-Function/Serenity-Trail -b web-dev
cd Serenity-Trail

# Remove the old Docker container
docker rm -f serenity

# Remove the old Docker image
docker rmi serenity

# Build the Docker image
docker build -t serenity .

# Run the new Docker container
docker run -d -e TZ=Pacific/Auckland -p 5555:5555 --name serenity serenity

rm -rf /tmp/serenity

echo "---------------------------------"
echo "Deployment completed successfully"
echo "---------------------------------"

exit 0