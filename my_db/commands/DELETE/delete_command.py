import struct
from my_db.helpers.get_db_files import get_db_idx_file
from my_db.helpers.binary_search_idx import binary_search_idx

def DELETE(table_name:str, where:dict) -> bool:
    """
        Deletes a record from the specified table based on the given condition.
        Args:
            table_name (str): The name of the table from which the record should be deleted.
            where (dict): A dictionary specifying the condition for deletion. Currently, only supports deletion based on the "id" key.
        Returns:
            bool: True if the record was successfully marked for deletion, False otherwise.
        Notes:
            - The function currently supports only IDX based deletion to minimize accidental deletions.
            - The record is not physically removed from the database but is marked for deletion by writing a specific flag.
        Raises:
            Exception: If any error occurs during the deletion process, it will be caught and printed.
    """
    try:
        db_file, idx_file = get_db_idx_file(table_name)

        search_id = where.get("id")
        #DELETE Error (1)
        if search_id is None:
            print('DELETE(1): currently I am only supporting IDX based deletion to minimize accidental deletions')
            return False
        
        record_start_offset = binary_search_idx(idx_file, search_id)
        
        #DELETE Error (2)
        if record_start_offset == -1:
            print('DELETE(2): record not found')
            return False
        
        with open(db_file, 'r+b') as file:
            file.seek(record_start_offset)
            file.write(struct.pack('i',1))
        
        print(f"Record{search_id} marked for deletion")
        return True
    except Exception as e:
        print('DELETE (e):',e)
