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

        """
        Uses chmod to change the permission of the file.
        :param mode: string chmod mode Ex: '777'
        :param file: the file to be chmod-ed
        :return: void
        :raises: when subprocess fails
        """

        try:
            subprocess.call(['chmod', mode, file])
        except subprocess.CalledProcessError as e:
            output = e.output
            print(output)

    def replace_text(self, text_search, text_replace):
        """
        Replaces pieces of text with other text.
        :param text_search: string text to be searched
        :param text_replace: string text to be replaced
        :return:
        """
        with fileinput.FileInput(self.__file_path, inplace=True, backup='.bak') as file:
            for line in file:
                print(line.replace(text_search, text_replace), end='')

    def configure_change(self):
        """
        Changes content in a file.
        :return: void, it returns early if
        channge variable is not list
        """

        # check if change is empty
        # then there is no need to change text
        if not isinstance(self.__change, list):
            return

        for change in self.__change:
            self.replace_text(change['old'], change['new'])

    def add_text(self, command, comment):

        """
        Appends text to a file.
        :param command: string
        :param comment:
        :return:
        """
        line = command + " # " + comment + "\n"

        with open(self.file_path, "a") as file:
            file.write(line)

    def configure_add(self):
        """
        Adds content to file.
        :return: void, it returns early if
        add variable is not list
        """

        # check if add is empty
        # then there is no need to add text
        if not isinstance(self.__add, list):
            return

        for add in self.__add:
            self.add_text(add['line'], add['comment'])

    def configure(self):

        # change open permission
        self.change_file_permission('777', self.__file_path)

        # do changing of lines first
        self.configure_change()

        # then do the adding
        self.configure_add()

        # change closed permission
        self.change_file_permission('444', self.__file_path)


