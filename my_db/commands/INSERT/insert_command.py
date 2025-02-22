import struct
import os
from pathlib import Path
from my_db.helpers.get_last_record_id import get_last_record_id
from my_db.helpers.generate_binary_format import generate_binary_format
from my_db.helpers.read_schema import read_schema
from my_db.helpers.get_db_files import get_db_idx_file
def INSERT(values: dict, table_name: str) -> int:
    '''
    Inserts new record into .db binary file and updates index.
    '''

    #Get file paths
    db_file, idx_file = get_db_idx_file(table_name)
    #Read db schema
    _, fields = read_schema(table_name)
    if not fields:
        print('Not a valid schema: no fields found')
        return -1  # Error code

    #Find last record id
    last_id = get_last_record_id(table_name)

    #Create new record
    new_record = {}
    for field in fields:
        field_name = field.name
        if field_name == 'id' and field.unique:
            new_record[field_name] = last_id + 1
            continue
        if field_name in values:
            new_record[field_name] = values[field_name]
        elif field.default is not None:
            new_record[field_name] = field.default
        elif not field.nullable:
            print(f'Column {field_name} is not nullable')
            return -1
        else:
            new_record[field_name] = None


    #Pack new record data in binary format
    packed_data = []
    for field in fields:
        value = new_record[field.name]
        if field.type == 'int':
            packed_data.append(int(value))
        elif field.type == 'str':
            packed_data.append(value.encode("utf-8").ljust(field.max_size, b'\x00'))
    #Store packed data
    binary_format = generate_binary_format(fields)    
    with open(db_file, 'ab') as file:
        file.seek(0,os.SEEK_END)
        record_offset = file.tell() # <- retrieves the byte offset where new file is about to be written
        file.write(struct.pack(binary_format, *packed_data))

    #Store id and offset in idx file
    with open(idx_file, 'ab') as idx:
        idx.write(struct.pack('ii', new_record['id'], record_offset)) 
        # ^ writes into the idx file the location of the byte offset to allow for seeking
        # 'ii' = 2 ints
        # (1) new records id#
        # (2) byte offset where new record is stored in the .db file

    return new_record["id"]
