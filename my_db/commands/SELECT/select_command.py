import os
import struct
from pathlib import Path
from my_db.helpers.read_schema import read_schema
from my_db.helpers.get_db_files import get_db_idx_file
from my_db.helpers.generate_binary_format import generate_binary_format
from my_db.helpers.binary_search_idx import binary_search_idx

def unpack_record(data, fields):
    """
    Converts unpacked binary data into a dictionary based on field types.
    """
    return {
        fields[i-1].name: 
        (data[i].decode('utf-8').rstrip('\x00') if fields[i-1].type == 'str' else data[i])
        for i in range(1, len(fields) + 1)
    }

def SELECT(table_name: str, where: dict | None = None) -> list:
    db_file, idx_file = get_db_idx_file(table_name)
    _, fields = read_schema(table_name)

    # SELECT Error (1): Invalid schema
    if not fields:
        print('SELECT(1): invalid schema / no fields')
        return []

    binary_format = generate_binary_format(fields)
    record_size = struct.calcsize(binary_format)

    # SELECT Error (2): Table does not exist or is empty
    if not os.path.exists(db_file) or os.path.getsize(db_file) == 0:
        print("SELECT(2): Table is empty or does not exist")
        return []

    results = []
    if where:
        search_id = where.get('id')
        if search_id:
            record_start_offset = binary_search_idx(idx_file, search_id)
            if record_start_offset is not None:
                with open(db_file, 'rb') as file:
                    file.seek(record_start_offset, os.SEEK_SET)
                    chunk = file.read(record_size)
                    if not chunk:
                        return []

                    data = struct.unpack(binary_format, chunk)
                    deletion_flag = data[0]

                    # Handle deleted records
                    if deletion_flag == 1:
                        if where.get('show_deleted'):
                            results.append(unpack_record(data, fields))
                            return results
                        print('Record has been previously deleted')
                        return []

                    # If record matches, return it
                    record = unpack_record(data, fields)
                    if all(record.get(k).lower() == v for k, v in where.items()):
                        results.append(record)
                    return results

    # Full Table Scan
    with open(db_file, 'rb') as file:
        while chunk := file.read(record_size):
            data = struct.unpack(binary_format, chunk)
            deletion_flag = data[0]

             # Skip deleted records
            if deletion_flag == 1:
                continue 

            record = unpack_record(data, fields)

            # Apply `where` condition filtering
            if where:
                if all(record.get(k) == v for k, v in where.items()):
                    results.append(record)
            else:
                results.append(record)

    return results
