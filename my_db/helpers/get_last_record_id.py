import os
import struct
from my_db.helpers.generate_binary_format import generate_binary_format
from my_db.helpers.read_schema import read_schema
from my_db.helpers.get_db_files import get_db_idx_file


def get_last_record_id(table_name: str) -> int:
    """
    Reads the last record's primary key from a binary .db file.

    Args:
        table_name (str): Name of the table.

    Returns:
        int: The last record's primary key ID, or 0 if the table is empty or does not exist.
    """

    # Get database file path
    db_file, _ = get_db_idx_file(table_name)

    # Return 0 if the file doesn't exist or is empty
    if not os.path.exists(db_file) or os.path.getsize(db_file) == 0:
        return 0  

    # Read schema
    _, fields = read_schema(table_name)

    # Error: Schema is invalid
    if not fields:
        print('get_last_record_id: No valid schema found for', table_name)
        return 0

    # Get the primary key field (first unique field)
    primary_key_field = next((field for field in fields if field.unique), None)
    if not primary_key_field:
        print(f'get_last_record_id: No unique primary key found in {table_name}')
        return 0
    
    # Determine the binary format and record size
    binary_format = generate_binary_format(fields)
    record_size = struct.calcsize(binary_format)

    # Error: If struct size is zero, return 0
    if record_size == 0:
        print(f'get_last_record_id: Struct size is zero for {table_name}')
        return 0

    try:
        # Read the last record
        with open(db_file, 'rb') as file:
            file.seek(-record_size, os.SEEK_END)  # Move to last record
            last_record = file.read(record_size)

            # Unpack the record
            unpacked_record = struct.unpack(binary_format, last_record)

            # Find the index of the primary key field
            primary_key_index = next(i for i, field in enumerate(fields) if field == primary_key_field)

            return unpacked_record[primary_key_index+1] # [+1] because deletion flag is [0] an not in schema

    except Exception as e:
        print('get_last_record_id: Error reading last record from', table_name, '->', e)
        return 0
