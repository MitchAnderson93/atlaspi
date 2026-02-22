"""Interactive menu system for AtlasPi"""

import os
import sys
import subprocess
import logging
from utils.config import get_config_paths


def show_menu(debug_mode=False):
    """Display the main menu options"""
    print("1. Start AtlasPi Service")
    print("2. Exit")
    if debug_mode:
        print("3. View Live Logs (tail -f)")
        print("4. Clear Database & Logs")
    print("")

def get_user_choice(debug_mode=False):
    """Get and validate user menu choice"""
    max_option = 4 if debug_mode else 2
    
    while True:
        try:
            choice = input(f"\nSelect option (1-{max_option}): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= max_option:
                return int(choice)
            else:
                print(f"Invalid choice. Please enter 1-{max_option}.")
        except (KeyboardInterrupt, EOFError):
            print("\nExiting...")
            return None


def view_live_logs():
    """View live logs with tail -f, allow return to menu"""
    paths = get_config_paths()
    log_file = paths['log_path']
    
    if not os.path.exists(log_file):
        print(f"\nLog file not found: {log_file}")
        print("Run AtlasPi service first to generate logs.")
        input("Press Enter to continue...")
        return
    
    print(f"\nViewing live logs: {log_file}")
    print("Press Ctrl+C to return to menu\n")
    
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
        print("\n\nReturning to menu...")
        if process:
            process.terminate()
            process.wait()
    except FileNotFoundError:
        print("Error: 'tail' command not found. Using basic file reading...")
        # Fallback for systems without tail command
        try:
            with open(log_file, 'r') as f:
                # Go to end and read backward
                f.seek(0, 2)  # Go to end
                file_size = f.tell()
                f.seek(max(0, file_size - 1000))  # Read last 1000 chars
                content = f.read()
                print(content)
                input("Press enter to continue...")
        except Exception as e:
            print(f"Error reading log file: {e}")
            input("Press enter to continue...")


def clear_debug_files():
    """Clear database and log files"""
    paths = get_config_paths()
    files_to_remove = [paths['db_path'], paths['log_path']]
    
    print("\nClearing debug files...")
    removed_count = 0
    
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Removed {os.path.basename(file_path)}")
                removed_count += 1
            except Exception as e:
                print(f"Failed to remove {os.path.basename(file_path)}: {e}")
        else:
            print(f"{os.path.basename(file_path)} not found")
    
    print(f"\nCleared {removed_count} files.")
    input("Press enter to continue...")


def run_interactive_menu(debug_mode=False):
    """Run the interactive menu system"""
    
    while True:
        show_menu(debug_mode)
        choice = get_user_choice(debug_mode)
        
        if choice is None:  # User pressed Ctrl+C
            break
            
        elif choice == 1:
            return True  # Signal to start the main application
            
        elif choice == 2:
            return False  # Signal to exit
            
        elif choice == 3 and debug_mode:
            view_live_logs()
            
        elif choice == 4 and debug_mode:
            clear_debug_files()
    
    return False