import unittest
import os
import json
from pathlib import Path
from my_db.commands.TABLE.create_table import create_table
from my_db.classes.field_class import Field

class TestCreateTable(unittest.TestCase):

    def setUp(self):
        self.table_name = "test_table"
        self.fields = [Field("id", "int"), Field("name", "str")]
        self.schema_dir = Path(__file__).resolve().parent.parent.parent / 'schemas'
        self.db_dir = Path(__file__).resolve().parent.parent.parent / 'databases'
        self.schema_file = self.schema_dir / f"{self.table_name}.schema.json"
        self.db_file = self.db_dir / f"{self.table_name}.db"

    def tearDown(self):
        if self.schema_file.exists():
            os.remove(self.schema_file)
        if self.db_file.exists():
            os.remove(self.db_file)

    def test_create_table_success(self):
        result = create_table(self.table_name, self.fields)
        self.assertEqual(result, f'Table {self.table_name} created successfully.')
        self.assertTrue(self.schema_file.exists())
        self.assertTrue(self.db_file.exists())

        with open(self.schema_file, 'r') as file:
            schema = json.load(file)
            self.assertEqual(schema["table_name"], self.table_name)
            self.assertEqual(len(schema["fields"]), len(self.fields))
            for i, field in enumerate(self.fields):
                self.assertEqual(schema["fields"][i], field.to_dict())

    def test_create_table_failure(self):
        # Simulate failure by passing invalid fields
        result = create_table(self.table_name, None)
        self.assertTrue("An error occurred" in result)

if __name__ == '__main__':
    unittest.main()