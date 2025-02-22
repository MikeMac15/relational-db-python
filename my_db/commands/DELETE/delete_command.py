from my_db.helpers.get_db_files import get_db_idx_file
def DELETE(table_name:str, where:dict):
    db_file, idx_file = get_db_idx_file(table_name)

    search_id = where.get("id")
    #DELETE Error (1)
    if search_id is None:
        print('currently I am only supporting IDX based deletion to minimize accidental deletions: DELETE(1)')
        return
    
    record_start_offset = binary_search_idx(table_name, idx)
    #DELETE Error (2)
    if record_start_offset == -1:
        print('record not found: DELETE(2)')
        return
    
    with open(db_file)