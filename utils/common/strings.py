# AtlasPi Logging Messages

# Application startup messages
APP_STARTING = "AtlasPi Application Starting..."
APP_SHUTDOWN = "AtlasPi shutting down..."
APP_STARTUP_ERROR = "Startup error: {}"

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
RUNTIME_LOOP_STATUS = "[{}] AtlasPi running. #{}"