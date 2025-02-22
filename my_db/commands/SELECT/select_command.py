from pathlib import Path
import os
from my_db.helpers.read_schema import read_schema
from my_db.helpers.get_db_files import get_db_idx_file


def SELECT(table_name:str, where:dict) -> any:
    db_file, idx_file = get_db_idx_file(table_name)
    _,fields = read_schema(table_name)