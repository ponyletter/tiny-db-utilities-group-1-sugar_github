import os
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb_tool.shared.error import handle_error


def load_database(path: str):
    try:
        db = TinyDB(path, storage=JSONStorage)
        return db
    except Exception as e:
        handle_error(f"Failed to load database: {str(e)}")
        raise