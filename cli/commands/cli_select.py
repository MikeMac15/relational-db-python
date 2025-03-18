from my_db.commands.SELECT.select_command import SELECT
from my_db.helpers.read_schema import read_schema

def cli_select():
    """
    CLI interface for selecting records from a database table.
    Prompts the user to enter a table name and whether to select all records
    from the table. If the user chooses to select specific records, it will
    prompt for column names and search values to build a WHERE clause.
    Returns:
        list: A list of records matching the selection criteria, or an empty
        list if no records are found.
    """
    table_name = input("\nEnter table name: ").strip()
    select_all = input(f'Select all from {table_name}? (y/n): ').lower()
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
    return results
