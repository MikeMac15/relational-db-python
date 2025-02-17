
from db.table import execute_query, Table, load_from_file

def main():
    # club_table = Table('clubs',['id','name','type','distance'])
    # execute_query("INSERT into clubs VALUES 1 Dr DRIVER 280", club_table)
    # execute_query("INSERT into clubs VALUES 2 3w WOOD 260", club_table)
    # execute_query("INSERT into clubs VALUES 3 4hyb HYBRID 230", club_table)

    # # execute_query("SELECT * FROM clubs", club_table)
    # club_table.save_to_file()

    
    # club_table2 = load_from_file('clubs')

    execute_query("SELECT id, type, name, distance FROM clubs")
    # club_table2.display_table()



if __name__ == "__main__":
    main()