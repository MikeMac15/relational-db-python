import struct
import os
from pathlib import Path
from my_db.helpers.read_schema import read_schema
from my_db.helpers.generate_binary_format import generate_binary_format
from my_db.helpers.display_table import display_table_results
from my_db.helpers.get_db_files import get_db_idx_file

def read_db(table_name: str):
    '''
    Reads and displays all records from a .db binary file.
    '''
    db_file, _ = get_db_idx_file(table_name)

    #(1)Read the schema
    _, fields = read_schema(table_name)

    if not fields:
        print("No fields found for this table.")
        return

    #(2)Determine binary format
    binary_format = generate_binary_format(fields)
    record_size = struct.calcsize(binary_format)

    #(3)Check if file exists
    if not os.path.exists(db_file) or os.path.getsize(db_file) == 0:
        print("No records found.")
        return

    #(4)Read records
    records = []
    with open(db_file, 'rb') as file:
        while True:
            record_data = file.read(record_size)
            if not record_data:
                break  # Stop reading when file ends
            print(record_data)
            unpacked_record = struct.unpack(binary_format, record_data)
            
            # Convert bytes to strings for string fields
            record_dict = {}
            for i, field in enumerate(fields):
                if field.type == "str":
                    record_dict[field.name] = unpacked_record[i].decode("utf-8").strip("\x00")
                else:
                    record_dict[field.name] = unpacked_record[i]

            records.append(record_dict)
    

    #(5)Display records manually
    display_table_results(table_name,fields,records)