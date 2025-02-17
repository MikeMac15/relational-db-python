
import csv
'''
Select response will return a list of values that fit query

SELECT id, name FROM table_name
'''

def SELECT( column_query: list, table_name:str) -> list|None:
    try:
        result = []
        with open(f"{table_name}.csv","r") as file:
            reader = csv.reader(file)
            headers = next(reader)
            
            column_idxs = [headers.index(col.strip()) for col in column_query]
            print()
            print(f"Table: {table_name}")
            print("-"*40)
            print("\t".join(column_query))
            
            for row in reader:
                selected_row = [row[i] for i in column_idxs]
                result.append(selected_row)
                print("\t".join(selected_row))
            
            print()

                    
                
            return result

            
    except FileNotFoundError:
        print(f"Error: File '{table_name}.csv' not found.")
        return None
    except ValueError as e:
        print(f"Error: Invalid column name in {column_query}. Available columns: {headers}")
        return None
        
    