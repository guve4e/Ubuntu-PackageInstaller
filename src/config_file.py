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
        3. append - dictionary of things that need to be appended

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
        self.__append = self.json_data['append']
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
    def append(self):
        return self.__append

    @append.setter
    def append(self, value):
        self.__append = value

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

        print("Replacing :'" + text_search + "' with '" + text_replace + "'")

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

    @classmethod
    def make_line(cls, line, comment)-> str:
        return line + " # " + comment + "\n"

    def append_text(self, line, comment):
        """
        Appends text to a file.
        :param line: string
        :param comment:
        :return:
        """
        line = self.make_line(line, comment)

        print("Appending Line: " + line, end="")

        with open(self.file_path, "a") as file:
            file.write(line)

    def configure_append(self):
        """
        Appends content to file.
        :return: void, it returns early if
        append variable is not list
        """

        # check if append is empty
        # then there is no need to append text
        if not isinstance(self.__append, list):
            return

        for append in self.__append:
            self.append_text(append['line'], append['comment'])

    def add_text(self, text_search, line_to_add, comment):
        """
        Adds text below particular line in the file.
        :param text_search: string, the search line
        :param line_to_add: string the line to be added
        :param comment: string the comment to be added
        :return:
        """
        line_to_add = self.make_line(line_to_add, comment)
        print("Adding Line: " + line_to_add, end="")

        with fileinput.FileInput(self.__file_path, inplace=True, backup='.bak') as file:
            for file_line in file:
                print(file_line, end='')
                if file_line.startswith(text_search):
                    print(line_to_add, end='')

    def configure_add(self):
        """
        Adds content to file, after a particular piece of text.
        :return: void, it returns early if
        append variable is not list
        """

        # check if append is empty
        # then there is no need to append text
        if not isinstance(self.__add, list):
            return

        for add in self.__add:
            self.add_text(add['after'], add['line'], add['comment'])

    def configure(self):

        print("=====================================")
        print("Configuring " + self.file_path + " file\n")

        # change open permission
        self.change_file_permission('777', self.__file_path)

        # do changing of lines first
        self.configure_change()

        # then do the appending
        self.configure_append()

        # then do the adding
        self.configure_add()

        # change closed permission
        self.change_file_permission('444', self.__file_path)



