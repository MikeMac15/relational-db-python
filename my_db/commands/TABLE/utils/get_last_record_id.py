import os
import struct
from utils.generate_binary_format import generate_binary_format
from commands.TABLE.read_schema import read_schema
from pathlib import Path



def get_last_record_id(file_name:str)->int:
    '''
    reads last record id from binary .db file
    '''

    _, fields = read_schema(file_name)
    if not fields:
        return -1

    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
    DB_DIR = BASE_DIR / 'databases'
    db_file = os.path.join(DB_DIR, f"{file_name}.db")

    try:
        with open(db_file,'rb') as file:
            record_size = struct.calcsize(generate_binary_format())
            if record_size == 0:
                return 0
            
            file.seek(-record_size, os.SEEK_END) # move to last record
            last_record = file.read(record_size)

            primary_key_field = next((field for field in fields if field.unique), None)
            if not primary_key_field:
                return 0
            
            unpacked_record = struct.unpack(generate_binary_format(fields), last_record)
            return unpacked_record[0] # first field being the primary key

    except:
        pass