"""Main application logic for AtlasPi"""

import time
import logging
from datetime import datetime
from utils.common import strings
from utils.database import get_tasks, update_task_last_run


def run_application_loop(db_path, log_path, debug_mode=False, stop_flag=None):
    """Main application loop that processes tasks periodically"""
    
    logging.info(strings.SERVICE_STARTING)
    
    if debug_mode:
        logging.info(strings.PATHS_LOG_FILE.format(log_path))
        logging.info(strings.PATHS_DATABASE.format(db_path))
    
    loop_count = 0
    
    while True:
        try:
            # Check if we should stop
            if stop_flag and stop_flag.is_set():
                logging.info("Service stop requested")
                break
                
            loop_count += 1
            
            # Log status every 6 loops (1 minute) - only to log file in normal mode
            if loop_count % 6 == 1:
                if debug_mode:
                    logging.info(strings.RUNTIME_LOOP_STATUS.format(
                        datetime.now().strftime('%H:%M:%S'), loop_count
                    ))
                else:
                    logging.info(f"Running cycle #{loop_count}")
            
            # Process any scheduled tasks
            process_scheduled_tasks(db_path)
            
            # Only log to file in normal mode
            logging.debug(strings.SERVICE_LOOP.format(loop_count))

            # TODO: Add actual task processing here
            # For now, just simulate periodic work
            time.sleep(10)  # Check every 10 seconds
            
        except KeyboardInterrupt:
            logging.info("Service interrupted by Ctrl+C")
            break
        except Exception as e:
            logging.error(strings.SERVICE_ERROR.format(e))
            # Continue running but wait a bit before retrying
            time.sleep(5)
            
    logging.info("AtlasPi service stopped")


def process_scheduled_tasks(db_path):
    """Check and execute any scheduled tasks"""
    try:
        tasks = get_tasks(db_path)
        current_time = datetime.now()
        
        for task in tasks:
            task_id, name, action, condition_type, condition_value, is_active, last_run = task
            
            if should_execute_task(current_time, condition_type, condition_value, last_run):
                logging.info(f"Executing task: {name}")
                execute_task_action(action, name)
                update_task_last_run(db_path, task_id)
                
    except Exception as e:
        logging.error(f"Error processing scheduled tasks: {e}")


def should_execute_task(current_time, condition_type, condition_value, last_run):
    """Determine if a task should be executed based on its schedule"""
    if condition_type == "time":
        # Convert minutes since midnight to time check
        current_minutes = current_time.hour * 60 + current_time.minute
        return current_minutes == int(condition_value)
    
    # Add other condition types here (interval, daily, etc.)
    return False


def execute_task_action(action, task_name):
    """Execute the specified task action"""
    try:
        if action == "check_api_health":
            # Placeholder for API health check
            logging.info(f"Checking API health for task: {task_name}")
            # TODO: Implement actual API health check
            
        elif action == "backup_database":
            # Placeholder for database backup
            logging.info(f"Backing up database for task: {task_name}")
            # TODO: Implement database backup
            
        else:
            logging.warning(f"Unknown action '{action}' for task: {task_name}")
            
    except Exception as e:
        logging.error(f"Failed to execute task '{task_name}': {e}")