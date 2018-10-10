from unittest import TestCase
from unittest.mock import MagicMock

from src.package_installer import PackageInstaller
from src.bash_connector import BashConnector


class TestPackageConverter(TestCase):

    def setUp(self):
        pass

    def runTest(self):
        pass

    def test_initialization_with_text_file(self):
        # Arrange
        expected_list = [
            {
                "name": "Chromium-Browser",
                "comment": "No comment",
                "package name": "chromium-browser",
                "version": "Latest",
                "commands": [
                    {
                        "commandDescription": "install",
                        "command": "sudo apt-get install chromium-browser -y"
                    }
                ]
            },
            {
                "name": "Kdeconnect",
                "comment": "No Comment",
                "package name": "kdeconnect",
                "version": "Latest",
                "commands": [
                    {
                        "commandDescription": "install",
                        "command": "sudo apt install kdeconnect -y"
                    }
                ]
            }
        ]

        # Act
        package = TestPackageConverter("testPackageInstaller.txt")

        # Assert
        self.assertEqual(expected_list, package.packages)

    def test_initialization_with_json_file(self):
        # Arrange
        # Arrange
        expected_list = [
            {
                "name": "Chromium-Browser",
                "comment": "No comment",
                "package name": "chromium-browser",
                "version": "Latest",
                "commands": [
                    {
                        "commandDescription": "install",
                        "command": "sudo apt-get install chromium-browser -y"
                    }
                ]
            },
            {
                "name": "Kdeconnect",
                "comment": "No Comment",
                "package name": "kdeconnect",
                "version": "Latest",
                "commands": [
                    {
                        "commandDescription": "install",
                        "command": "sudo apt install kdeconnect -y"
                    }
                ]
            }
        ]

        package = PackageInstaller("testPackageInstaller.json")

        self.assertEqual(expected_list, package.packages)
    #
    # def foo(self):
    #     # Arrange
    #
    #     # Act
    #
    #     # Assert
    #
    #     self.assertEqual()