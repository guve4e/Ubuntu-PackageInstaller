#!/usr/bin/python3
import unittest
from unittest import TestCase, mock
from src.file import File

class FileTest(unittest.TestCase):
    def setUp(self):
        self.file_content = "Errors Off\nSomething Else Off\nSome Configuration\n[mode]"

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

        file = File("testfile.json")
        file.append("SomeText")
        # # Act

        # # Assert
        pass

    def test_preppend(self):
        # Arrange
        file = File("testfile.json")

        # # Act

        # # Assert
        pass

    def test_add(self):
        # Arrange
        file = File("testfile.json")

        # # Act

        # # Assert
        pass

    def test_change(self):
        # Arrange
        file = File("testfile.json")

        # # Act

        # # Assert
        pass

    def test_remove(self):
        # Arrange
        file = File("testfile.json")

        # # Act

        # # Assert
        pass