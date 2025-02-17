import csv
import os

from db.query_statements.select_command import SELECT

class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns
        self.rows = []
    
    def insert_row(self, values:list):
        if len(values) != len(self.columns):
            print('Column mismatch: Table.py / 9')
            return
        self.rows.append(values)
    
    def display_table(self):
        print(f"Table: {self.name}")
        print("\t".join(self.columns))
        print("-"*40)
        for row in self.rows:
            print("\t".join(row))
        
    def save_to_file(self):
        '''
            Creates or opens csv file and writes or overwrites file with columns and rows.
            Should this not completely overwrite the file..?
        '''
        with open(f"{self.name}.csv", "w", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(self.columns)
            writer.writerows(self.rows)

def load_from_file(table_name):
    if not os.path.exists(f"{table_name}.csv"):
        return
    table = Table(table_name,[])

    with open(f"{table_name}.csv", "r") as file:
        reader = csv.reader(file)
        table.columns = next(reader)
        table.rows = [row for row in reader]
    
    return table

# Read/Writes

def execute_query(query:str) -> bool:
    tokens = query.strip().split()
    if not tokens:
        return False
    
    command = tokens[0].upper()

    
    if command == "INSERT": 
        # if tokens[1].upper() != "INTO" or tokens[2] != table.name or tokens[3].upper() != "VALUES":
        #     print("invalid query syntax: Table.py / 56")
        #     return False
        
        values = tokens[4:]
        # table.insert_row(values)
    
    elif command == "SELECT":
        '''
        SELECT * FROM {table.name}
        '''
        col_names = []
        
        for token in tokens[1:]:
            if token.upper() == "FROM":
                break
            col_names.append(token.strip().rstrip(','))  # Strip spaces & remove trailing commas

        table_name = tokens[-1]
        SELECT(col_names, table_name)


        
    else:
        print("Not implimented yet or wrong command: table.py / 69")
        return False

    return True

