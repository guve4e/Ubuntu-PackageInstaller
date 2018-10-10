from unittest import TestCase
from unittest.mock import MagicMock
from src.package_converter import PackageConverter


class TestPackageConverter(TestCase):

    def setUp(self):
        self.file_content = "some-package\nsome-other-package\n"

        self.json_content = [
            {
                "name": "Some-Package",
                "comment": "No comment",
                "package name": "some-package",
                "version": "Latest",
                "commands": [
                        {
                            "commandDescription": "install",
                            "command": "sudo apt install some-package -y"
                        }
                    ]
            },
            {
                "name": "Some-Other-Package",
                "comment": "No comment",
                "package name": "some-other-package",
                "version": "Latest",
                "commands": [
                        {
                            "commandDescription": "install",
                            "command": "sudo apt install some-other-package -y"
                        }
                    ]
            }
        ]

    def runTest(self):
        pass


    def testPackageConverter(self):
        # Act
        packageConverter = PackageConverter("testPackageInstaller.txt")
        actual_json = packageConverter.get_packages()

        # Assert
        self.assertEqual(actual_json, self.json_content)