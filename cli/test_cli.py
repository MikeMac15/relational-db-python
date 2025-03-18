import unittest
from unittest.mock import patch, MagicMock
from cli.cli import list_tables, view_table, cli_create_table, cli_delete

class TestCLI(unittest.TestCase):

    @patch('builtins.print')
    @patch('cli.cli.DB_DIR.glob')
    def test_list_tables(self, mock_glob, mock_print):
        mock_glob.return_value = [MagicMock(stem='table1'), MagicMock(stem='table2')]
        list_tables()
        mock_print.assert_any_call("\nAvailable Tables:")
        mock_print.assert_any_call(" - table1")
        mock_print.assert_any_call(" - table2")

    @patch('builtins.input', side_effect=['0'])
    @patch('cli.cli.cli_select', return_value=[{'id': 1, 'name': 'test'}])
    @patch('cli.cli.print_data')
    @patch('builtins.print')
    @patch('cli.cli.DB_DIR.glob')
    def test_view_table(self, mock_glob, mock_print, mock_print_data, mock_cli_select, mock_input):
        mock_glob.return_value = [MagicMock(stem='table1')]
        view_table()
        mock_print.assert_any_call("\nAvailable Tables:")
        mock_print.assert_any_call("0 - table1")
        mock_print_data.assert_called_once_with([{'id': 1, 'name': 'test'}])

    @patch('builtins.input', side_effect=['test_table', 'y', 'name', 'str', '50', 'n', 'y', '', 'n'])
    @patch('cli.cli.create_table', return_value="Table created successfully!")
    @patch('builtins.print')
    def test_cli_create_table(self, mock_print, mock_create_table, mock_input):
        cli_create_table()
        mock_create_table.assert_called_once()
        mock_print.assert_called_with('\n Table created successfully!')

    @patch('builtins.input', side_effect=['test_table', '1'])
    @patch('cli.cli.DELETE', return_value=True)
    @patch('builtins.print')
    def test_cli_delete(self, mock_print, mock_delete, mock_input):
        cli_delete()
        mock_delete.assert_called_once_with('test_table', {'id': 1})
        mock_print.assert_called_with("\nRecord deleted successfully!")

if __name__ == '__main__':
    unittest.main()