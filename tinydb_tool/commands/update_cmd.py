import json
from tinydb_tool.shared.db_utils import load_database
from tinydb_tool.shared.error import handle_error
from tinydb_tool.commands.query_cmd import parse_and_build_query


def execute_update_command(file_path: str, string_to_query: str, data_string: str) -> int:
    """
    Execute the update command to modify documents in the database.
    
    Args:
        file_path: Path to the TinyDB JSON database file.
        string_to_query: Query condition string to match documents for update.
        data_string: JSON string containing the fields and values to update.
        
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
        
        # Parse and validate update data
        try:
            update_data = json.loads(data_string)
            if not isinstance(update_data, dict):
                handle_error("Update data must be a JSON object (dict), not an array or other type")
                return 1
        except json.JSONDecodeError as e:
            handle_error(f"Invalid JSON format in update data: {str(e)}")
            return 1
        except Exception as e:
            handle_error(f"Error parsing update data: {str(e)}")
            return 1
        
        # Load database
        try:
            db = load_database(file_path)
        except (FileNotFoundError, PermissionError, ValueError) as e:
            # Errors are already handled in load_database
            return 1
        
        # Update matching documents
        try:
            db.update(update_data, query_condition)
        except Exception as e:
            handle_error(f"Failed to update documents: {str(e)}")
            db.close()
            return 1
        
        db.close()
        return 0
        
    except Exception as e:
        handle_error(f"Unexpected error while updating documents: {str(e)}")
        return 1

