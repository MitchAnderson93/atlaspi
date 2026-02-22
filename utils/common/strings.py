# AtlasPi Application Constants and Logging Messages

# Application constants
APP_NAME = "Atlas"
APP_DISPLAY_NAME = "Atlas"

# Application startup messages
APP_STARTING = f"{APP_NAME} Application Starting..."
APP_SHUTDOWN = f"{APP_NAME} shutting down..."
APP_STARTUP_ERROR = "Startup error: {}"

# Menu messages
MENU_HEADER = f"{APP_DISPLAY_NAME}"
MENU_SERVICE_RUNNING = "Service status: RUNNING"
MENU_SERVICE_STOPPED = "Service status: STOPPED"
MENU_START_SERVICE = f"Start {APP_NAME} service"
MENU_STOP_SERVICE = f"Stop {APP_NAME} service"
MENU_VIEW_LOGS = "View live logs (tail -f)"
MENU_CLEAR_FILES = "Clear database & logs"
MENU_EXIT = "Exit"

# Menu interaction messages
LOG_FILE_NOT_FOUND = "Log file not found: {}"
RUN_SERVICE_FOR_LOGS = f"Run {APP_NAME} service first to generate logs."
PRESS_ENTER_CONTINUE = "Press enter to continue..."
VIEWING_LIVE_LOGS = "Viewing live logs: {}"
PRESS_CTRL_C_RETURN = "Press Ctrl+C to return to menu"
RETURNING_TO_MENU = "Returning to menu..."
TAIL_NOT_FOUND = "Error: 'tail' command not found. Using basic file reading..."
ERROR_READING_LOG = "Error reading log file: {}"
CLEARING_DEBUG_FILES = "Clearing debug files..."
REMOVED_FILE = "Removed {}"
FAILED_TO_REMOVE = "Failed to remove {}: {}"
FILE_NOT_FOUND = "{} not found"
CLEARED_FILES_COUNT = "Cleared {} files."
STARTING_SERVICE_BG = f"Starting {APP_NAME} service..."
SERVICE_STARTED = "Service started successfully"
STOPPING_SERVICE = f"Stopping {APP_NAME} service..."
SERVICE_STOPPED = "Service stopped successfully"
SERVICE_NOT_RUNNING = "Service is not running"
SHUTTING_DOWN = "Shutting down..."
EXITING = "Exiting..."
INVALID_CHOICE = "Invalid choice. Please enter 1-{}."
SELECT_OPTION = "Select option (1-{}): "

# Service status messages  
SERVICE_STARTING = "Starting the main app process..."
SERVICE_LOOP = "Task cycle #{}"
SERVICE_INTERRUPTED = "App interrupted and shutting down."
SERVICE_ERROR = "An error occurred in the main loop: {}"

# Database messages
DB_INITIALIZING = "Database not found. Initializing at {}..."
DB_TABLE_CREATED = "Created tasks table."
DB_INITIALIZED = "Database initialized successfully."
DB_EXISTS = "Database already exists. Skipping initialization."
DB_TASKS_FOUND = "Found {} tasks in the configuration."
DB_TASKS_NONE = "No tasks found in configuration. Database created with empty tasks table."
DB_TASK_INSERTING = "Inserting task: {}"
DB_TASK_SUCCESS = "Successfully seeded task: {}"
DB_TASK_ERROR = "Failed to insert task: {}. Error: {}"

# Configuration messages
CONFIG_LOADING = "Loading configuration from {}"
CONFIG_NOT_FOUND = "Configuration file not found: {}, proceeding without tasks"

# File path messages
PATHS_LOG_FILE = "Logs are being written to: {}"
PATHS_DATABASE = "Database location: {}"

# Runtime messages
RUNTIME_LOOP_STATUS = f"[{{}}] {APP_NAME} running. #{{}}"