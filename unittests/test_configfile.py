#!/usr/bin/python3
import unittest
import os
import subprocess
from src.config_file import ConfigurationFile


class ConfigurationFileTestCase(unittest.TestCase):
    def setUp(self):

        # Arrange
        # Dependency for Make Requests
        self.file = ConfigurationFile("testjson.json")

    def runTest(self):
        self.test_configure()
        self.test_change_permission()

        self.test_restore()

    def check_permission(self, option):
        return os.access("testjson.json", option)

    def change_permission(self, mode):
        try:
            subprocess.call(['chmod', mode, "testjson.json"])
        except subprocess.CalledProcessError as e:
            output = e.output
            print(output)

    def test_change_permission(self):
        # Arrange
        self.change_permission('444')

        # Act
        self.file.change_file_permission('777', "testjson.json")

        # Assert
        self.assertEqual(True, self.check_permission(os.W_OK))

    def test_configure(self):

        # Act
        self.file.configure_change()
        list_of_lines = []

        with open('testfile.txt') as fin:
            for line in fin:
                list_of_lines.append(line)

        # Assert
        self.assertEqual("Errors On\n", list_of_lines[0])
        self.assertEqual("Something Else On\n", list_of_lines[1])

    def test_restore(self):
        """
        Doesnt TEST, but restores the testing file
        and it checks for competition
        :return:
        """
        # write everything back
        with open('testfile.txt', 'w') as file:
            file.writelines("Errors Off\n")
            file.writelines("Something Else Off\n")

        list_of_lines = []

        with open('testfile.txt') as fin:
            for line in fin:
                list_of_lines.append(line)

        self.change_permission('444')

        self.assertEqual("Errors Off\n", list_of_lines[0])
        self.assertEqual("Something Else Off\n", list_of_lines[1])
        self.assertEqual(False, self.check_permission(os.W_OK))