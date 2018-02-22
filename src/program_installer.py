#!/usr/bin/python3
import subprocess
import os
import time
import string
from pathlib import Path

from src.package_installer import PackageInstaller
from src.parse_json import ParseJson

TMP_DIR = 'tmp/programinstaller'


class ProgramInstaller:
    """
    Downloads, unzips, and moves programs to specific folders.

    """
    def __init__(self, file_name) -> None:
        """
        Constructor
        :param file_name: s.Path object representing the path to the main json file
        """
        # send to ParseJson
        self.__json_list = ParseJson(file_name)
        self.__name = self.__directory = self.__prerequisites = self.__url = self.__alternative_dir = None

    @classmethod
    def delete_folder(cls, path):
        """
        Deletes folder specified by the
        path parameter
        :param path: string, path to directory
        :return:
        """
        for sub in path.iterdir():
            if sub.is_dir():
                cls.delete_folder(sub)
            else:
                sub.unlink()
        path.rmdir()

    @classmethod
    def file_size(cls, file_path) -> int:
        """
        Calculates the size of folder.
        :param file_path: path to directory.
        :return:
        """
        res = 0
        try:
            stat_info = os.stat(file_path)
            res = stat_info.st_size
        except IOError:
            pass
        finally:
            return res

    @classmethod
    def download_package(cls, download_url) -> bool:
        """
        Tries to download file
        :param download_url: url to a website
        :return:
        """
        success = False
        tmp_dir = ProgramInstaller.get_path()
        wget = 'wget -U Mozilla -P ' + tmp_dir + ' ' + download_url

        try:
            ProgramInstaller.execute_command(wget)
            success = True
        except subprocess.CalledProcessError as e:
            output = e.output
            print("=============================================")
            print("** Something went wrong while downloading  **")
            print("Message: " + output)
        finally:
            return success

    @classmethod
    def get_path(cls) -> str:
        """
        Returns the path to the temp
        folder used to store the downloaded files.
        """
        root_dir = os.path.abspath(os.sep)
        dir_name = root_dir + TMP_DIR

        return dir_name

    @classmethod
    def make_tmp_dir(cls) -> None:
        """
        Makes a tmp directory used to
        store downloaded files.
        :return:
        """
        tmp_dir = cls.get_path()

        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

    @classmethod
    def retrieve_archive_name(cls, path):
        """
        Given path to file, it splits it
        and returns the last part.
        Ex input - /home/some-file
           output - some-file
        :param path: string, path to file
        """
        if not path:
            return None

        archive_name = path.split('/')[-1]

        return str(archive_name)

    @classmethod
    def retrieve_file_name(cls, archive_name) -> str:
        """
        Given string representing archive name,
        it returns the name of the file.
        It strips the archive extensions.
        Ex: input - some-file.tar.gz
           output - some-file
        :param archive_name:
        :return: string, name of file
        """

        file_name = None
        # filter for non printing chars
        filtered_archive_name = ''.join(filter(lambda x: x in string.printable, archive_name))

        if cls.extract_archive_extension(archive_name) == "gz":
            file_name = filtered_archive_name.replace('.tar.gz', '')
        elif cls.extract_archive_extension(archive_name) == "zip":
            file_name = filtered_archive_name.replace('.zip', '')

        return file_name

    @classmethod
    def extract_archive_extension(cls, archive_name)-> str:
        """
        Given the name of the archive name,
        it splits by '.' and returns the last element
        Ex: input - some-file.tar.gz
            output - gz

        :param archive_name: string, the name of the archive
        :return: string, the name of the archive extension
        """
        if not archive_name:
            raise Exception("Null string!")

        archive_extension = archive_name.split('.')[-1]

        return archive_extension

    @classmethod
    def construct_archive_command(cls, file_name, destination_folder) -> str:
        """
        Constructs the command for unzipping using zip or tar.
        :param file_name: string, the path to file to be unzipped
        :param destination_folder: string, the path to the destination folder
        :return: string, the constructed command
        """
        command = None
        archive_extension = cls.extract_archive_extension(file_name)

        if archive_extension == 'zip':
            command = 'unzip -q ' + file_name + ' -d ' + destination_folder
        elif archive_extension == 'gz':
            command = 'tar -xvzf ' + file_name + ' -C ' + destination_folder
        else:
            raise Exception("Not know archive!")

        return command

    @classmethod
    def unzip_to_folder(cls, file_name, destination_folder) -> None:
        """
        Unzips.
        :param file_name: string, the path to file to be unzipped
        :param destination_folder: string, the path to the destination folder
        :return: void
        """
        command = cls.construct_archive_command(file_name, destination_folder)
        cls.make_destination_folder(destination_folder)

        try:
            cls.execute_command(command)

        except subprocess.CalledProcessError as e:
            output = e.output
            print(output)

    @classmethod
    def delete_tmp_dir(cls) -> None:
        """
        Deletes the directory used to store downloaded files
        :return: void
        """
        tmp_dir = cls.get_path()

        if cls.file_size(tmp_dir) > 0:
            p = Path(tmp_dir)
            cls.delete_folder(p)
        else:
            if os.path.exists(tmp_dir):
                os.rmdir(tmp_dir)

    @classmethod
    def execute_command(cls, command) -> None:
        """
        Executes shell command.
        Wrapped over subprocess.run.
        :param command:
        :return:
        """
        if not command:
            raise Exception("Null command!")

        subprocess.run(str(command), shell=True, check=True)

    @classmethod
    def make_destination_folder(cls, folder_name) -> None:
        """
        Creates directory used for storing downloaded files.
        :param folder_name: string, path to the folder to be created.
        :return: void
        """
        root_dir = os.path.abspath(os.sep)
        new_folder_path = root_dir + folder_name

        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

    @classmethod
    def install_prerequisites(cls, prerequisites):
        """
        Installs prerequisite packages,
        needed for each program.
        Loops trough each prerequisite and runs package_installer
        on each one.
        :param prerequisites: dict of prerequisites
        :return: void
        """
        if not prerequisites:
            return

        PackageInstaller(prerequisites)

    def install_single_program(self):
        """
        Installs one single program.
        :return:
        """

        print("=============================================")
        print("****       Installing Prerequisites      ****")
        print()
        self.install_prerequisites(self.__prerequisites)
        print("****                Done                 ****")

        self.make_tmp_dir()
        print("****            Downloading...           ****")
        print()

        if self.__url:
            if self.download_package(self.__url):
                file_name = self.retrieve_archive_name(self.__url)
                dir_name = self.get_path()
                file_name = dir_name + '/' + file_name
            elif self.__alternative_dir:
                file_name = self.__alternative_dir
            else:
                file_name = input("Enter a folder name with already downloaded archive: ")
        elif self.__alternative_dir:
            file_name = self.__alternative_dir

        time.sleep(2)
        self.make_destination_folder(self.__directory)

        print("****                Done                 ****")
        print("****            UnArchiving...           ****")
        print()
        self.unzip_to_folder(file_name, self.__directory)
        self.delete_tmp_dir()
        print("****                Done                 ****")

    def install_programs(self):
        """
        Loops trough each program and
        installs it.
        :return:
        """

        for program in self.__json_list.json_data:

            self.process_program_info(program)
            if not self.does_exist():
                self.install_single_program()
            else:
                print("The program {0} already exist!".format(self.__name))
                print("Files are located at {}".format(self.__directory))

    def process_program_info(self, program):
        """
        Sets members. Makes sure that
        one of the properties self.__url or self.__alternative_dir
        is set. If not it raises Exception
        :param program:
        :raise Exception, if  one of the properties self.__url or self.__alternative_dir
        is not set
        :return: void
        """

        self.__name = program['name']
        self.__url = program['download_url']
        self.__alternative_dir = program['alternative_dir']
        self.__prerequisites = program['prerequisites']
        self.__directory = program['directory']

        if not self.__url and not self.__alternative_dir:
            raise Exception("Bad JSON! download_url or alternative_dir MUST be specified!")

    def does_exist(self):
        """
        Check if a program is already copied to
        the destination folder. If there exist a folder that
        has name that contains the program name in it, it will
        return True.
        TODO if suck a folder is found give the user the diffference
        TODO and ask her what she needs to be done.
        :return:
        """
        file_name = None

        archive_name = self.retrieve_archive_name(self.__url)
        if archive_name:
            file_name = self.retrieve_file_name(archive_name)
        else:
            file_name = self.retrieve_file_name(self.__alternative_dir)

        # Sanity check
        if file_name is None:
            raise Exception('Something went wrong!')

        dir_list = os.listdir(self.__directory)
        program_name = self.extract_program_name(file_name)

        if any(program_name in dir_name for dir_name in dir_list):
            return True

    @classmethod
    def extract_program_name(cls, archive_name):
        """
        Given the name of the archive, it tries to extract,
        the program name
        First splits by '/', if any and returns the last one.
        Then it splits by '.' if any and returns the first one.
        Finally splits by '-' if any and returns the first one.
        :param archive_name:
        :return:
        """
        program_name = archive_name.split('/')[-1]
        program_name = program_name.split('.')[0]
        program_name = program_name.split('-')[0]
        return program_name
