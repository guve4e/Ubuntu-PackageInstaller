from unittest import TestCase, mock
from src.package_converter import PackageConverter


class TestPackageConverter(TestCase):

    def setUp(self):
        self.file_content_list  = "some-package\nsome-other-package\n"

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
        self.testPackageConverter()

    @mock.patch("builtins.open", create=True)
    def testPackageConverter(self, mock_open):
        # Arrange
        mock_open.side_effect = [
            mock.mock_open(read_data=self.file_content_list).return_value
        ]

        # Act
        packageConverter = PackageConverter("testPackageInstaller.txt")
        actual_json = packageConverter.get_packages()

        # Assert
        self.assertEqual(actual_json, self.json_content)