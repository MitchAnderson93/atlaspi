"""User interface functions for AtlasPi"""

import os


def print_logo():
    """Print the AtlasPi ASCII art logo"""
    try:
        logo_path = os.path.join(os.path.dirname(__file__), "common", "logo.txt")
        with open(logo_path, "r", encoding="utf-8") as f:
            logo = f.read()
        print(logo)
    except FileNotFoundError:
        # Fallback if logo file is missing
        print("AtlasPi")
    print("=" * 80)