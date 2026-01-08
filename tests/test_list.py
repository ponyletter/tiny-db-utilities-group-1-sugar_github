import os
import pytest
import tempfile
from tinydb import TinyDB
from tinydb_tool.commands.list_cmd import execute_list_command
# 即使是测试，也要遵循 PEP8 规范

class TestListCommand:
    @pytest.fixture
    def temp_db_with_data(self):
        """
        Fixture: 创建一个带有临时数据的数据库文件
        """
        # 创建临时文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            db_path = f.name
        
        # 初始化数据
        db = TinyDB(db_path)
        sample_docs = [
            {'name': 'Alice', 'age': 30, 'city': 'New York'},
            {'name': 'Bob', 'age': 25, 'city': 'Los Angeles'},
            {'name': 'Charlie', 'age': 35, 'city': 'Chicago'}
        ]
        db.insert_multiple(sample_docs)
        db.close()
        
        yield db_path, sample_docs
        
        # 清理工作：删除临时文件
        if os.path.exists(db_path):
            os.remove(db_path)

    def test_list_command_execution(self, temp_db_with_data, capsys):
        """
        测试 list 命令是否能正常执行并输出内容 (Happy Path)
        """
        db_path, sample_data = temp_db_with_data
        
        # 执行 list 命令
        result_code = execute_list_command(db_path, pretty=False)
        
        # 验证 1: 返回代码应该是 0 (成功)
        assert result_code == 0
        
        # 验证 2: 捕获标准输出 (stdout)，检查是否包含了数据
        captured = capsys.readouterr()
        for doc in sample_data:
            assert doc['name'] in captured.out
            assert str(doc['age']) in captured.out