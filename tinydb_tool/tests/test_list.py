import os
import pytest
import tempfile
from pathlib import Path
from tinydb import TinyDB
from io import StringIO
import sys


class TestListCommand:
    @pytest.fixture
    def temp_db_with_data(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            db_path = f.name
        
        db = TinyDB(db_path)
        sample_docs = [
            {'name': 'Alice', 'age': 30, 'city': 'New York'},
            {'name': 'Bob', 'age': 25, 'city': 'Los Angeles'},
            {'name': 'Charlie', 'age': 35, 'city': 'Chicago'}
        ]
        db.insert_multiple(sample_docs)
        db.close()
        
        yield db_path, sample_docs
        
        if os.path.exists(db_path):
            os.remove(db_path)
    