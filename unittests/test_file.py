#!/usr/bin/python3
import unittest
from unittest import TestCase, mock
from src.file import File


class FileTest(unittest.TestCase):
    def setUp(self):
        self.file_content = "Errors Off\nSomething Else Off\n" \
                            "Some Configuration\n[mode]\n    Some other configuration"

    def runTest(self):
        pass

    def tearDown(self):
        pass

    @mock.patch("builtins.open", create=True)
    def test_append(self, mock_open):
        # Arrange
        mock_open.side_effect = [
            mock.mock_open(read_data=self.file_content).return_value
        ]

        expected_content = self.file_content + "\nSome Appended Text"

        # Act
        file = File("testfile.json")
        file.append("Some Appended Text")

        # Assert
        self.assertEqual(expected_content, file.content)

    @mock.patch("builtins.open", create=True)
    def test_prepend(self, mock_open):
        # Arrange
        mock_open.side_effect = [
            mock.mock_open(read_data=self.file_content).return_value
        ]

        expected_content = "Some Prepended Text\n" + self.file_content

        # Act
        file = File("testfile.json")
        file.prepend("Some Prepended Text")

        # Assert
        self.assertEqual(expected_content, file.content)

    @mock.patch("builtins.open", create=True)
    def test_add(self, mock_open):
        # Arrange
        mock_open.side_effect = [
            mock.mock_open(read_data=self.file_content).return_value
        ]

        expected_content = "Errors Off\nSomething Else Off\nSome Added Text\n" \
                           "Some Configuration\n[mode]\n    Some other configuration"

        # Act
        file = File("testfile.json")
        file.add("Some Added Text", "Something Else Off")

        # Assert
        self.assertEqual(expected_content, file.content)

    @mock.patch("builtins.open", create=True)
    def test_change(self, mock_open):
        # Arrange
        mock_open.side_effect = [
            mock.mock_open(read_data=self.file_content).return_value
        ]

        expected_content = "Errors Off\nSomething Else On\n" \
                           "Some Configuration\n[mode]\n    Some other configuration"

        # Act
        file = File("testfile.json")
        file.change("Something Else Off", "Something Else On")

        # Assert
        self.assertEqual(expected_content, file.content)

    @mock.patch("builtins.open", create=True)
    def test_remove(self, mock_open):
        # Arrange
        mock_open.side_effect = [
            mock.mock_open(read_data=self.file_content).return_value
        ]

        expected_content = "Errors Off\n" \
                           "Some Configuration\n[mode]\n    Some other configuration"

        # Act
        file = File("testfile.json")
        file.remove("Something Else Off")

        # Assert
        self.assertEqual(expected_content, file.content)
