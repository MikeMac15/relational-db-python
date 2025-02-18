import unittest
import os
import csv
from db.table import Table, load_from_file, execute_query

class TestTable(unittest.TestCase):
    def setUp(self):
        self.table = Table("test_table", ["id", "name"])
    
    def tearDown(self):
        if os.path.exists("test_table.csv"):
            os.remove("test_table.csv")
    
    def test_insert_row(self):
        self.table.insert_row(["1", "Alice"])
        self.assertEqual(len(self.table.rows), 1)
        self.assertEqual(self.table.rows[0], ["1", "Alice"])
    
    def test_insert_row_invalid(self):
        self.table.insert_row(["1"])
        self.assertEqual(len(self.table.rows), 0)  # Should not insert due to column mismatch
    
    def test_save_and_load(self):
        self.table.insert_row(["1", "Alice"])
        self.table.save_to_file()
        loaded_table = load_from_file("test_table")
        self.assertIsNotNone(loaded_table)
        self.assertEqual(loaded_table.rows, [["1", "Alice"]])
    
    def test_execute_insert_query(self):
        execute_query("INSERT INTO test_table VALUES 2 Bob", self.table)
        self.assertEqual(len(self.table.rows), 1)
        self.assertEqual(self.table.rows[0], ["2", "Bob"])
    
    def test_execute_invalid_insert_query(self):
        execute_query("INSERT test_table VALUES 3 Charlie", self.table)
        self.assertEqual(len(self.table.rows), 0)  # Should not insert due to syntax error
    
    def test_execute_select_query(self):
        self.table.insert_row(["1", "Alice"])
        execute_query("SELECT * FROM test_table", self.table)
        # This only prints, so we check for no errors (no assertion needed)
    
    def test_execute_invalid_select_query(self):
        execute_query("SELECT ALL test_table", self.table)
        # This should not crash but print an error

if __name__ == "__main__":
    unittest.main()
