
from db.query_statements.execute_query import execute_query
from db.table import load_from_file
from db.query_statements.insert_command import get_last_line

def main():
    # club_table = Table('clubs',['id','name','type','distance'])
    # execute_query("INSERT INTO clubs VALUES 1 Dr DRIVER 280", club_table)
    # execute_query("INSERT INTO clubs VALUES 2 3w WOOD 260", club_table)
    # execute_query("INSERT INTO clubs VALUES 3 4hyb HYBRID 230", club_table)
    # execute_query("INSERT INTO clubs VALUES 4 4i IRON 215")


    # # execute_query("SELECT * FROM clubs", club_table)
    # club_table.save_to_file()

    print(execute_query('INSERT INTO clubs VALUES 5i IRON 195'))
    club_table2 = load_from_file('clubs')
    # print(club_table2.num_of_rows)
    clubs = execute_query("SELECT id, name FROM clubs")
    clubs2 = execute_query("SELECT * FROM clubs")
    print(clubs)
    print(clubs2)
    club_table2.display_table()

    print(get_last_line('clubs.csv'))



if __name__ == "__main__":
    main()