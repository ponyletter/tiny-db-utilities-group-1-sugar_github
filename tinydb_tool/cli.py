"""
CLI utilities for TinyDB tool.

This module provides functions for setting up command-line argument parsing
using argparse.
"""

import argparse


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the main argument parser for tinydb-tool.
    
    Returns:
        Configured ArgumentParser instance with subcommands.
    """
    # Create the main parser
    parser = argparse.ArgumentParser(
        prog='tinydb-tool',
        description='A suite of command-line tools for manipulating TinyDB database files.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Create subparsers for commands
    subparsers = parser.add_subparsers(
        dest='command',
        help='Available commands',
        metavar='COMMAND'
    )
    
    # Add 'list' subcommand
    list_parser = subparsers.add_parser(
        'list',
        help='List all documents in a TinyDB database file',
        description='Display all documents in the specified TinyDB database file.'
    )
    
    # Add required --file argument for list command
    list_parser.add_argument(
        '--file',
        type=str,
        required=True,
        help='Path to the TinyDB JSON database file'
    )
    
    # Add --no-pretty flag to disable pretty printing (default is True)
    list_parser.add_argument(
        '--no-pretty',
        action='store_false',
        dest='pretty',
        default=True,
        help='Disable pretty formatting (compact output). Default is pretty formatting enabled.'
    )
    
    # Add 'insert' subcommand
    insert_parser = subparsers.add_parser(
        'insert',
        help='Insert documents into a TinyDB database file',
        description='Add one or more documents to the specified TinyDB database file. Documents can be provided either as a JSON string via --data or read from a file via --file-input.'
    )
    
    # Add required --file argument for insert command
    insert_parser.add_argument(
        '--file',
        type=str,
        required=True,
        help='Path to the TinyDB JSON database file'
    )
    
    # Create mutually exclusive group for data input methods
    data_group = insert_parser.add_mutually_exclusive_group(required=True)
    
    data_group.add_argument(
        '--data',
        type=str,
        help='JSON string to insert. Can be a single object (e.g., \'{"name": "john"}\') or an array of objects (e.g., \'[{"name": "john"}, {"name": "jane"}]\')'
    )
    
    data_group.add_argument(
        '--file-input',
        type=str,
        dest='file_input',
        help='Path to a JSON file containing the data to insert. The file should contain a single JSON object or an array of JSON objects'
    )
    
    # Add 'query' subcommand
    query_parser = subparsers.add_parser(
        'query',
        help='Query documents in a TinyDB database file',
        description='Search for documents in the database that match the specified query condition. Returns all matching documents.'
    )
    
    # Add required --file argument for query command
    query_parser.add_argument(
        '--file',
        type=str,
        required=True,
        help='Path to the TinyDB JSON database file'
    )
    
    # Add required --where argument for query command
    query_parser.add_argument(
        '--where',
        type=str,
        required=True,
        help='Query condition in the format "field == value", "field != value", '
             '"field > value", "field < value", "field >= value", or "field <= value". '
             'String values can be quoted with single or double quotes (e.g., \'name == "john"\'). '
             'Numeric values can be written directly (e.g., \'age > 25\'). '
             'Numeric operators (>, <, >=, <=) require numeric values. '
             'Examples: \'name == "john"\', \'age != 30\', \'age > 25\', \'price <= 100\''
    )
    
    # Add --no-pretty flag to disable pretty printing (default is True)
    query_parser.add_argument(
        '--no-pretty',
        action='store_false',
        dest='pretty',
        default=True,
        help='Disable pretty formatting (compact output). Default is pretty formatting enabled.'
    )
    
    # Add 'delete' subcommand
    delete_parser = subparsers.add_parser(
        'delete',
        help='Delete documents from a TinyDB database file',
        description='Remove documents from the database that match the specified query condition. '
                   'This operation permanently deletes matching documents.'
    )
    
    # Add required --file argument for delete command
    delete_parser.add_argument(
        '--file',
        type=str,
        required=True,
        help='Path to the TinyDB JSON database file'
    )
    
    # Add required --where argument for delete command
    delete_parser.add_argument(
        '--where',
        type=str,
        required=True,
        help='Query condition in the format "field == value", "field != value", '
             '"field > value", "field < value", "field >= value", or "field <= value". '
             'String values can be quoted with single or double quotes (e.g., \'name == "john"\'). '
             'Numeric values can be written directly (e.g., \'age > 25\'). '
             'Numeric operators (>, <, >=, <=) require numeric values. '
             'Examples: \'name == "john"\', \'age != 30\', \'age > 25\', \'price <= 100\''
    )
    
    # Add 'update' subcommand
    update_parser = subparsers.add_parser(
        'update',
        help='Update documents in a TinyDB database file',
        description='Update documents in the database that match the specified query condition. '
                   'The --data argument specifies the fields and values to update.'
    )
    
    # Add required --file argument for update command
    update_parser.add_argument(
        '--file',
        type=str,
        required=True,
        help='Path to the TinyDB JSON database file'
    )
    
    # Add required --where argument for update command
    update_parser.add_argument(
        '--where',
        type=str,
        required=True,
        help='Query condition in the format "field == value", "field != value", '
             '"field > value", "field < value", "field >= value", or "field <= value". '
             'String values can be quoted with single or double quotes (e.g., \'name == "john"\'). '
             'Numeric values can be written directly (e.g., \'age > 25\'). '
             'Numeric operators (>, <, >=, <=) require numeric values. '
             'Examples: \'name == "john"\', \'age != 30\', \'age > 25\', \'price <= 100\''
    )
    
    # Add required --data argument for update command
    update_parser.add_argument(
        '--data',
        type=str,
        required=True,
        help='JSON object string containing the fields and values to update. '
             'Only the specified fields will be updated in matching documents. '
             'Example: \'{"status": "inactive", "updated_at": "2024-01-01"}\''
    )
    
    return parser


def parse_args(args: list[str] | None = None) -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Args:
        args: Optional list of arguments to parse. If None, uses sys.argv.
        
    Returns:
        Parsed arguments as a Namespace object.
    """
    parser = create_parser()
    return parser.parse_args(args)
