
import csv
'''
Select response will return a list of values that fit query

SELECT id, name FROM table_name
'''

def iterate_thru_reader(reader:any, column_idxs:list|None) -> list:
    result = []
    for row in reader:
        if column_idxs:
            selected_row = [row[i] for i in column_idxs]
            result.append(selected_row)
        else:
            result.append(row)
    
    return result


def SELECT(column_query: list, table_name:str) -> list|None:
    try:
        with open(f"{table_name}.csv","r") as file:
            reader = csv.reader(file)
            headers = next(reader)
            
            if column_query[0] == '*':
                column_idxs = None
            else:
                column_idxs = [headers.index(col.strip()) for col in column_query]


            return iterate_thru_reader(reader, column_idxs)
            
    except FileNotFoundError:
        print(f"Error: File '{table_name}.csv' not found.")
        return None
    except ValueError as e:
        print(f"Error: Invalid column name in {column_query}. Available columns: {headers}")
        return None
        
    