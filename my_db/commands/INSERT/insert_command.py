import struct
import os
from pathlib import Path
from my_db.helpers.get_last_record_id import get_last_record_id
from my_db.helpers.generate_binary_format import generate_binary_format
from my_db.helpers.read_schema import read_schema
from my_db.helpers.get_db_files import get_db_idx_file

def INSERT(values: dict, table_name: str) -> int:
    """
    Inserts a new record into the .db binary file and updates the index file.

    Returns:
        int: The ID of the inserted record, or -1 if an error occurs.
    """

    # Get file paths
    db_file, idx_file = get_db_idx_file(table_name)
    
    # Read table schema
    _, fields = read_schema(table_name)

    # INSERT Error (1): Invalid schema
    if not fields:
        print('INSERT(1): Not a valid schema, no fields found')
        return -1  # Error code

    # Find last record ID
    last_id = get_last_record_id(table_name)

    # Create new record
    new_record = {}
    for field in fields:
        field_name = field.name

        # Auto-increment 'id' field if it's unique
        if field_name == 'id' and field.unique:
            new_record[field_name] = last_id + 1
            continue

        # Assign provided values
        if field_name in values:
            new_record[field_name] = values[field_name]

        # Assign default values if not provided
        elif field.default is not None:
            new_record[field_name] = field.default

        # INSERT Error (2): Ensure non-nullable fields have values
        elif not field.nullable:
            print(f'INSERT(2): Column {field_name} is not nullable')
            return -1

        else:
            new_record[field_name] = None  # Assign None to nullable fields

    # Pack new record data in binary format
    packed_data = [0]  # 0 = active / 1 = flagged for deletion

    for field in fields:
        value = new_record[field.name]

        if field.type == 'int':
            packed_data.append(int(value) if value is not None else 0)

        elif field.type == 'str':
            max_size = getattr(field, "max_size", 255)  # Default max size if not defined
            encoded_value = (value if value is not None else "").encode("utf-8")
            packed_data.append(encoded_value.ljust(max_size, b'\x00'))

    # Store packed data
    binary_format = generate_binary_format(fields)
    
    with open(db_file, 'ab') as file:
        record_offset = file.tell()  # Retrieve byte offset before writing
        file.write(struct.pack(binary_format, *packed_data))

    # Store ID and offset in idx file
    with open(idx_file, 'ab') as idx:
        idx.write(struct.pack('ii', new_record['id'], record_offset))  
        # 'ii' = 2 ints: (1) new record ID, (2) byte offset in the .db file

    return new_record["id"]