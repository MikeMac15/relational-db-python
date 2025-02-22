import argparse
import json
from pathlib import Path
from my_db.classes.field_class import Field
from my_db.commands.TABLE.create_table import create_table
from my_db.commands.INSERT.insert_command import INSERT
# from my_db.commands.SELECT.select_command import SELECT
# from my_db.commands.DELETE.delete_command import DELETE
# from my_db.commands.UPDATE.update_command import UPDATE
from cli.commands.cli_insert import cli_insert
from my_db.helpers.read_db import read_db

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "my_db/schemas"
DB_DIR = Path(__file__).resolve().parent.parent / "my_db/databases"

def list_tables():
    """List all available tables in the database."""
    tables = [f.stem for f in DB_DIR.glob("*.db")]
    if tables:
        print("\nAvailable Tables:")
        for table in tables:
            print(f" - {table}")
    else:
        print("\nNo tables found.")

def view_table():
    tables = [f.stem for f in DB_DIR.glob("*.db")]
    if tables:
        print("\nAvailable Tables:")
        for t, table in enumerate(tables):
            print(f"{t} - {table}")
    idx = int(input("\nTable to view: "))
    if idx not in range(len(tables)):
        print('invalid choice')
    else:
        read_db(tables[idx])


def cli_create_table():
    """CLI interface for creating a table."""
    table_name = input("\nEnter table name: ").strip().lower()
    fields = []
    count = 1
    print("\nDefine table columns:")
    while True:
        print(f'\nColumn {count}:')
        if count == 1:
            pk = input('Make column 1 a unique primary key?(y/n): ')
            if pk.lower() == 'y':
                count += 1
                fields.append(Field('id', 'int', True, False, None))
                continue 
        column_name = input("Name: ").strip().lower()
        
        
        cloumn_type = input("Type (int/str): ").strip().lower()
        if cloumn_type not in ["int", "str"]:
            print("Invalid type. Use 'int' or 'str'.")
            continue
        
        max_size = None
        if cloumn_type == "str":
            max_size = int(input("Max size: ").strip())
        
        unique = input("Unique? (y/n): ").strip().lower() == "y"
        nullable = input("Nullable? (y/n): ").strip().lower() == "y"
        default = input("Default value (press enter for none): ").strip().lower() or None

        fields.append(Field(column_name, cloumn_type, unique, nullable, default, max_size))
        keep_going = input('\nWould you like to add another field?(y/n): ')
        if keep_going.lower() == 'n':
            break 
        count+=1

    print('\n', create_table(table_name, fields))
    



def cli_select():
    """CLI interface for selecting records."""
    table_name = input("\nEnter table name: ").strip()
    # results = SELECT(table_name)
    results = None
    if not results:
        print("\nNo records found.")
        return
    
    print("\n🔍 Records Found:")
    for record in results:
        print(record)

def cli_delete():
    """CLI interface for deleting a record."""
    table_name = input("\nEnter table name: ").strip().lower()
    record_id = int(input("Enter ID of record to delete: ").strip())

    # if DELETE(table_name, int(record_id)):
    #     print("\n✅ Record deleted successfully!")
    # else:
    #     print("\n❌ Record not found.")

def main():
    """CLI menu for database commands."""
    while True:
        print("\n🛠️ SimpleDB CLI 🛠️")
        print("(C) Create a Table")
        print("(I) Insert a Record")
        print("(S) Select Records")
        print("(D) Delete a Record")
        print("(L) List Tables")
        print("(V) View Table")
        print("(E) Exit")
        
        choice = input("\nEnter your choice: ").strip().lower()
        
        if choice == "c":
            cli_create_table()
        elif choice == "i":
            cli_insert()
        elif choice == "s":
            cli_select()
        elif choice == "d":
            cli_delete()
        elif choice == "l":
            list_tables()
        elif choice == "v":
            view_table()
        elif choice == "e":
            print("\n Exiting CLI. Goodbye!")
            break
        else:
            print("\n Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
