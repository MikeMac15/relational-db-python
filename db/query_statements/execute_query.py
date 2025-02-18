from db.query_statements.select_command import SELECT
from db.query_statements.insert_command import INSERT

def execute_query(query:str) -> bool|int:
    tokens = query.strip().split()
    if not tokens:
        return False
    
    command = tokens[0].upper()

    
    if command == "INSERT": 
        if tokens[1].upper() != "INTO" or tokens[3].upper() != "VALUES":
            print("invalid query syntax: Table.py / 56")
            return False
        
        values = tokens[4:]
        return INSERT(values, tokens[2])
    
    elif command == "SELECT":
        '''
        SELECT * FROM {table.name}
        '''
        col_names = []
        
        for token in tokens[1:]:
            if token.upper() == "FROM":
                break
            col_names.append(token.strip().rstrip(','))  # Strip spaces & remove trailing commas

        table_name = tokens[-1]  # Must change to allow for secondary commands like where. # Find new way to get table name out of query
        return SELECT(col_names, table_name)


        
    else:
        print("Not implimented yet or wrong command: table.py / 69")
        return False

    return True

