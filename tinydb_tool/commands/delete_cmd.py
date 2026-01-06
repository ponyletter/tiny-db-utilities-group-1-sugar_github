from tinydb_tool.shared.db_utils import load_database
from tinydb_tool.shared.error import handle_error
from tinydb_tool.commands.query_cmd import parse_and_build_query


def execute_delete_command(file_path: str, string_to_query: str) -> int:
    """
    Execute the delete command to remove documents from the database.
    
    Args:
        file_path: Path to the TinyDB JSON database file.
        string_to_query: Query condition string to match documents for deletion.
        
    Returns:
        Exit code: 0 for success, 1 for error.
    """
    try:
        # Parse and build query condition
        try:
            query_condition = parse_and_build_query(string_to_query)
        except ValueError as e:
            handle_error(str(e))
            return 1
        
        # Load database
        try:
            db = load_database(file_path)
        except (FileNotFoundError, PermissionError, ValueError) as e:
            # Errors are already handled in load_database
            return 1
        
        # Remove matching documents
        try:
            db.remove(query_condition)
        except Exception as e:
            handle_error(f"Failed to delete documents: {str(e)}")
            db.close()
            return 1
        
        db.close()
        return 0
        
    except Exception as e:
        handle_error(f"Unexpected error while deleting documents: {str(e)}")
        return 1
