import json
from typing import Optional, Dict, List, Any, Union
from tinydb_tool.shared.db_utils import load_database
from tinydb_tool.shared.error import handle_error


def validate_json_data(json_str: str) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Validate and parse JSON string.
    
    Args:
        json_str: JSON string to validate and parse.
        
    Returns:
        Parsed JSON data (dict or list of dicts).
        
    Raises:
        ValueError: If JSON is invalid or doesn't match expected format.
        json.JSONDecodeError: If JSON string cannot be parsed.
    """
    try:
        data = json.loads(json_str)
        
        if not isinstance(data, (dict, list)):
            raise ValueError("JSON data must be either an object (dict) or an array of objects")
        
        if isinstance(data, list):
            if not all(isinstance(item, dict) for item in data):
                raise ValueError("All items in JSON array must be objects (dicts)")
            if len(data) == 0:
                raise ValueError("JSON array cannot be empty")
        
        return data
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {str(e)}")
    except ValueError:
        # Re-raise ValueError with our custom messages
        raise


def read_json_from_file(file_path: str) -> str:
    """
    Read JSON content from a file.
    
    Args:
        file_path: Path to the JSON file.
        
    Returns:
        JSON string content from the file.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If permission is denied to read the file.
        IOError: If there's an error reading the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        return content
        
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except PermissionError:
        raise PermissionError(f"Permission denied: Cannot read file '{file_path}'")
    except IOError as e:
        raise IOError(f"Error reading file '{file_path}': {str(e)}")


def execute_insert_command(db_path: str, data: Optional[str] = None, file_input: Optional[str] = None) -> int:
    """
    Execute the insert command to add documents to the database.
    
    Args:
        db_path: Path to the TinyDB JSON database file.
        data: JSON string to insert (if provided via --data).
        file_input: Path to JSON file to read data from (if provided via --file-input).
        
    Returns:
        Exit code: 0 for success, 1 for error.
    """
    try:
        # Read JSON data from file or use provided data
        json_str = None
        if file_input is not None:
            try:
                json_str = read_json_from_file(file_input)
            except FileNotFoundError as e:
                handle_error(str(e))
                return 1
            except PermissionError as e:
                handle_error(str(e))
                return 1
            except IOError as e:
                handle_error(str(e))
                return 1
        else:
            json_str = data
        
        # Validate and parse JSON
        try:
            parsed_data = validate_json_data(json_str)
        except ValueError as e:
            handle_error(f"Invalid JSON: {str(e)}")
            return 1

        # Load database
        try:
            db = load_database(db_path)
        except (FileNotFoundError, PermissionError, ValueError) as e:
            # Errors are already handled in load_database
            return 1
        
        # Insert data into database
        try:
            if isinstance(parsed_data, dict):
                doc_id = db.insert(parsed_data)
            else:
                doc_ids = db.insert_multiple(parsed_data)
        except Exception as e:
            handle_error(f"Failed to insert data into database: {str(e)}")
            db.close()
            return 1

        db.close()
        return 0
        
    except Exception as e:
        handle_error(f"Unexpected error while inserting documents: {str(e)}")
        return 1

