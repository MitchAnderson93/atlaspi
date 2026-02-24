#!/usr/bin/env python3
"""Quick task viewer for AtlasPi database"""

import sys
import os
import sqlite3
from datetime import datetime

def format_last_run(timestamp_str):
    """Format last run timestamp for display"""
    if not timestamp_str:
        return "Never"
    
    try:
        timestamp = datetime.fromisoformat(timestamp_str)
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return "Invalid"

def view_tasks():
    """Display all tasks from the database in a formatted table"""
    
    # Get the database path
    db_path = os.path.join(os.getcwd(), "tasks.db")
    
    if not os.path.exists(db_path):
        print("Database not found at: " + db_path)
        print("Make sure you're running from the AtlasPi directory.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tasks (active and inactive)
        cursor.execute("SELECT id, name, action, condition_type, condition_value, is_active, last_run FROM tasks ORDER BY id")
        tasks = cursor.fetchall()
        conn.close()
        
        if not tasks:
            print("No tasks found in database")
            print("Tasks will be created from config/default_config.json when service starts.")
            return
        
        print("AtlasPi Task Database")
        print("=" * 80)
        print(f"{'ID':<4} {'Status':<8} {'Name':<25} {'Action':<20} {'Last Run':<20}")
        print("-" * 80)
        
        for task in tasks:
            task_id, name, action, condition_type, condition_value, is_active, last_run = task
            status = "Active" if is_active else "Inactive"
            last_run_formatted = format_last_run(last_run)
            
            # Truncate long names/actions for display
            name_display = name[:24] + "..." if len(name) > 24 else name
            action_display = action[:19] + "..." if len(action) > 19 else action
            
            print(f"{task_id:<4} {status:<8} {name_display:<25} {action_display:<20} {last_run_formatted:<20}")
        
        print("-" * 80)
        print(f"Total tasks: {len(tasks)}")
        
        # Show condition details
        print("\nTask Details:")
        for task in tasks:
            task_id, name, action, condition_type, condition_value, is_active, last_run = task
            print(f"  [{task_id}] {name}")
            print(f"      Condition: {condition_type} = {condition_value}")
            print(f"      Action: {action}")
            if last_run:
                print(f"      Last run: {format_last_run(last_run)}")
            print()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    view_tasks()