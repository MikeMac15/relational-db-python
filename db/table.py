import csv
import os

from db.query_statements.select_command import SELECT

class Table:
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns
        self.rows = []
        self.num_of_rows = 0
    
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
        table.num_of_rows = len(table.rows)
    
    return table

# Read/Writes

