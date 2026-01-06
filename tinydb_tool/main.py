"""
Main entry point for TinyDB tool.

This module provides the command-line interface entry point that parses
arguments and dispatches to the appropriate command handlers.
"""

import sys
from tinydb_tool.cli import parse_args
from tinydb_tool.commands.list_cmd import execute_list_command
from tinydb_tool.commands.insert_cmd import execute_insert_command
from tinydb_tool.commands.query_cmd import execute_query_command
from tinydb_tool.commands.delete_cmd import execute_delete_command
from tinydb_tool.commands.update_cmd import execute_update_command
from tinydb_tool.shared.error import handle_error


def main() -> int:
    """
    Main entry point for the tinydb-tool CLI.
    
    Parses command-line arguments and executes the appropriate command.
    
    Returns:
        Exit code: 0 for success, 1 for error.
    """
    try:
        # Parse command-line arguments
        args = parse_args()
        
        # Check if a command was provided
        if not args.command:
            # No command specified, show help
            parse_args(['--help'])
            return 1
        
        # Dispatch to the appropriate command handler
        if args.command == 'list':
            return execute_list_command(
                file_path=args.file,
                pretty=args.pretty
            )
        elif args.command == 'insert':
            return execute_insert_command(
                db_path=args.file,
                data=getattr(args, 'data', None),
                file_input=getattr(args, 'file_input', None)
            )
        elif args.command == 'query':
            return execute_query_command(
                file_path=args.file,
                string_to_query=args.where,
                pretty=args.pretty
            )
        elif args.command == 'delete':
            return execute_delete_command(
                file_path=args.file,
                string_to_query=args.where
            )
        elif args.command == 'update':
            return execute_update_command(
                file_path=args.file,
                string_to_query=args.where,
                data_string=args.data
            )
        else:
            handle_error(f"Unknown command: {args.command}")
            return 1
            
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nOperation cancelled by user.", file=sys.stderr)
        return 130  # Standard exit code for SIGINT
    except Exception as e:
        handle_error(f"Unexpected error: {str(e)}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
