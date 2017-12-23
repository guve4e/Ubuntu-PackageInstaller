#!/usr/bin/python3
import unittest
import os
import subprocess
from src.config_file import ConfigurationFile


class ConfigurationFileTestCase(unittest.TestCase):
    def setUp(self):
        # Arrange
        self.restore()
        # Dependency for Make Requests
        self.file = ConfigurationFile("testjson.json")

    def runTest(self):
        self.test_configure_change()
        self.test_change_permission()
        self.test_configure_append()
        self.test_configure_add()
        self.test_no_add()

    @staticmethod
    def check_permission(option):
        return os.access("testjson.json", option)

    @staticmethod
    def change_permission(mode):
        try:
            subprocess.call(['chmod', mode, "testjson.json"])
        except subprocess.CalledProcessError as e:
            output = e.output
            print(output)

    def restore(self):
        """
        Doesnt TEST, but restores the testing file
        and it checks for competition
        :return:
        """
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

    def test_change_permission(self):
        # Arrange
        self.change_permission('444')

        # Act
        self.file.change_file_permission('777', "testjson.json")

        # Assert
        self.assertEqual(True, self.check_permission(os.W_OK))

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
        self.restore()

    # def test_line_exists(self):
    #     # Arrange
    #
    #
    #     # Act
    #     res = self.file.line_exists("Something Else Off")
    #
    #     # Assert
    #     self.assertEqual(True, res)

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
        self.restore()

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
        self.restore()

    def test_no_add(self):
        # Arrange
        file = ConfigurationFile("testjson2.json")

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

