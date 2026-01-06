"""
Error handling utilities for TinyDB tool.

This module provides unified error handling functions for consistent
error reporting across the application.
"""

import sys


def handle_error(msg: str) -> None:
    """
    Handle and display error messages in a consistent format.
    
    Args:
        msg: Error message string to display.
    """
    print(f"Error: {msg}", file=sys.stderr)
