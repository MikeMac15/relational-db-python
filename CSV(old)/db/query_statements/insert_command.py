import csv
import os

def get_last_line(file_name)->list:
    with open(f"{file_name}", "rb") as file:
        file.seek(-2, os.SEEK_END)  # Move to second-last byte
        
        max_iterations = 1000  # Safety limit to prevent infinite loops
        iterations = 0

        while iterations < max_iterations:
            char = file.read(1)
            if char == b"\n":  # Found the last newline
                break
            file.seek(-2, os.SEEK_CUR)  # Move back 2 bytes
            iterations += 1
            result = file.readline().decode().strip()  # Read last line
            
            return result



def INSERT(values:list,table_name:str) -> int:
    print(table_name)
    try:
        last_line_idx = int(get_last_line(table_name)[0])

        with open(f'{table_name}.csv', 'r+', newline='') as file:
            reader = csv.reader(file)
            try:
                header = next(reader)  # Read the first row as headers
            except StopIteration:
                print(f"Error: {table_name}.csv is empty. Cannot insert data.")
                return -1
            file.seek(0,2)
            writer = csv.writer(file)
            if len(values) == len(header)-1:
                values.insert(0,last_line_idx+1)
                writer.writerow(values)
            else: 
                return -1
    except FileNotFoundError:
        print(f"Error: File '{table_name}.csv' not found.")
        return -1
    except ValueError as e:
        print(e)
        return -1