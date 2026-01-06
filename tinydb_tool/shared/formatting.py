"""
Formatting utilities for displaying database documents.

This module provides functions for formatting and displaying TinyDB documents
in a user-friendly way.
"""

import json
from typing import List, Dict, Any


def format_documents(documents: List[Dict[str, Any]], pretty: bool = True) -> str:
    """
    Format a list of documents for display.
    
    Args:
        documents: A list of document dictionaries from TinyDB.
        pretty: If True, format JSON with indentation. If False, use compact format.
        
    Returns:
        A formatted string representation of the documents.
    """
    if not documents:
        return "No documents found in the database."
    
    if pretty:
        return json.dumps(documents, indent=2, ensure_ascii=False)
    else:
        return json.dumps(documents, ensure_ascii=False)


def print_documents(documents: List[Dict[str, Any]], pretty: bool = True) -> None:
    """
    Print a list of documents in a formatted way.
    
    Args:
        documents: A list of document dictionaries from TinyDB.
        pretty: If True, format JSON with indentation. If False, use compact format.
    """
    formatted_output = format_documents(documents, pretty)
    print(formatted_output)

