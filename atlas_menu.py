#!/usr/bin/env python3
"""Atlas menu launcher with systemd service awareness"""

import sys
import os
import subprocess
import time

# Add the atlaspi directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.menu import run_interactive_menu, show_menu_with_planet
from utils.config import get_config_paths
from utils.view_tasks import view_tasks
from utils.common import strings

def check_systemd_service_running():
    """Check if the atlaspi systemd service is running"""
    try:
        result = subprocess.run(['systemctl', 'is-active', '--quiet', 'atlaspi'], 
                              capture_output=True)
        return result.returncode == 0
    except:
        return False

def restart_systemd_service():
    """Restart the atlaspi systemd service"""
    try:
        print("\nRestarting AtlasPi service...")
        subprocess.run(['sudo', 'systemctl', 'restart', 'atlaspi'], check=True)
        time.sleep(2)
        
        if check_systemd_service_running():
            print("Service restarted successfully")
        else:
            print("Service failed to restart")
            subprocess.run(['sudo', 'systemctl', 'status', 'atlaspi', '--no-pager'])
        
        input("\nPress Enter to continue...")
    except subprocess.CalledProcessError as e:
        print(f"Failed to restart service: {e}")
        input("\nPress Enter to continue...")

def stop_systemd_service():
    """Stop the atlaspi systemd service"""
    try:
        print("\nStopping AtlasPi service...")
        subprocess.run(['sudo', 'systemctl', 'stop', 'atlaspi'], check=True)
        print("Service stopped")
        input("\nPress Enter to continue...")
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop service: {e}")
        input("\nPress Enter to continue...")

def show_systemd_service_status():
    """Show detailed systemd service status"""
    try:
        print()
        subprocess.run(['sudo', 'systemctl', 'status', 'atlaspi'])
        input("\nPress Enter to continue...")
    except subprocess.CalledProcessError as e:
        print(f"Failed to get service status: {e}")
        input("\nPress Enter to continue...")

def view_live_logs():
    """View live application logs"""
    try:
        repo_dir = os.path.expanduser("~/atlaspi")
        log_path = os.path.join(repo_dir, "atlaspi.log")
        
        print("\nLive logs (Press Ctrl+C to stop):")
        print("=" * 35)
        subprocess.run(['tail', '-f', log_path])
    except KeyboardInterrupt:
        print("\n")
    except Exception as e:
        print(f"Failed to view logs: {e}")
        input("\nPress Enter to continue...")

def run_systemd_aware_menu():
    """Run menu system with systemd service awareness"""
    
    systemd_service_running = check_systemd_service_running()
    
    if systemd_service_running:
        # Systemd service is running - show service management menu
        while True:
            # Show the same ASCII art header as the regular menu
            show_menu_with_planet()
            print("AtlasPi service is running in background")
            
            print("\nSelect an option:")
            print("  1. View database tasks")
            print("  2. Check service status") 
            print("  3. View live logs")
            print("  4. Restart service")
            print("  5. Stop service")
            print("  6. Exit")
            
            try:
                choice = input("\nEnter choice [1-6]: ").strip()
                
                if choice == "1":
                    print("\nCurrent Tasks in Database:")
                    print("=" * 32)
                    view_tasks()
                    input("\nPress Enter to continue...")
                    
                elif choice == "2":
                    show_systemd_service_status()
                    
                elif choice == "3":
                    view_live_logs()
                    
                elif choice == "4":
                    restart_systemd_service()
                    
                elif choice == "5":
                    stop_systemd_service()
                    # After stopping, check if we should switch to interactive mode
                    if not check_systemd_service_running():
                        print("\nSystemd service stopped. Switching to interactive mode...")
                        time.sleep(1)
                        break  # Exit this loop and fall through to interactive mode
                    
                elif choice == "6":
                    print("Goodbye!")
                    return
                    
                else:
                    print("\nInvalid choice. Please enter 1-6.")
                    
            except KeyboardInterrupt:
                print("\nGoodbye!")
                return
    
    # If systemd service is not running, use the regular interactive menu
    if not check_systemd_service_running():
        print("AtlasPi service is not running.")
        print("Starting interactive debug session...")
        print("\nPress Ctrl+C to exit and return to shell.\n")
        run_interactive_menu(debug_mode=True)

if __name__ == "__main__":
    run_systemd_aware_menu()