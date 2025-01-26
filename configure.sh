#!/bin/bash

REPO_DIR="/home/pi/atlaspi"
BRANCH="main"
GIT_REPO="https://github.com/MitchAnderson93/atlaspi.git"

echo "Checking for internet connection..."
if ping -q -c 1 -W 1 github.com >/dev/null; then
    echo "System online... pulling the latest code from the repository."
    
    # Clone or pull the latest code
    if [ -d "$REPO_DIR" ]; then
        cd "$REPO_DIR" || exit
        git fetch origin $BRANCH
        git reset --hard origin/$BRANCH
        echo "Repository updated."
    else
        echo "Cloning repository..."
        git clone -b $BRANCH $GIT_REPO "$REPO_DIR"
    fi

    # Install dependencies
    echo "Installing dependencies..."
    if [ -d "/home/pi/venv" ]; then
        source /home/pi/venv/bin/activate
    else
        python3 -m venv /home/pi/venv
        source /home/pi/venv/bin/activate
    fi
    pip install --upgrade pip
    pip install -r "$REPO_DIR/requirements.txt"
else
    echo "Offline. Skipping update."
fi

# Run the main setup script
echo "Running setup.py..."
python3 "$REPO_DIR/setup.py"