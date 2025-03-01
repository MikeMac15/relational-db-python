from my_db.commands.SELECT.select_command import SELECT
from my_db.helpers.read_schema import read_schema

def cli_select():
    """CLI interface for selecting records."""
    table_name = input("\nEnter table name: ").strip()
    select_all = input(f'Select all from {table_name}?')
    if select_all == 'y':
        results = SELECT(table_name)
    else:
        _,fields = read_schema(table_name)
        if not fields:
            return
        for field in fields:
            print(field.name)
        where = {}
        while True:
            column = input('Enter column name: ')
            value = input('Enter search value: ')
            where[column.lower()] = value.lower()
            again = input('Add another where? (y/n): ')
            if again.lower() == 'n':
                break
        results = SELECT(table_name, where)

    if not results:
        print("\nNo records found.")
        return
    
    print("\n🔍 Records Found:")
    for record in results:
        print(record)
