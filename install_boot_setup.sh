#!/bin/bash
# AtlasPi Complete Setup Script for Raspberry Pi Boot Configuration

set -e  # Exit on any error

# Make this script executable
chmod +x "$0" 2>/dev/null || true

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Configuration
REPO_DIR="$HOME/atlaspi"
SERVICE_NAME="atlaspi"
UPDATE_INTERVAL="*/30 * * * *"  # Every 30 minutes

print_status "Starting AtlasPi Boot Setup..."

# 1. Make scripts executable
print_status "Setting up script permissions..."
chmod +x configure.sh
chmod +x update.sh
chmod +x atlas

# 2. Run initial configuration if needed
if [ ! -d "$REPO_DIR/env" ]; then
    print_status "Running initial configuration..."
    ./configure.sh
fi

# 3. Install systemd service
print_status "Installing systemd service..."
sudo cp atlaspi.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
print_success "Service installed and enabled for boot"

# 4. Set up cron job for automatic updates
print_status "Setting up automatic updates..."
(crontab -l 2>/dev/null | grep -v "atlaspi.*update.sh"; echo "$UPDATE_INTERVAL $REPO_DIR/update.sh >/dev/null 2>&1") | crontab -
print_success "Automatic updates configured (every 30 minutes)"

# 5. Set up SSH convenience
print_status "Setting up SSH convenience features..."

# Add atlas alias to .bashrc if not already there
if ! grep -q "alias atlas=" ~/.bashrc 2>/dev/null; then
    echo "# AtlasPi convenience alias" >> ~/.bashrc
    echo "alias atlas='$REPO_DIR/atlas'" >> ~/.bashrc
    print_success "Added 'atlas' command alias"
else
    print_warning "Atlas alias already exists in .bashrc"
fi

# Add atlas to PATH
if ! grep -q "atlaspi.*atlas" ~/.bashrc 2>/dev/null; then
    echo "export PATH=\"\$PATH:$REPO_DIR\"" >> ~/.bashrc
    print_success "Added AtlasPi to PATH"
fi

# Make atlas globally accessible
sudo ln -sf $REPO_DIR/atlas /usr/local/bin/atlas 2>/dev/null || true

# 6. Create log directory and set permissions
sudo mkdir -p /var/log
sudo touch /var/log/atlaspi.log
sudo chown $USER:$USER /var/log/atlaspi.log

# 7. Start the service
print_status "Starting AtlasPi service..."
sudo systemctl start $SERVICE_NAME

# Wait a moment and check status
sleep 2
if systemctl is-active --quiet $SERVICE_NAME; then
    print_success "AtlasPi service is running!"
else
    print_error "Failed to start AtlasPi service. Check logs with: journalctl -u $SERVICE_NAME"
    exit 1
fi

print_success "AtlasPi boot setup completed!"
echo ""
echo "================== SETUP COMPLETE =================="
echo ""
print_status "Your Raspberry Pi is now configured to:"
echo "  ✓ Run AtlasPi automatically on every boot"
echo "  ✓ Check for updates from main branch every 30 minutes"
echo "  ✓ Allow easy menu access via SSH"
echo ""
print_status "Available commands:"
echo "  • atlas               - Access the AtlasPi menu"
echo "  • sudo systemctl status atlaspi    - Check service status" 
echo "  • sudo systemctl stop atlaspi     - Stop the service"
echo "  • sudo systemctl start atlaspi    - Start the service"
echo "  • tail -f /var/log/atlaspi.log    - View update logs"
echo ""
print_status "The service will start automatically on next reboot!"
print_warning "Remember to reboot or run 'source ~/.bashrc' to use the new alias"