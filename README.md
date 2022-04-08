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

## Running the Docker network
To get the network running, following commands need to be run from project's root, where docker-compose.yaml resides.  

Build images:

    docker-compose build

Run the containers up:

    docker-compose up

To update your changes to the containers, you need to run the containers down:

    docker-compose down

Then repeat the process of building images and running containers up again.

## Usage
Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Support
Tell people where they can go to for help. It can be any combination of an issue tracker, a chat room, an email address, etc.

## Roadmap
If you have ideas for releases in the future, it is a good idea to list them in the README.

## Contributing
State if you are open to contributions and what your requirements are for accepting them.

For people who want to make changes to your project, it's helpful to have some documentation on how to get started. Perhaps there is a script that they should run or some environment variables that they need to set. Make these steps explicit. These instructions could also be useful to your future self.

You can also document commands to lint the code or run tests. These steps help to ensure high code quality and reduce the likelihood that the changes inadvertently break something. Having instructions for running tests is especially helpful if it requires external setup, such as starting a Selenium server for testing in a browser.

## Authors and acknowledgment
Show your appreciation to those who have contributed to the project.

## License
For open source projects, say how it is licensed.

## Project status
If you have run out of energy or time for your project, put a note at the top of the README saying that development has slowed down or stopped completely. Someone may choose to fork your project or volunteer to step in as a maintainer or owner, allowing your project to keep going. You can also make an explicit request for maintainers.
