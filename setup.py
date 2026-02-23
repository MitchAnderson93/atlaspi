"""AtlasPi Application Entry Point"""

import logging
import argparse
from utils.config import load_config, get_config_paths
from utils.logging_config import setup_logging
from utils.database import initialize_database
from utils.app import run_application_loop
from utils.menu import run_interactive_menu
from utils.common import strings


def main():
    """Main entry point for AtlasPi application"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='AtlasPi Task Management System')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode with verbose logging')
    parser.add_argument('--service', action='store_true', help='Run as background service (non-interactive)')
    args = parser.parse_args()
    
    try:
        # Get configuration paths
        paths = get_config_paths()
        
        # Clean up files in debug mode
        if args.debug:
            cleanup_debug_files(paths)
        
        # Setup logging with debug mode
        setup_logging(paths['log_path'], debug_mode=args.debug)
        
        if args.service:
            # Run as background service (non-interactive)
            logging.info("Starting AtlasPi in service mode")
            logging.info(f"Config path: {paths['config_path']}")
            config = load_config(paths['config_path'])
            logging.info(f"Config loaded: {type(config)}, content: {config}")
            logging.info(f"About to initialize database with db_path: {paths['db_path']}")
            initialize_database(paths['db_path'], config)
            logging.info("Database initialized successfully")
            run_application_loop(paths['db_path'], paths['log_path'], debug_mode=args.debug)
        else:
            # Run interactive menu (this now handles everything internally)
            run_interactive_menu(debug_mode=args.debug)
        
    except Exception as e:
        logging.error(strings.APP_STARTUP_ERROR.format(e))


def cleanup_debug_files(paths):
    """Remove existing database and log files for fresh debug run"""
    import os
    files_to_remove = [paths['db_path'], paths['log_path']]
    
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"DEBUG: Removed {file_path}")


if __name__ == "__main__":
    main()