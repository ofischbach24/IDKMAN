#!/bin/bash

# Install required Python packages
pip3 install pimoroni-ioexpander 
pip3 install RPi.GPIO 
pip3 install inputs 
pip3 install colorama
pip3 install socket

#install required updates
sudo apt-get update
sudo apt-get install -y python3-pip
sudo apt-get install -y python3-evdev
sudo apt-get install -y python3-smbus

# Install xinput tool
sudo apt-get install xinput

# Add user to gpio group
sudo usermod -aG gpio $USER

# Create a udev rule for correct group ownership of /dev/mem
echo 'SUBSYSTEM=="bcm2835-gpiomem", KERNEL=="gpiomem", GROUP="gpio", MODE="0660"' | sudo tee /etc/udev/rules.d/20-gpiomem.rules

echo "Setup completed successfully!"
