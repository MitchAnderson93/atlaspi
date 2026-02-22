"""Configuration management for AtlasPi"""

import os
import json
import logging
from utils.common import strings


def load_config(config_path):
    """Load configuration from JSON file"""
    try:
        with open(config_path, "r") as file:
            logging.info(strings.CONFIG_LOADING.format(config_path))
            return json.load(file)
    except FileNotFoundError:
        logging.warning(strings.CONFIG_NOT_FOUND.format(config_path))
        return {}


def get_config_paths():
    """Get standardized paths for database and config"""
    current_dir = os.getcwd()
    return {
        'db_path': os.path.join(current_dir, "tasks.db"),
        'config_path': os.path.join(current_dir, "config", "default_config.json"),
        'log_path': os.path.join(current_dir, "atlaspi.log")
    }