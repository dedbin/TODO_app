import unittest
from unittest import mock
from io import StringIO
from cli_main import TodoApp


class TestTodoApp(unittest.TestCase):
    def setUp(self):
        self.app = TodoApp()

    def test_create_task(self):
        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.app.onecmd('create_task Buy groceries, Buy food for dinner, 2023-08-19')
            output = fake_out.getvalue().strip()
            self.assertEqual(output, 'Задача создана успешно!')

    def test_mark_task_as_completed(self):
        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.app.onecmd('mark_task_as_completed 1')
            output = fake_out.getvalue().strip()
            self.assertEqual(output, 'Задача отмечена как выполненная!')

    def test_update_task(self):
        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.app.onecmd('update_task 1, title=New title, description=New description')
            output = fake_out.getvalue().strip()
            self.assertEqual(output, 'Задача обновлена успешно!')

    def test_delete_task(self):
        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.app.onecmd('delete_task 1')
            output = fake_out.getvalue().strip()
            self.assertEqual(output, 'Задача удалена успешно!')

    def test_exit(self):
        with mock.patch('sys.stdout', new=StringIO()) as fake_out:
            self.assertTrue(self.app.onecmd('exit'))
            output = fake_out.getvalue().strip()
            self.assertEqual(output, 'До свидания!')


if __name__ == '__main__':
    unittest.main()