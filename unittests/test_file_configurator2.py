#!/usr/bin/python3
import unittest
import os
import subprocess
from src.file_configurator import FileConfigurator
from src.json_parser import JsonParser

class ConfigurationFileTestCase(unittest.TestCase):
    def setUp(self):
        self.file = FileConfigurator(JsonParser("testjson.json"))

    def runTest(self):
        self.test_configure_change()
        self.test_configure_append()
        self.test_configure_add()
        self.test_no_add()

    @staticmethod
    def check_permission(option):
        return os.access("testjson.json", option)

    @staticmethod
    def change_permission(mode):
        subprocess.call(['chmod', mode, "testjson.json"])

    def tearDown(self):
        # delete everything first
        open('testfile.txt', 'w').close()

        # write everything back
        with open('testfile.txt', 'w') as file:
            file.writelines("Errors Off\n")
            file.writelines("Something Else Off\n")
            file.writelines("Appended Line\n")

        list_of_lines = []

        with open('testfile.txt') as fin:
            for line in fin:
                list_of_lines.append(line)

        self.change_permission('444')

    def test_configure_change(self):
        # Act
        self.file.configure_change()
        list_of_lines = []

        with open('testfile.txt') as fin:
            for line in fin:
                list_of_lines.append(line)

        # Assert
        self.assertEqual("Errors On\n", list_of_lines[0])
        self.assertEqual("Something Else On\n", list_of_lines[1])
        self.assertEqual(True, self.check_permission(os.O_RDONLY))

        # Clean Up
        self.tearDown()

    def test_configure_append(self):

        # Act
        self.file.configure_append()
        list_of_lines = []

        with open('testfile.txt') as fin:
            for line in fin:
                list_of_lines.append(line)

        # Assert
        self.assertEqual("Line 1\n", list_of_lines[3])
        self.assertEqual("Line 2 # Comment 2\n", list_of_lines[4])
        self.assertEqual(True, self.check_permission(os.O_RDONLY))

        # Clean Up
        self.tearDown()

    def test_configure_add(self):

        # Act
        self.file.configure_add()
        list_of_lines = []

        with open('testfile.txt') as fin:
            for line in fin:
                list_of_lines.append(line)

        # Assert
        self.assertEqual("Insert in the middle 1 # Comment 1\n", list_of_lines[1])
        self.assertEqual("Insert in the middle 2 # Comment 2\n", list_of_lines[3])
        self.assertEqual(True, self.check_permission(os.O_RDONLY))

        # Clean Up
        self.tearDown()

    def test_no_add(self):
        # Arrange
        file = FileConfigurator(JsonParser("testjson2.json"))

        # Act
        file.configure_append()
        list_of_lines = []

        with open('testfile.txt') as fin:
            for line in fin:
                list_of_lines.append(line)

        # Assert
        self.assertEqual("Errors Off\n", list_of_lines[0])
        self.assertEqual("Something Else Off\n", list_of_lines[1])
        self.assertEqual(True, self.check_permission(os.O_RDONLY))

