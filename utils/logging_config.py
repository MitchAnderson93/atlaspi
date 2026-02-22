"""Logging configuration for AtlasPi"""

import logging


def setup_logging(log_path, debug_mode=False):
    """Configure dual logging (file + console) for the application"""
    
    # Create formatters
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # File handler - always logs everything
    file_handler = logging.FileHandler(log_path, mode='a')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Console handler - different levels based on debug mode
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter('%(message)s' if not debug_mode else '%(levelname)s: %(message)s'))
    
    if debug_mode:
        console_handler.setLevel(logging.DEBUG)  # Show everything in debug mode
        root_level = logging.DEBUG
    else:
        console_handler.setLevel(logging.WARNING)  # Only show warnings/errors in normal mode
        root_level = logging.INFO

    # Configure root logger
    logging.basicConfig(level=root_level, handlers=[file_handler, console_handler])
    
    logging.info("Starting the AtlasPi setup script.")