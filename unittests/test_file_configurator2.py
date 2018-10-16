#!/usr/bin/python3
import unittest
import os
import subprocess
from unittest.mock import patch, MagicMock

from src.bash_connector import BashConnector
from src.file_configurator import FileConfigurator
from src.json_parser import JsonParser


class ConfigurationFileTestCase(unittest.TestCase):
    def setUp(self):
        self.file_content = "Errors Off\nSomething Else Off\n" \
                            "Some Configuration\n[mode]\n    Some other configuration"

    def runTest(self):
        pass

    @staticmethod
    def check_permission(option):
        return os.access("testjson.json", option)

    @staticmethod
    def change_permission(mode):
        subprocess.call(['chmod', mode, "testjson.json"])

    def tearDown(self):
        pass

    @patch("src.file.File.write_file", create=True)
    @patch("src.file.File.read_file", create=True)
    @patch("src.json_parser.JsonParser.load_json", create=True)
    def test_foo(self, mock_parser, mock_open_config_file, mock_close_config_file):
        # Arrange
        mock_parser.return_value = {
            "file_path": "/etc/apache2/apache2.conf",
            "comment_symbol": "#",
            "permission": "444",
            "config": [
                {
                    "verb": "append",
                    "unique": True,
                    "text": "Include /etc/phpmyadmin/apache.conf"
                },
                {
                    "verb": "add",
                    "unique": True,
                    "after": "Something Else Off",
                    "text": "<Directory /var/www/>\n    Options Indexes FollowSymLinks\n    AllowOverride "
                            "None\n</Directory>\n"
                }
            ]
        }

        mock_open_config_file.return_value = "Errors Off\nSomething Else Off\n" \
                                             "Some Configuration\n[mode]\n    Some other configuration"

        mock_close_config_file.return_value = None

        expected_file_content = "Errors Off\nSomething Else Off\n<Directory /var/www/>\n    Options Indexes " \
                                "FollowSymLinks\n    AllowOverride None\n</Directory>\n" \
                                "Some Configuration\n[mode]\n    Some other configuration\nInclude " \
                                "/etc/phpmyadmin/apache.conf "

        mock_bash_connector = BashConnector()
        mock_bash_connector.change_file_permission = MagicMock()

        # Act
        file_configurator = FileConfigurator(JsonParser("some_file"), mock_bash_connector)
        file_configurator.configure()

        # Assert
        self.assertEqual(file_configurator.file.content, expected_file_content)