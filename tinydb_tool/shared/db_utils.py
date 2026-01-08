"""
Database utilities for TinyDB tool.

This module provides functions for loading and managing TinyDB database connections.
It handles database file operations and provides a unified interface for database access.
"""

import os
from typing import TYPE_CHECKING
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb_tool.shared.error import handle_error

if TYPE_CHECKING:
    from tinydb import TinyDB as TinyDBType


def load_database(path: str) -> "TinyDBType":
    """
    Load a TinyDB database from the specified file path.
    
    This function creates a TinyDB instance using JSON storage. If the file doesn't exist,
    TinyDB will create it automatically. The function handles common errors like file
    permission issues and invalid file paths.
    
    Args:
        path: Path to the TinyDB JSON database file. The file will be created if it
              doesn't exist.
        
    Returns:
        A TinyDB database instance that can be used for database operations.
        
    Raises:
        FileNotFoundError: If the directory containing the file doesn't exist.
        PermissionError: If the file cannot be accessed due to permission issues.
        ValueError: If the file path is invalid or the file cannot be opened.
        OSError: For other file system related errors.
        
    Example:
        >>> db = load_database("data.json")
        >>> documents = db.all()
        >>> db.close()
    """
    try:
        # Create TinyDB instance with JSON storage
        # TinyDB will automatically create the file if it doesn't exist
        db = TinyDB(path, storage=JSONStorage)
        return db
    except FileNotFoundError as e:
        # Handle case where the directory doesn't exist
        handle_error(f"Directory not found for database file: {path}")
        raise
    except PermissionError as e:
        # Handle permission denied errors
        handle_error(f"Permission denied: Cannot access database file '{path}'")
        raise
    except (ValueError, OSError) as e:
        # Handle invalid paths and other OS errors
        handle_error(f"Failed to load database from '{path}': {str(e)}")
        raise
    except Exception as e:
        # Catch any other unexpected errors
        handle_error(f"Unexpected error while loading database: {str(e)}")
        raise