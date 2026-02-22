"""Interactive menu system for AtlasPi"""

import os
import sys
import subprocess
import logging
import threading
import time
from utils.config import get_config_paths
from utils.config import load_config
from utils.database import initialize_database
from utils.app import run_application_loop
from utils.common import strings

# Global service state
service_thread = None
service_running = False
stop_service_flag = threading.Event()


def show_menu(debug_mode=False):
    """Display the main menu options"""
    global service_running
    
    if service_running:
        print(strings.MENU_SERVICE_RUNNING)
        print(f"1. {strings.MENU_STOP_SERVICE}")
        print(f"2. {strings.MENU_VIEW_LOGS}")
        print(f"3. {strings.MENU_EXIT}")
        if debug_mode:
            print(f"4. {strings.MENU_CLEAR_FILES}")
    else:
        print(strings.MENU_SERVICE_STOPPED)
        print(f"1. {strings.MENU_START_SERVICE}")
        print(f"2. {strings.MENU_EXIT}")
        if debug_mode:
            print(f"3. {strings.MENU_VIEW_LOGS}")
            print(f"4. {strings.MENU_CLEAR_FILES}")
    
    print("="*50)

def get_user_choice(debug_mode=False):
    """Get and validate user menu choice"""
    global service_running
    
    if service_running:
        max_option = 4 if debug_mode else 3
    else:
        max_option = 4 if debug_mode else 2
    
    while True:
        try:
            choice = input(strings.SELECT_OPTION.format(max_option)).strip()
            if choice.isdigit() and 1 <= int(choice) <= max_option:
                return int(choice)
            else:
                print(strings.INVALID_CHOICE.format(max_option))
        except (KeyboardInterrupt, EOFError):
            print(f"\n{strings.EXITING}")
            return None


def view_live_logs():
    """View live logs with tail -f, allow return to menu"""
    paths = get_config_paths()
    log_file = paths['log_path']
    
    if not os.path.exists(log_file):
        print(f"\n{strings.LOG_FILE_NOT_FOUND.format(log_file)}")
        print(strings.RUN_SERVICE_FOR_LOGS)
        input(strings.PRESS_ENTER_CONTINUE)
        return
    
    print(f"\n{strings.VIEWING_LIVE_LOGS.format(log_file)}")
    print(f"{strings.PRESS_CTRL_C_RETURN}\n")
    
    try:
        # Use subprocess to run tail -f
        process = subprocess.Popen(
            ['tail', '-f', log_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Read and display output until interrupted
        while True:
            output = process.stdout.readline()
            if output:
                print(output.rstrip())
            elif process.poll() is not None:
                break
                
    except KeyboardInterrupt:
        print(f"\n\n{strings.RETURNING_TO_MENU}")
        if process:
            process.terminate()
            process.wait()
    except FileNotFoundError:
        print(strings.TAIL_NOT_FOUND)
        # Fallback for systems without tail command
        try:
            with open(log_file, 'r') as f:
                # Go to end and read backward
                f.seek(0, 2)  # Go to end
                file_size = f.tell()
                f.seek(max(0, file_size - 1000))  # Read last 1000 chars
                content = f.read()
                print(content)
                input(strings.PRESS_ENTER_CONTINUE)
        except Exception as e:
            print(strings.ERROR_READING_LOG.format(e))
            input(strings.PRESS_ENTER_CONTINUE)


def clear_debug_files():
    """Clear database and log files"""
    paths = get_config_paths()
    files_to_remove = [paths['db_path'], paths['log_path']]
    
    print(f"\n{strings.CLEARING_DEBUG_FILES}")
    removed_count = 0
    
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(strings.REMOVED_FILE.format(os.path.basename(file_path)))
                removed_count += 1
            except Exception as e:
                print(strings.FAILED_TO_REMOVE.format(os.path.basename(file_path), e))
        else:
            print(strings.FILE_NOT_FOUND.format(os.path.basename(file_path)))
    
    print(f"\n{strings.CLEARED_FILES_COUNT.format(removed_count)}")
    input(strings.PRESS_ENTER_CONTINUE)


def start_service_background(db_path, log_path, debug_mode=False):
    """Start the AtlasPi service in a background thread"""
    global service_running, stop_service_flag
    
    def service_wrapper():
        global service_running
        try:
            service_running = True
            logging.info(strings.APP_STARTING)
            run_application_loop(db_path, log_path, debug_mode, stop_service_flag)
        except Exception as e:
            logging.error(f"Service error: {e}")
        finally:
            service_running = False
    
    stop_service_flag.clear()
    thread = threading.Thread(target=service_wrapper, daemon=True)
    thread.start()
    return thread


def stop_service_background():
    """Stop the background AtlasPi service"""
    global service_thread, service_running, stop_service_flag
    
    if service_running and service_thread:
        print(f"\n{strings.STOPPING_SERVICE}")
        stop_service_flag.set()
        service_thread.join(timeout=5)
        service_running = False
        print(strings.SERVICE_STOPPED)
        time.sleep(1)
    else:
        print(strings.SERVICE_NOT_RUNNING)


def run_interactive_menu(debug_mode=False):
    """Run the interactive menu system"""
    global service_thread, service_running
    
    # Initialize paths and config here since we're not exiting to setup.py
    paths = get_config_paths()
    config = load_config(paths['config_path'])
    
    try:
        while True:
            show_menu(debug_mode)
            choice = get_user_choice(debug_mode)
            
            if choice is None:  # User pressed Ctrl+C
                break
                
            # Handle menu choices based on service state
            if not service_running:
                # Service is stopped
                if choice == 1:  # Start service
                    print(f"\n{strings.STARTING_SERVICE_BG}")
                    initialize_database(paths['db_path'], config)
                    service_thread = start_service_background(paths['db_path'], paths['log_path'], debug_mode)
                    time.sleep(1)  # Give service time to start
                    print(strings.SERVICE_STARTED)
                    
                elif choice == 2:  # Exit
                    break
                    
                elif choice == 3 and debug_mode:  # View logs
                    view_live_logs()
                    
                elif choice == 4 and debug_mode:  # Clear files
                    clear_debug_files()
                    
            else:
                # Service is running
                if choice == 1:  # Stop service
                    stop_service_background()
                    
                elif choice == 2:  # View logs
                    view_live_logs()
                    
                elif choice == 3:  # Exit
                    stop_service_background()
                    break
                    
                elif choice == 4 and debug_mode:  # Clear files (stop service first)
                    stop_service_background()
                    clear_debug_files()
                    
    except KeyboardInterrupt:
        print(f"\n{strings.SHUTTING_DOWN}")
        if service_running:
            stop_service_background()
    
    return False  # Always return False since we handle everything internally now