# Atlas

Atlas is a lightweight task management and monitoring system designed for reliability and simplicity. It provides automated task scheduling, health monitoring, and comprehensive logging capabilities with zero external dependencies.

## Features

- **Task scheduling**: Configure and execute tasks based on time conditions
- **Interactive menu system**: Enhanced terminal menu with task database viewer
- **Live log monitoring**: View application logs in real-time with tail -f functionality  
- **Task database viewer**: Inspect all configured tasks, status, and execution history
- **Debug mode**: Enhanced logging and diagnostic tools for development
- **Zero dependencies**: Uses only Python standard library for maximum compatibility
- **SQLite database**: Lightweight, embedded database for task persistence
- **Background service**: Non-blocking service operation with clean start/stop controls

## Requirements

- Python 3.7 or higher
- No external dependencies required

## Installation

### Fresh Raspberry Pi OS Lite Setup

Fresh Pi installation from a new OS image? Follow these steps:

#### 1. **Initial Pi Configuration**
```bash
# Connect to wifi (if not done during image setup)
sudo raspi-config
# Navigate to: System Options > Wireless LAN > Enter SSID and password

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y git python3 python3-pip python3-venv

# Optional: Set timezone
sudo timedatectl set-timezone Australia/Melbourne
```

#### 2. **Download AtlasPi Source**
```bash
# Clone the repository
cd ~
git clone https://github.com/MitchAnderson93/atlaspi.git
cd atlaspi
```

#### 3. **Complete Pi Setup (One Command)**
```bash
# Run the automated setup (configures everything)
chmod +x install_boot_setup.sh
./install_boot_setup.sh
```

**This configures your Pi to:**
- **Auto-start**: AtlasPi runs automatically on every boot
- **Auto-update**: Checks development branch every 30 minutes and updates if needed  
- **Easy SSH access**: Just type `atlas` to access the menu when you SSH in

#### 4. **Verify Installation**
```bash
# Check service status
sudo systemctl status atlaspi

# Access the menu
atlas
```

---

### Standard Installation (Development/Manual)

For development or manual installation without auto-start:

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd atlaspi
   ```

2. **Run the configure script**
   ```bash
   chmod +x configure.sh
   ./configure.sh
   ```

### Post-Installation Commands

After setup, you can manage AtlasPi with:
- **Access menu**: `atlas`
- **Check service**: `sudo systemctl status atlaspi`
- **View logs**: `tail -f ~/atlaspi/atlaspi.log`
- **Manual updates**: `~/atlaspi/update.sh`

---

## Updates & Development

### Manual Update Process

When you need to pull the latest code changes manually:

#### 1. **Pre-Update Steps**
```bash
# Stop service to prevent conflicts
sudo systemctl stop atlaspi

# Check for local modifications
cd ~/atlaspi
git status
```

#### 2. **Pull Updates**
```bash
# Pull latest changes
git pull origin development

# Clear Python cache (important!)
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true

# Fix script permissions (git doesn't preserve execute bits)  
chmod +x atlas configure.sh update.sh install_boot_setup.sh atlas_menu.py
```

#### 3. **Test Before Restarting Service**
```bash
# Test atlas command manually
./atlas

# Test task viewer utility
source venv/bin/activate
python3 utils/view_tasks.py
deactivate
```

#### 4. **Restart Service**
```bash
# If manual tests work, restart service
sudo systemctl start atlaspi
sudo systemctl status atlaspi

# Verify with menu
atlas
```

### Troubleshooting Updates

If you encounter issues:
```bash
# Reset to clean state
sudo systemctl stop atlaspi
git reset --hard origin/development  
chmod +x *.sh atlas
sudo systemctl start atlaspi
```

**Important:** Always stop the systemd service before manual testing to avoid dual-service conflicts.

## Usage

### Atlas Menu System

Access the AtlasPi management interface:
```bash
atlas
```

**When service is running**, you get an interactive menu with options to:
- **View database tasks** - See all configured tasks and their status
- **Check service status** - Detailed systemd service information  
- **View live logs** - Real-time log monitoring with tail -f
- **Restart service** - Clean service restart with status verification
- **Stop service** - Gracefully stop the background service
- **Exit** - Return to shell

**When service is stopped**, atlas automatically starts an interactive debug session.

### Basic Operation

Start Atlas with the interactive menu (if service not running):
```bash
python3 setup.py
```

### Debug Mode

Run with enhanced logging and debugging features:
```bash
python3 setup.py --debug
```

### Menu Options

**Normal Mode:**
- Start/Stop Atlas service
- Exit application

**Debug Mode (additional options):**
- View live logs with tail -f
- Clear database and log files
- Enhanced diagnostic output

## Configuration

Atlas uses a JSON configuration file located at `config/default_config.json`. Tasks can be configured with:

- **name**: Task identifier
- **action**: Action to execute
- **condition_type**: When to run (e.g., "time")
- **condition_value**: Specific condition parameters
- **is_active**: Enable/disable task

Example configuration:
```json
{
  "tasks": [
    {
      "name": "Monitor API Health",
      "action": "check_api_health",
      "condition_type": "time",
      "condition_value": 480,
      "is_active": true
    }
  ]
}
```

## File Structure

```
atlaspi/
├── setup.py                   # Main application entry point
├── atlas                      # CLI management interface (bash launcher)
├── atlas_menu.py             # Python menu system with ASCII art
├── configure.sh              # Initial setup script
├── update.sh                 # Auto-update script
├── install_boot_setup.sh     # Complete Pi deployment script
├── config/
│   └── default_config.json   # Task configuration
├── utils/
│   ├── app.py                # Core application logic
│   ├── config.py             # Configuration management
│   ├── database.py           # SQLite database operations
│   ├── logging_config.py     # Logging setup
│   ├── menu.py              # Interactive menu system
│   ├── ui.py                # User interface components
│   ├── view_tasks.py        # Database task viewer utility
│   └── common/
│       └── strings.py        # Centralized text constants
└── tests/                    # Unit tests
```

## Development

### Running Tests

Execute the test suite:
```bash
python -m unittest discover tests
```

### Debug Mode Features

When running with `--debug` flag:
- Verbose console logging
- Automatic cleanup of database and log files on startup  
- Additional menu options for file management
- Real-time log viewing capabilities

### Logging

Atlas creates detailed logs in `atlaspi.log`. In normal mode, only important information is displayed in the console, while debug mode shows comprehensive diagnostic information.

## Support

For issues, feature requests, or questions, please refer to the project documentation or contact the development team. 