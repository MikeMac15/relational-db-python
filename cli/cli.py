import argparse
import json
from pathlib import Path
from my_db.classes.field_class import Field
from my_db.commands.TABLE.create_table import create_table
from my_db.commands.INSERT.insert_command import INSERT
# from my_db.commands.SELECT.select_command import SELECT
# from my_db.commands.DELETE.delete_command import DELETE
# from my_db.commands.UPDATE.update_command import UPDATE
from my_db.commands.TABLE.read_schema import read_schema  # Utility function to read schemas

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"
DB_DIR = Path(__file__).resolve().parent.parent / "databases"

def list_tables():
    """List all available tables in the database."""
    tables = [f.stem for f in SCHEMA_DIR.glob("*.schema.json")]
    if tables:
        print("\nAvailable Tables:")
        for table in tables:
            print(f" - {table}")
    else:
        print("\nNo tables found.")

def cli_create_table():
    """CLI interface for creating a table."""
    table_name = input("\nEnter table name: ").strip()
    fields = []

    print("Define fields (Type 'done' when finished).")
    while True:
        field_name = input("Field name: ").strip()
        if field_name.lower() == "done":
            break
        
        field_type = input("Field type (int/str): ").strip()
        if field_type not in ["int", "str"]:
            print("Invalid type. Use 'int' or 'str'.")
            continue
        
        max_size = None
        if field_type == "str":
            max_size = int(input("Max size: ").strip())
        
        unique = input("Unique? (y/n): ").strip().lower() == "y"
        nullable = input("Nullable? (y/n): ").strip().lower() == "y"
        default = input("Default value (press enter for none): ").strip() or None

        fields.append(Field(field_name, field_type, unique, nullable, default, max_size))

    create_table(table_name, fields)
    print(f"\n✅ Table '{table_name}' created successfully!")

def cli_insert():
    """CLI interface for inserting a record."""
    table_name = input("\nEnter table name: ").strip()
    _, fields = read_schema(table_name)

    if not fields:
        print(f"\n❌ Table '{table_name}' does not exist.")
        return
    
    values = {}
    for field in fields:
        value = input(f"Enter value for '{field.name}' (Type: {field.type}): ").strip()
        
        if value == "" and field.default is not None:
            values[field.name] = field.default
        elif value == "" and not field.nullable:
            print(f"\n❌ '{field.name}' cannot be NULL!")
            return
        elif field.type == "int":
            values[field.name] = int(value)
        else:
            values[field.name] = value
    
    new_id = INSERT(values, table_name)
    if new_id != -1:
        print(f"\n✅ Record inserted successfully with ID {new_id}!")
    else:
        print("\n❌ Error inserting record.")

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
    table_name = input("\nEnter table name: ").strip()
    record_id = input("Enter ID of record to delete: ").strip()

    # if DELETE(table_name, int(record_id)):
    #     print("\n✅ Record deleted successfully!")
    # else:
    #     print("\n❌ Record not found.")

def main():
    """CLI menu for database commands."""
    while True:
        print("\n🛠️ SimpleDB CLI 🛠️")
        print("1. Create a Table")
        print("2. Insert a Record")
        print("3. Select Records")
        print("4. Delete a Record")
        print("5. List Tables")
        print("6. Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            cli_create_table()
        elif choice == "2":
            cli_insert()
        elif choice == "3":
            cli_select()
        elif choice == "4":
            cli_delete()
        elif choice == "5":
            list_tables()
        elif choice == "6":
            print("\n👋 Exiting CLI. Goodbye!")
            break
        else:
            print("\n❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
