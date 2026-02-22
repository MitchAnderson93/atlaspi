import os
import sqlite3
import json
import logging
import time
from datetime import datetime
import platform  # To detect the system

# Configure logging
LOG_PATH = os.path.join(os.getcwd(), "atlaspi.log")  # Always log to current directory

logging.basicConfig(
    filename=LOG_PATH,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logging.info("Starting the AtlasPi setup script.")

# Use current directory for all paths
DB_PATH = os.path.join(os.getcwd(), "tasks.db")
CONFIG_PATH = os.path.join(os.getcwd(), "config", "default_config.json")

# Load default configuration
def load_config():
    try:
        with open(CONFIG_PATH, "r") as file:
            logging.info(f"Loading configuration from {CONFIG_PATH}")
            return json.load(file)
    except FileNotFoundError:
        logging.warning(f"Configuration file not found: {CONFIG_PATH}, using defaults")
        # Return default config if file doesn't exist
        return {
            "project_name": "atlaspi",
            "version": "1.0.0", 
            "tasks": [
                {
                    "name": "Monitor API Health",
                    "action": "check_api_health",
                    "condition_type": "time",
                    "condition_value": "00:00"
                }
            ]
        }

config = load_config()

# Initialize the SQLite database
def initialize_database():
    if not os.path.exists(DB_PATH):
        logging.info(f"Database not found. Initializing at {DB_PATH}...")
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create the tasks table
        cursor.execute("""
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            action TEXT NOT NULL,
            condition_type TEXT NOT NULL,
            condition_value TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            last_run TIMESTAMP DEFAULT NULL
        )
        """)
        logging.info("Created tasks table.")

        # Seed the database with tasks from the default config
        seed_tasks(cursor)

        conn.commit()
        conn.close()
        logging.info("Database initialized successfully.")
    else:
        logging.info("Database already exists. Skipping initialization.")

# Seed tasks from default_config.json
def seed_tasks(cursor):
    # Check if the config contains tasks
    if "tasks" in config:
        tasks = config["tasks"]
        logging.info(f"Found {len(tasks)} tasks in the configuration.")
        
        # Iterate through tasks and insert them into the database
        for task in tasks:
            try:
                logging.info(f"Inserting task: {task['name']}")
                cursor.execute("""
                INSERT INTO tasks (name, action, condition_type, condition_value)
                VALUES (?, ?, ?, ?)
                """, (task["name"], task["action"], task["condition_type"], task["condition_value"]))
                logging.info(f"Successfully seeded task: {task['name']}")
            except Exception as e:
                logging.error(f"Failed to insert task: {task['name']}. Error: {e}")
    else:
        logging.warning("No tasks found in default configuration.")

# Main process of the app
def start_app():
    logging.info("Starting the main app process...")
    print("AtlasPi is running! Press Ctrl+C to stop.")
    print(f"Logs are being written to: {LOG_PATH}")
    print(f"Database location: {DB_PATH}")
    
    try:
        loop_count = 0
        while True:
            loop_count += 1
            # Print status every 10 loops (10 seconds) so user knows it's working
            if loop_count % 6 == 1:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] AtlasPi running... (loop {loop_count})")
            
            logging.info(f"App is running. Performing periodic tasks... (loop {loop_count})")

            # Simulate a task or delay (shorter for responsiveness)
            time.sleep(10)  # Check every 10 seconds instead of 60
    except KeyboardInterrupt:
        print("\nAtlasPi shutting down...")
        logging.info("App interrupted and shutting down.")
    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"An error occurred in the main loop: {e}")

# Print ASCII art logo
def print_logo():
    try:
        logo_path = os.path.join(os.path.dirname(__file__), "config", "logo.txt")
        with open(logo_path, "r", encoding="utf-8") as f:
            logo = f.read()
        print(logo)
    except FileNotFoundError:
        print("""  
 ░▒▓██████▓▒░▒▓████████▓▒░▒▓█▓▒░       ░▒▓██████▓▒░ ░▒▓███████▓▒░      ░▒▓███████▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░             ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░ 
░▒▓████████▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓████████▓▒░░▒▓██████▓▒░       ░▒▓███████▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░ 
░▒▓█▓▒░░▒▓█▓▒░ ░▒▓█▓▒░   ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░       ░▒▓█▓▒░      ░▒▓█▓▒░ 
        """)
    print("=" * 80)

# Entry point
if __name__ == "__main__":
    try:
        print_logo()
        print("AtlasPi Application Starting...")
        
        # Run database initialization once at startup
        initialize_database()

        # Start the main application loop
        start_app()
    except Exception as e:
        print(f"Startup error: {e}")
        logging.error(f"An unexpected error occurred: {e}")