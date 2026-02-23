# Atlas

Atlas is a lightweight task management and monitoring system designed for reliability and simplicity. It provides automated task scheduling, health monitoring, and comprehensive logging capabilities with zero external dependencies.

## Features

- **Task scheduling**: Configure and execute tasks based on time conditions
- **Interactive menu system**: Simple terminal menu to control the service
- **Live log monitoring**: View application logs in real-time with tail -f functionality
- **Debug mode**: Enhanced logging and diagnostic tools for development
- **Zero dependencies**: Uses only Python standard library for maximum compatibility
- **SQLite database**: Lightweight, embedded database for task persistence
- **Background service**: Non-blocking service operation with clean start/stop controls

## Requirements

- Python 3.7 or higher
- No external dependencies required

## Installation

### Standard Installation

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

### Raspberry Pi Boot Setup 

For production Raspberry Pi deployment with auto-start and auto-update:

1. **One-time setup** (run this once on your Pi)
   ```bash
   cd atlaspi
   chmod +x install_boot_setup.sh
   ./install_boot_setup.sh
   ```

**This configures your Pi to:**
- ✅ **Auto-start**: AtlasPi runs automatically on every boot
- ✅ **Auto-update**: Checks main branch every 30 minutes and updates if needed  
- ✅ **Easy SSH access**: Just type `atlas` to access the menu when you SSH in

**After setup, you can:**
- Use `atlas` command from anywhere to access the menu
- Check service status: `sudo systemctl status atlaspi`
- View update logs: `tail -f /var/log/atlaspi.log`

### Manual Installation

2. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Operation

Start Atlas with the interactive menu:
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
├── setup.py              # Main application entry point
├── config/
│   └── default_config.json    # Task configuration
├── utils/
│   ├── app.py             # Core application logic
│   ├── config.py          # Configuration management
│   ├── database.py        # SQLite database operations
│   ├── logging_config.py  # Logging setup
│   ├── menu.py           # Interactive menu system
│   ├── ui.py             # User interface components
│   └── common/
│       └── strings.py     # Centralized text constants
└── tests/                 # Unit tests
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