# Developer Guide

This guide explains how to extend the TinyDB tool suite by adding new subcommands. It covers the project structure, shared library usage, and step-by-step instructions for implementing new commands.

## Table of Contents

- [Project Structure](#project-structure)
- [Shared Library](#shared-library)
- [Adding a New Subcommand](#adding-a-new-subcommand)
- [Best Practices](#best-practices)
- [API Reference](#api-reference)

## Project Structure

```
tinydb_tool/
├── main.py              # Entry point, dispatches to command handlers
├── cli.py               # Argument parser configuration
├── commands/            # Command implementations
│   ├── list_cmd.py
│   ├── insert_cmd.py
│   ├── query_cmd.py
│   ├── delete_cmd.py
│   └── update_cmd.py
└── shared/              # Shared library modules
    ├── db_utils.py      # Database loading utilities
    ├── error.py         # Error handling
    └── formatting.py    # Output formatting
```

## Shared Library

### Database Utilities (`shared/db_utils.py`)

**`load_database(path: str) -> TinyDB`**

Loads a TinyDB database from a file path. Handles common errors automatically.

```python
from tinydb_tool.shared.db_utils import load_database

db = load_database("data.json")
# Use db for operations
db.close()
```

**Error Handling:**
- Automatically handles `FileNotFoundError`, `PermissionError`, and `OSError`
- Errors are displayed via `handle_error()` and then re-raised

### Error Handling (`shared/error.py`)

**`handle_error(msg: str) -> None`**

Displays error messages in a consistent format to stderr.

```python
from tinydb_tool.shared.error import handle_error

try:
    # Some operation
    pass
except ValueError as e:
    handle_error(f"Invalid input: {str(e)}")
    return 1
```

**Best Practice:** Always use `str(e)` when passing exceptions to `handle_error()`.

### Formatting (`shared/formatting.py`)

**`print_documents(documents: List[Dict[str, Any]], pretty: bool = True) -> None`**

Prints documents in a formatted way. Supports pretty-printing with indentation.

```python
from tinydb_tool.shared.formatting import print_documents

documents = db.all()
print_documents(documents, pretty=True)
```

## Adding a New Subcommand

Follow these steps to add a new command to the tool suite:

### Step 1: Create Command Module

Create a new file in `commands/` directory, e.g., `commands/my_cmd.py`:

```python
"""
My command implementation for TinyDB tool.

This module implements the 'my' subcommand that performs some operation.
"""

from typing import Optional
from tinydb_tool.shared.db_utils import load_database
from tinydb_tool.shared.error import handle_error
from tinydb_tool.shared.formatting import print_documents


def execute_my_command(file_path: str, arg1: str, arg2: Optional[str] = None) -> int:
    """
    Execute the my command.
    
    Args:
        file_path: Path to the TinyDB JSON database file.
        arg1: Required argument description.
        arg2: Optional argument description.
        
    Returns:
        Exit code: 0 for success, 1 for error.
    """
    try:
        # Load database
        try:
            db = load_database(file_path)
        except (FileNotFoundError, PermissionError, ValueError) as e:
            # Errors are already handled in load_database
            return 1
        
        # Perform operations
        # ...
        
        db.close()
        return 0
        
    except Exception as e:
        handle_error(f"Unexpected error: {str(e)}")
        return 1
```

### Step 2: Add CLI Arguments

Edit `cli.py` to add your command's argument parser:

```python
# In create_parser() function, after other subcommands

my_parser = subparsers.add_parser(
    'my',
    help='Brief description of my command',
    description='Detailed description of what the command does.'
)

my_parser.add_argument(
    '--file',
    type=str,
    required=True,
    help='Path to the TinyDB JSON database file'
)

my_parser.add_argument(
    '--arg1',
    type=str,
    required=True,
    help='Description of arg1'
)

my_parser.add_argument(
    '--arg2',
    type=str,
    help='Description of optional arg2'
)
```

### Step 3: Integrate in Main

Edit `main.py` to dispatch to your command:

```python
# Add import at the top
from tinydb_tool.commands.my_cmd import execute_my_command

# Add handler in main() function
elif args.command == 'my':
    return execute_my_command(
        file_path=args.file,
        arg1=args.arg1,
        arg2=getattr(args, 'arg2', None)
    )
```

### Step 4: Test Your Command

Test your command manually:

```bash
python -m tinydb_tool.main my --file db.json --arg1 value1
```

## Best Practices

### Error Handling

1. **Use specific exception types** when possible:
   ```python
   except (FileNotFoundError, PermissionError, ValueError) as e:
       # Handle specific errors
   ```

2. **Always provide error messages**:
   ```python
   handle_error(f"Clear error message: {str(e)}")
   ```

3. **Handle errors at appropriate levels**:
   - Database loading errors: Already handled in `load_database()`
   - Command-specific errors: Handle in command function
   - Unexpected errors: Catch with descriptive message

### Code Style

1. **Type hints**: Always include type hints for function parameters and return types
2. **Docstrings**: Use Google-style docstrings for all public functions
3. **Comments**: Add comments for complex logic or non-obvious decisions
4. **Naming**: Use descriptive names following Python conventions

### Function Signatures

- Command functions should return `int` (0 for success, 1 for error)
- Use `Optional[...]` for optional parameters
- Always include `file_path: str` as the first parameter for database commands

### Database Operations

- Always close the database connection: `db.close()`
- Handle database errors appropriately
- Use try-except blocks for database operations

## API Reference

### Shared Library Functions

#### `load_database(path: str) -> TinyDB`

Loads a TinyDB database instance.

**Parameters:**
- `path`: Path to JSON database file

**Returns:** TinyDB instance

**Raises:**
- `FileNotFoundError`: Directory doesn't exist
- `PermissionError`: Permission denied
- `ValueError`, `OSError`: Invalid path or file system error

#### `handle_error(msg: str) -> None`

Displays error message to stderr.

**Parameters:**
- `msg`: Error message string

#### `print_documents(documents: List[Dict[str, Any]], pretty: bool = True) -> None`

Prints documents in formatted output.

**Parameters:**
- `documents`: List of document dictionaries
- `pretty`: If True, use indented format (default: True)

### Query Parser (`commands/query_cmd.py`)

#### `parse_and_build_query(string_to_query: str) -> Any`

Parses a query string and builds a TinyDB query condition. Can be reused by other commands.

**Parameters:**
- `string_to_query`: Query string in format "field == value" or "field != value"

**Returns:** TinyDB query condition object

**Raises:**
- `ValueError`: Invalid query format

**Example:**
```python
from tinydb_tool.commands.query_cmd import parse_and_build_query

query = parse_and_build_query('name == "john"')
results = db.search(query)
```

## Example: Complete Command Implementation

See `commands/list_cmd.py` for a simple example, or `commands/insert_cmd.py` for a more complex one with multiple input methods.

## Questions?

Refer to existing command implementations for patterns and conventions. All commands follow the same structure and use the shared library consistently.
