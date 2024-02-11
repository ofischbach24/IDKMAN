Initial Setup:

    Clone the Repository: git clone https://github.com/ofischbach24/Robocup24.git

    bash

cd Desktop
git clone https://github.com/ofischbach24/Robocup24.git

Make setup.sh Executable:

bash

cd Robocup24
chmod +x setup.sh

Run setup.sh:

bash

./setup.sh

Identify the Gamepad Event Device:

bash

    ls /dev/input/

    Look for a device named eventX. This will be used in your app2.py script.

Run app2.py:

    Make app2.py Executable:

    bash

chmod +x app2.py

Run app2.py:

bash

    ./app2.py

Optional: Configure GPIO Pins and Enable Flipper Commands:

    Configure GPIO Pins in app2.py:
    Open app2.py in a text editor and set the GPIO pins accordingly:

    python

# Update GPIO pin configurations for treads, flippers, etc.

Enable Flipper Commands:
Uncomment the relevant flipper commands in your app2.py script.

python

    # Uncomment flipper commands and inputs

Control Instructions:

    Treads Movement:
        Use the joysticks in a vertical motion (tank controls) to move the treads.

    Front Flippers (Assuming Enabled):
        Use the triggers to move the front flippers.
        Use shoulder buttons to control the direction of the front flippers (up or down).

    Rear Flippers (Assuming Enabled):
        Press the triangle button to switch to rear flipper mode.
        Use the same buttons (shoulder buttons) to control the rear flippers.

Note:

    Ensure that the connected game controller (DualShock 4) is recognized and events are captured by the script.
    Make sure to configure GPIO pins correctly for motor control.
