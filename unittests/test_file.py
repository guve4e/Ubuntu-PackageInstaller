#!/usr/bin/python3
import unittest
from unittest import TestCase, mock
from src.file import File
from parameterized import parameterized


class FileTest(unittest.TestCase):
    def setUp(self):
        self.file_content = "Errors Off\nSomething Else Off\n" \
                            "Some Configuration\n[mode]\n    Some other configuration"

    def runTest(self):
        self.test_add()
        self.test_append()
        self.test_prepend()
        self.test_add_when_last_element()
        self.test_add_when_multi_line_text()
        self.test_change()
        self.test_remove()
        self.test_find_text()
        self.test_line_exists()
        self.test_open_file_when_file_does_not_exist_must_throw_exception()

    def tearDown(self):
        pass

    @mock.patch("builtins.open", create=True)
    @mock.patch('os.path.exists')
    def test_append(self, file_exists, mock_open):
        # Arrange
        mock_open.side_effect = [
            mock.mock_open(read_data=self.file_content).return_value
        ]
        file_exists.return_value = True

        expected_content = self.file_content + "\nSome Appended Text"

        # Act
        file = File("testfile.json")
        file.append("Some Appended Text")

        # Assert
        self.assertEqual(expected_content, file.content)

    @mock.patch("builtins.open", create=True)
    @mock.patch('os.path.exists')
    def test_prepend(self, file_exists, mock_open):
        # Arrange
        mock_open.side_effect = [
            mock.mock_open(read_data=self.file_content).return_value
        ]
        file_exists.return_value = True

        expected_content = "Some Prepended Text\n" + self.file_content

        # Act
        file = File("testfile.json")
        file.prepend("Some Prepended Text")

        # Assert
        self.assertEqual(expected_content, file.content)

    @mock.patch("builtins.open", create=True)
    @mock.patch('os.path.exists')
    def test_add(self, file_exists, mock_open):
        # Arrange
        mock_open.side_effect = [
            mock.mock_open(read_data=self.file_content).return_value
        ]
        file_exists.return_value = True

        expected_content = "Errors Off\nSomething Else Off\nSome Added Text\n" \
                           "Some Configuration\n[mode]\n    Some other configuration"

        # Act
        file = File("testfile.json")
        file.add("Some Added Text", "Something Else Off")

        # Assert
        self.assertEqual(expected_content, file.content)

    @mock.patch("builtins.open", create=True)
    @mock.patch('os.path.exists')
    def test_add_when_last_element(self, file_exists, mock_open):
        # Arrange
        mock_open.side_effect = [
            mock.mock_open(read_data=self.file_content).return_value
        ]
        file_exists.return_value = True

        expected_content = "Errors Off\nSomething Else Off\n" \
                           "Some Configuration\n[mode]\n    Some other configuration\nSome Added Text"

        # Act
        file = File("testfile.json")
        file.add("Some Added Text", "    Some other configuration")

        # Assert
        self.assertEqual(expected_content, file.content)

    @mock.patch("builtins.open", create=True)
    @mock.patch('os.path.exists')
    def test_add_when_multi_line_text(self, file_exists, mock_open):
        # Arrange
        mock_open.side_effect = [
            mock.mock_open(read_data=self.file_content).return_value
        ]
        file_exists.return_value = True

        expected_content = "Errors Off\nSomething Else Off\n" \
                           "<Directory /var/www/>\n    Options Indexes FollowSymLinks\n" \
                           "    AllowOverride None\n" \
                           "</Directory>\n" \
                           "Some Configuration\n[mode]\n    Some other configuration"

        content_to_add = "<Directory /var/www/>\n    Options Indexes FollowSymLinks\n" \
                           "    AllowOverride None\n" \
                           "</Directory>"

        # Act
        file = File("testfile.json")
        file.add(content_to_add, "Something Else Off")

        # Assert
        self.assertEqual(expected_content, file.content)

    @mock.patch("builtins.open", create=True)
    @mock.patch('os.path.exists')
    def test_change(self, file_exists, mock_open):
        # Arrange
        mock_open.side_effect = [
            mock.mock_open(read_data=self.file_content).return_value
        ]
        file_exists.return_value = True

        expected_content = "Errors Off\nSomething Else On\n" \
                           "Some Configuration\n[mode]\n    Some other configuration"

        # Act
        file = File("testfile.json")
        file.change("Something Else Off", "Something Else On")

        # Assert
        self.assertEqual(expected_content, file.content)

    @mock.patch("builtins.open", create=True)
    @mock.patch('os.path.exists')
    def test_remove(self, file_exists, mock_open):
        # Arrange
        mock_open.side_effect = [
            mock.mock_open(read_data=self.file_content).return_value
        ]
        file_exists.return_value = True

        expected_content = "Errors Off\n" \
                           "Some Configuration\n[mode]\n    Some other configuration"

        # Act
        file = File("testfile.json")
        file.remove("Something Else Off")

        # Assert
        self.assertEqual(expected_content, file.content)

    @mock.patch("builtins.open", create=True)
    @mock.patch('os.path.exists')
    def test_line_exists(self, file_exists, mock_open):
        # Arrange
        mock_open.side_effect = [
            mock.mock_open(read_data=self.file_content).return_value
        ]
        file_exists.return_value = True

        # Act
        file = File("testfile.json")

        # Assert
        self.assertTrue(file.line_exists("[mode]"))
        self.assertFalse(file.line_exists("Some String that should not be there"))

    def test_open_file_when_file_does_not_exist_must_throw_exception(self):
        # Act
        with self.assertRaises(IOError): File("some_file_that_should_not_exists.txt")

    @mock.patch("builtins.open", create=True)
    @mock.patch('os.path.exists')
    def test_find_text(self, file_exists, mock_open):
        # Arrange
        mock_open.side_effect = [
            mock.mock_open(read_data=self.file_content).return_value
        ]
        file_exists.return_value = True

        # Act
        file = File("testfile.json")

        test_cases = [
            ("some string that is not suppose to be there", False),
            ("Some Configuration\n[mode]\n    Some other configuration", True),
        ]
        for x, output in test_cases:
            # Assert
            self.assertEqual(file.text_exists(x), output)
