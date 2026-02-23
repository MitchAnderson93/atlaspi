#!/bin/bash

REPO_DIR="$HOME/atlaspi"  # Dynamically uses the home directory
BRANCH="development"             # Use main branch for production
GIT_REPO="https://github.com/MitchAnderson93/atlaspi.git"
VENV_DIR="$REPO_DIR/venv"

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
    if [ -d "$VENV_DIR" ]; then
        source "$VENV_DIR/bin/activate"
    else
        python3 -m venv "$VENV_DIR"
        source "$VENV_DIR/bin/activate"
    fi
    pip install --upgrade pip
    pip install -r "$REPO_DIR/requirements.txt"
else
    echo "System offline. Skipping update."
fi

# Run the main setup script
echo "Running setup.py..."
python3 "$REPO_DIR/setup.py"
