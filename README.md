# Water World - Automatic watering system

## Description
Automatic watering system utilizing Raspberry Pi 4, soil moisture sensor and a water pump.

## Dependencies
    sudo apt install apt-transport-https libffi-dev libssl-dev python3-dev python3-pip

## Installing Tailscale
Add Tailscale's package signing key and repository:

    curl -fsSL https://pkgs.tailscale.com/stable/raspbian/bullseye.gpg | sudo apt-key add -
    curl -fsSL https://pkgs.tailscale.com/stable/raspbian/bullseye.list | sudo tee /etc/apt/sources.list.d/tailscale.list

Install Tailscale:

    sudo apt update && sudo apt install tailscale

Authenticate and connect your machine to your Tailscale network:

    sudo tailscale up

View your Tailscale IPv4 address:

    tailscale ip -4

## Installing Docker and Docker Compose
Download Docker installation script for Linux distributions:

    curl -fsSL https://get.docker.com -o get-docker.sh

Inspect and run the script file:

    sudo sh get-docker.sh

Add your user to docker group to run docker without root:

    sudo usermod -aG docker pi

Install Docker Compose:

    sudo pip3 install docker-compose

Enable the Docker system service to start your containers on boot:

    sudo systemctl enable docker

## Creating the .env file
Before building and running the docker-compose, you need to set these variables in .env file at the projects root to correspond to your own settings.  

    DJANGO_SUPERUSER_PASSWORD='<superuser password of your choice>'
    DJANGO_SUPERUSER_EMAIL='<superuser email of your choice>'
    DJANGO_SUPERUSER_USERNAME='<superuser username of your choice>'
    SECRET_KEY='<your django secret key from the settings.py file>'
    DEBUG="<desired debug mode True/False>"
    MONGODB_URI=<mongodb+srv://<username>:<password>@<cluster>/<database>?retryWrites=true&w=majority>
    UID='<your user id (run 'id -u' in bash)>'
    GID='<your user group id (run 'id -g' in bash)>'

## Running the Docker network
To get the network running, following commands need to be run from project's root, where docker-compose.yaml resides.  

Build images:

    docker-compose build

Run the containers up:

    docker-compose up -d

To update your changes to the containers, you need to run the containers down:

    docker-compose down

Then repeat the process of building images and running containers up again.  

To view the output of a docker container:

    docker logs -f -n 20 <name of container>

## Creating a new Django model
Make sure the changes are updated to the docker container by rebuilding the image and that the containers is up and running.  
Then to move inside the django container from bash:  

    docker exec -it water_world_gunicorn_server /bin/bash

Once inside the container, make the migrations:  

    python manage.py makemigrations
    python manage.py migrate


## Authors
Joonas Pietilä and Henna Lehtinen

