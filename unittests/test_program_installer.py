#!/usr/bin/python3
import unittest
import os
from pathlib import Path
from src.program_installer import ProgramInstaller


class ProgramInstallerTestCase(unittest.TestCase):
    def setUp(self):
       pass

    def runTest(self):
        self.test_creation_of_tmp_dir()
        self.test_downloading()
        self.test_retrieve_name_of_file()
        self.test_unzip()
        self.test_deletion_of_tmp_dir()

    @classmethod
    def get_file_size(cls, file_path) -> int:
        stat_info = os.stat(file_path)
        return stat_info.st_size

    @classmethod
    def clean_up(cls):
        try:
            path = Path('/tmp/programinstaller')
        except IOError as e:
            print(e)
        ProgramInstaller.delete_folder(path)

    def test_creation_of_tmp_dir(self):
        # Arrange
        res = False

        # Act
        ProgramInstaller.make_tmp_dir()
        if os.path.exists('/tmp/programinstaller'):
            res = True

        # Assert
        self.assertTrue(res)

        # Clean Up
        ProgramInstallerTestCase.clean_up()

    def test_downloading(self):
        # Act
        ProgramInstaller.download_package("http://www.no-ip.com/client/linux/noip-duc-linux.tar.gz")

        # Assert
        self.assertTrue(os.path.exists('/tmp/programinstaller/noip-duc-linux.tar.gz'))

        # Clean Up
        ProgramInstallerTestCase.clean_up()

    def test_retrieve_name_of_file(self):
        # Arrange
        url = "http://www.no-ip.com/client/linux/noip-duc-linux.tar.gz"
        expected_name_of_file = 'noip-duc-linux.tar.gz'

        # Act
        actual_name_of_file = ProgramInstaller.retrieve_archive_name(url)

        # Assert
        self.assertEqual(expected_name_of_file, actual_name_of_file)

    def test_unzip(self):
        # Arrange
        file = "/tmp/programinstaller/noip-duc-linux.tar.gz"
        destination_folder = '/tmp/programinstaller/test'

        # Act
        ProgramInstaller.download_package("http://www.no-ip.com/client/linux/noip-duc-linux.tar.gz")
        ProgramInstaller.unzip_to_folder(file, destination_folder)

        # Assert
        file_size = ProgramInstallerTestCase.get_file_size('/tmp/programinstaller/test')
        self.assertTrue(file_size > 0)

        # Clean Up
        ProgramInstallerTestCase.clean_up()

    def test_deletion_of_tmp_dir(self):
        # Arrange
        res = False

        # Act
        ProgramInstaller.make_tmp_dir()
        ProgramInstaller.delete_tmp_dir()
        if not os.path.exists('/tmp/programinstaller'):
            res = True

        # Assert
        self.assertTrue(res)

    def test_retrieve_archive_name(self):
        # Act
        actual = ProgramInstaller.extract_archive_extension("android-studio-ide-171.4408382-linux.zip")

        # Assert
        self.assertEqual('zip', actual)