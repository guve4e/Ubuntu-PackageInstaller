#!/usr/bin/python3
import subprocess
import fileinput
from src.parse_json import ParseJson


class ConfigurationFile(ParseJson):
    """
    This class parses json file -> test.json
    It inherits from PareJson since it parses a json file,
    but specific json file.

    Note: This class uses subprocess which is an
    expensive operation, as you are creating a sub-shell
    and invoking /bin/chmod directly.

    It has 3 members:
        1. file_path - path to the file that will be configured
        2. change - dictionary of things that need to be changed
        3. add - dictionary of things that need to be added

        """
    def __init__(self, file_name) -> None:
        """
        Constructor
        :param file_name: s.Path object representing the path to the main json file
        """

        # send to ParseJson
        ParseJson.__init__(self, file_name)

        self.__file_path = self.json_data['file_path']
        self.__change = self.json_data['change']
        self.__add = self.json_data['add']

    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, value):
        self.__file_path = value

    @property
    def change(self):
        return self.__change

    @change.setter
    def change(self, value):
        self.__change = value

    @property
    def add(self):
        return self.__add

    @add.setter
    def add(self, value):
        self.__add = value

    @classmethod
    def change_file_permission(cls, mode, file):

        # TODO check file and mode

        try:
            subprocess.call(['chmod', mode, file])
        except subprocess.CalledProcessError as e:
            output = e.output
            print(output)

    def replace_text(self, text_search, text_replace):

        with fileinput.FileInput(self.__file_path, inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace(text_search, text_replace), end='')

    def configure_change(self):

        for change in self.__change:
            self.replace_text(change['old'], change['new'])

    def configure(self):

        # change open permission
        self.change_file_permission('777', self.__file_path)

        self.configure_change()

        # change closed permission
        self.change_file_permission('444', self.__file_path)