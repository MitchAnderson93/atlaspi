"""Database operations for AtlasPi"""

import os
import sqlite3
import logging
from utils.common import strings


def initialize_database(db_path, config):
    """Initialize SQLite database and seed with tasks if needed"""
    if not os.path.exists(db_path):
        logging.info(strings.DB_INITIALIZING.format(db_path))
        conn = sqlite3.connect(db_path)
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
        logging.info(strings.DB_TABLE_CREATED)

        # Seed the database with tasks from config
        seed_tasks(cursor, config)

        conn.commit()
        conn.close()
        logging.info(strings.DB_INITIALIZED)
    else:
        logging.info(strings.DB_EXISTS)
        # Check if database has tasks, reseed if empty
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tasks")
        task_count = cursor.fetchone()[0]
        
        if task_count == 0:
            logging.info("Database is empty, seeding with tasks...")
            seed_tasks(cursor, config)
            conn.commit()
        
        conn.close()


def seed_tasks(cursor, config):
    """Seed database with tasks from configuration"""
    if "tasks" in config and config["tasks"]:
        tasks = config["tasks"]
        logging.info(strings.DB_TASKS_FOUND.format(len(tasks)))
        
        # Iterate through tasks and insert them into the database
        for task in tasks:
            try:
                logging.info(strings.DB_TASK_INSERTING.format(task['name']))
                cursor.execute("""
                INSERT INTO tasks (name, action, condition_type, condition_value)
                VALUES (?, ?, ?, ?)
                """, (task["name"], task["action"], task["condition_type"], task["condition_value"]))
                logging.info(strings.DB_TASK_SUCCESS.format(task['name']))
            except Exception as e:
                logging.error(strings.DB_TASK_ERROR.format(task['name'], e))
    else:
        logging.info(strings.DB_TASKS_NONE)


def get_tasks(db_path):
    """Retrieve all active tasks from database"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE is_active = 1")
    tasks = cursor.fetchall()
    conn.close()
    return tasks


def update_task_last_run(db_path, task_id):
    """Update the last_run timestamp for a task"""
    from datetime import datetime
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET last_run = ? WHERE id = ?", 
        (datetime.now().isoformat(), task_id)
    )
    conn.commit()
    conn.close()