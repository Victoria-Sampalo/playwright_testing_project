#!/bin/sh

echo "**********************************************************"
echo "*** INSTALLING PYTHON VENV - PLAYWRIGHT & REQUIREMENTS ***"
echo "**********************************************************"

# Prompt user for confirmation
while true; do
    read -p "This will replace your actual venv folder 'playwright_venv' with a fresh one. Do you want to proceed? (y/n) " yn
    case $yn in 
        [yY] ) echo "Ok, we will proceed.";
            break;;
        [nN] ) echo "Exiting...";
            return 0;;  # Return to shell without closing it
        * ) echo "Invalid response. Please answer y or n.";;
    esac
done

# Deactivate virtual environment if active
if [ ! -z "$VIRTUAL_ENV" ]; then
    deactivate
fi

# Remove the existing virtual environment
if [ -d "playwright_venv" ]; then
    sudo rm -r playwright_venv
    echo "Old virtual environment 'playwright_venv' removed."
else
    echo "No existing virtual environment 'playwright_venv' found."
fi

# Update system packages
echo "Updating system packages..."
sudo apt update -y
if [ $? -ne 0 ]; then
    echo "System update failed. Please check your network connection and try again."
    return 1
fi

# Install necessary packages
echo "Installing necessary packages..."
sudo apt install -y python3-venv figlet jp2a python3-pip
if [ $? -ne 0 ]; then
    echo "Package installation failed. Please check the errors and try again."
    return 1
fi

# Create a new virtual environment
python3 -m venv playwright_venv
if [ $? -ne 0 ]; then
    echo "Failed to create virtual environment."
    return 1
fi

# Activate the virtual environment
source playwright_venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Failed to activate virtual environment."
    return 1
fi

# Upgrade pip
pip install --upgrade pip
if [ $? -ne 0 ]; then
    echo "Failed to upgrade pip."
    return 1
fi

# Install Python requirements
pip install -r requirements.txt --no-cache-dir
if [ $? -ne 0 ]; then
    echo "Failed to install requirements."
    return 1
fi

# Install Playwright browsers
playwright install
if [ $? -ne 0 ]; then
    echo "Failed to install Playwright browsers."
    return 1
fi

echo

# Display success message
figlet "PLAYWRIGHT DEMO PROJECT INSTALLED"
if [ $? -ne 0 ]; then
    echo "Failed to display installation message."
    return 1
fi

echo "Run 'pytest test_demo.py' for example test." && echo
