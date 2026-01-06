"""
List command implementation for TinyDB tool.

This module implements the 'list' subcommand that displays all documents
in a TinyDB database file.
"""

from tinydb_tool.shared.db_utils import load_database
from tinydb_tool.shared.formatting import print_documents


def execute_list_command(file_path: str, pretty: bool = True) -> int:
    """
    Execute the list command to display all documents in the database.
    
    Args:
        file_path: Path to the TinyDB JSON database file.
        pretty: If True, format output with indentation. Default is True.
        
    Returns:
        Exit code: 0 for success, 1 for error.
    """
    try:
        # Load the database
        db = load_database(file_path)
        
        # Retrieve all documents
        all_documents = db.all()
        
        # Print documents in formatted way
        print_documents(all_documents, pretty)
        
        # Close the database connection
        db.close()
        
        return 0
        
    except (FileNotFoundError, PermissionError, ValueError) as e:
        # Errors are already handled in load_database
        return 1
    except Exception as e:
        from tinydb_tool.shared.error import handle_error
        handle_error(f"Unexpected error while listing documents: {str(e)}")
        return 1

