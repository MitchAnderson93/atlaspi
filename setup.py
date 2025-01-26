import os
import sqlite3
import json
import logging
from datetime import datetime
import platform  # To detect the system

# Configure logging
if platform.system() == "Linux" and os.uname()[1] == "raspberrypi":
    LOG_PATH = "/var/log/atlaspi.log"  # Log file for Raspberry Pi
else:
    LOG_PATH = os.path.join(os.getcwd(), "atlaspi.log")  # Log file for development

logging.basicConfig(
    filename=LOG_PATH,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logging.info("Starting the AtlasPi setup script.")

# Detect if the script is running on Raspberry Pi or a development machine
if platform.system() == "Linux" and os.uname()[1] == "raspberrypi":
    # Running on Raspberry Pi
    DB_PATH = "/home/pi/atlaspi/tasks.db"
    CONFIG_PATH = "/home/pi/atlaspi/config/default_config.json"
else:
    # Running on a development machine
    DB_PATH = os.path.join(os.getcwd(), "tasks.db")
    CONFIG_PATH = os.path.join(os.getcwd(), "config", "default_config.json")

# Load default configuration
def load_config():
    try:
        with open(CONFIG_PATH, "r") as file:
            logging.info(f"Loading configuration from {CONFIG_PATH}")
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"Configuration file not found: {CONFIG_PATH}")
        return {}

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
    if "tasks" in config:
        for task in config["tasks"]:
            cursor.execute("""
            INSERT INTO tasks (name, action, condition_type, condition_value)
            VALUES (?, ?, ?, ?)
            """, (task["name"], task["action"], task["condition_type"], task["condition_value"]))
        logging.info(f"Seeded task: {task['name']}")
    else:
        logging.warning("No tasks found in default configuration.")

# Main process of the app
def start_app():
    logging.info("Starting the main app process...")
    # Placeholder for your main app logic
    # Example: process_tasks() or start a service loop
    logging.info("App is running. Ready to process tasks.")

# Entry point
if __name__ == "__main__":
    try:
        initialize_database()
        start_app()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")