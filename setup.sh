#!/bin/bash

# Install required Python packages
pip install pimoroni-ioexpander RPi.GPIO

# Install xinput tool
sudo apt-get install xinput

# Add user to gpio group
sudo usermod -aG gpio $USER

# Create a udev rule for correct group ownership of /dev/mem
echo 'SUBSYSTEM=="bcm2835-gpiomem", KERNEL=="gpiomem", GROUP="gpio", MODE="0660"' | sudo tee /etc/udev/rules.d/20-gpiomem.rules

echo "Setup completed successfully!"
