#!/bin/bash

# Change to the directory where your docker-compose.yml file is located
cd $DOCKER_COMPOSE_PATH

# Stop and remove the Docker containers defined in the docker-compose.yml file
docker-compose down

# Check the exit code of the previous command
if [ $? -eq 0 ]; then
    # If the previous command succeeded (exit code 0), start the Docker containers
    docker-compose up -d
    
    # Check the exit code of the previous command
    if [ $? -eq 0 ]; then
        # If the previous command succeeded (exit code 0), display a success message
        echo "Docker Compose up completed successfully!"
    else
        # If the previous command failed, display an error message
        echo "Error: docker-compose up command failed"
        exit 1
    fi
else
    # If the previous command failed, display an error message
    echo "Error: docker-compose down command failed"
    exit 1
fi
