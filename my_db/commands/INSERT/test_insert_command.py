import unittest
from unittest.mock import patch, mock_open
from my_db.commands.INSERT.insert_command import INSERT

class TestInsertCommand(unittest.TestCase):

    @patch('my_db.commands.INSERT.insert_command.get_db_idx_file')
    @patch('my_db.commands.INSERT.insert_command.read_schema')
    @patch('my_db.commands.INSERT.insert_command.get_last_record_id')
    @patch('my_db.commands.INSERT.insert_command.generate_binary_format')
    @patch('builtins.open', new_callable=mock_open)
    def test_insert_valid_record(self, mock_open, mock_generate_binary_format, mock_get_last_record_id, mock_read_schema, mock_get_db_idx_file):
        # Mock return values
        mock_get_db_idx_file.return_value = ('test.db', 'test.idx')
        mock_read_schema.return_value = (None, [
            type('Field', (object,), {'name': 'id', 'type': 'int', 'unique': True, 'nullable': False, 'default': None}),
            type('Field', (object,), {'name': 'name', 'type': 'str', 'unique': False, 'nullable': False, 'default': None, 'max_size': 255})
        ])
        mock_get_last_record_id.return_value = 1
        mock_generate_binary_format.return_value = 'i255s'

        # Call the function
        result = INSERT({'name': 'Test Name'}, 'test_table')

        # Assertions
        self.assertEqual(result, 2)
        mock_open.assert_called_with('test.db', 'ab')


    def test_insert_invalid_schema(self, mock_open, mock_generate_binary_format, mock_get_last_record_id, mock_read_schema, mock_get_db_idx_file):
        # Mock return values
        mock_get_db_idx_file.return_value = ('test.db', 'test.idx')
        mock_read_schema.return_value = (None, [])

        # Call the function
        result = INSERT({'name': 'Test Name'}, 'test_table')

        # Assertions
        self.assertEqual(result, -1)
        mock_open.assert_not_called()


    def test_insert_non_nullable_field_missing(self, mock_open, mock_generate_binary_format, mock_get_last_record_id, mock_read_schema, mock_get_db_idx_file):
        # Mock return values
        mock_get_db_idx_file.return_value = ('test.db', 'test.idx')
        mock_read_schema.return_value = (None, [
            type('Field', (object,), {'name': 'id', 'type': 'int', 'unique': True, 'nullable': False, 'default': None}),
            type('Field', (object,), {'name': 'name', 'type': 'str', 'unique': False, 'nullable': False, 'default': None, 'max_size': 255})
        ])
        mock_get_last_record_id.return_value = 1

        # Call the function
        result = INSERT({}, 'test_table')

        # Assertions
        self.assertEqual(result, -1)
        mock_open.assert_not_called()

    def test_insert_with_default_values(self, mock_open, mock_generate_binary_format, mock_get_last_record_id, mock_read_schema, mock_get_db_idx_file):
        # Mock return values
        mock_get_db_idx_file.return_value = ('test.db', 'test.idx')
        mock_read_schema.return_value = (None, [
            type('Field', (object,), {'name': 'id', 'type': 'int', 'unique': True, 'nullable': False, 'default': None}),
            type('Field', (object,), {'name': 'name', 'type': 'str', 'unique': False, 'nullable': False, 'default': 'Default Name', 'max_size': 255})
        ])
        mock_get_last_record_id.return_value = 1
        mock_generate_binary_format.return_value = 'i255s'

        # Call the function
        result = INSERT({}, 'test_table')

        # Assertions
        self.assertEqual(result, 2)
        mock_open.assert_called_with('test.db', 'ab')

if __name__ == '__main__':
    unittest.main()