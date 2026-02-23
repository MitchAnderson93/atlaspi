#!/bin/bash
# AtlasPi Auto-Update Script

REPO_DIR="$HOME/atlaspi"  # Dynamically uses the home directory
BRANCH="development"
VENV_DIR="$REPO_DIR/env"

# Function to log with timestamp
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a /var/log/atlaspi.log
}

# Check if we're in the repo directory
if [ ! -d "$REPO_DIR" ]; then
    log_message "ERROR: AtlasPi directory not found at $REPO_DIR"
    exit 1
fi

cd "$REPO_DIR" || exit 1

# Check for internet connection
log_message "Checking internet connectivity..."
if ! ping -q -c 1 -W 1 github.com >/dev/null; then
    log_message "No internet connection. Skipping update."
    exit 0
fi

# Check for updates
log_message "Checking for updates from origin/$BRANCH..."
git fetch origin $BRANCH

# Compare local and remote versions
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/$BRANCH)

if [ "$LOCAL" = "$REMOTE" ]; then
    log_message "Already up to date."
    exit 0
fi

log_message "Updates available. Updating from $LOCAL to $REMOTE"

# Stop the service if it's running
if systemctl is-active --quiet atlaspi; then
    log_message "Stopping AtlasPi service for update..."
    sudo systemctl stop atlaspi
    RESTART_SERVICE=true
else
    RESTART_SERVICE=false
fi

# Pull the latest changes
git reset --hard origin/$BRANCH
log_message "Repository updated successfully."

# Update dependencies if requirements changed
if git diff $LOCAL..HEAD --name-only | grep -q requirements.txt; then
    log_message "Requirements updated. Installing new dependencies..."
    source "$VENV_DIR/bin/activate"
    pip install --upgrade pip
    pip install -r requirements.txt
fi

# Restart service if it was running
if [ "$RESTART_SERVICE" = true ]; then
    log_message "Restarting AtlasPi service..."
    sudo systemctl start atlaspi
fi

log_message "Update completed successfully."