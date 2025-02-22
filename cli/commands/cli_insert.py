from my_db.helpers.read_schema import read_schema
from my_db.commands.INSERT.insert_command import INSERT

def cli_insert():
    """CLI interface for inserting a record."""
    table_name = input("\nEnter table name: ").strip()
    _, fields = read_schema(table_name)

    if not fields:
        print(f"\n Table '{table_name}' does not exist.")
        return
    
    values = {}
    for field in fields:
        if field.name == 'id':
            continue
        value = input(f"Enter value for '{field.name}' (Type: {field.type}): ").strip()
        
        if value == "" and field.default is not None:
            values[field.name] = field.default
        elif value == "" and not field.nullable:
            print(f"\n'{field.name}' cannot be NULL")
            return
        elif field.type == "int":
            values[field.name] = int(value)
        else:
            values[field.name] = value
    
    new_id = INSERT(values, table_name)
    if new_id != -1:
        print(f"\nRecord inserted successfully with ID {new_id}")
    else:
        print("\nError inserting record.")