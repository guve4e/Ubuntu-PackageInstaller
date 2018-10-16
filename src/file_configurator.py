#!/usr/bin/python3
import fileinput
from src.json_parser import JsonParser
from src.bash_connector import BashConnector
from src.file import File


class FileConfigurator(object):

    def __init__(self, json_parser: JsonParser)-> None:
        super().__init__()

        self.__json_parser = json_parser

        try:
            self.__file_path = self.__json_parser.json_data['file_path']
            self.__comment_symbol = self.__json_parser.json_data['comment_symbol']
            self.__permission = self.__json_parser.json_data['permission']
            self.__config = self.__json_parser.json_data['config']

        except Exception as e:
            print("Wrong JSON file! Exception : " + str(e))

        self.__file = File(self.__file_path)

    @classmethod
    def __make_line(cls, line, comment, comment_symbol) -> str:
        if not comment:
            return line + "\n"
        else:
            return line + " " + comment_symbol + " " + comment + "\n"

    def __line_exists(self, search_line) -> bool:
        """
        Checks if line is already in the file.
        If so return true, if not false.
        :param search_line: dict containing line and comment
        the line to search for
        :return: boolean
        """
        search_line = self.__make_line(search_line['line'], "", self.__comment_symbol)

        with fileinput.FileInput(self.__file_path, inplace=False) as file:
            for line in file:
                if line == search_line:
                    print("The Line already exists : " + search_line, end='')
                    return True

        return False

    def __write_file(self):
        file = open(self.__file_path, 'w+')
        file.truncate(0)
        print(self.__file.content)
        file.close()

    def replace_text(self, text_search, text_replace) -> None:
        """
        Replaces pieces of text with other text.
        :param text_search: string text to be searched
        :param text_replace: string text to be replaced
        :return:
        """
        print("Replacing :'" + text_search + "' with '" + text_replace + "'")

        self.__file.change(text_search, text_replace)

    def configure_change(self) -> None:
        """
        Changes content in a file.
        :return: void, it returns early if
        change variable is not list
        """

        # check if change is empty
        # then there is no need to change text
        if not isinstance(self.__change, list):
            return

        for change in self.__change:
            self.__file.change(change['old'], change['new'])

    def append_text(self, line, comment):
        """
        Appends text to a file.
        :param line: string
        :param comment:
        :return:
        """
        line = self.__make_line(line, comment, self.__comment_symbol)

        print("Appending Line: " + line, end="")

        self.__file.append(line)

    def configure_append(self) -> None:
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
            # then check if this line is already appended
            # and if not, append it
            if not self.__line_exists(append):
                self.append_text(append['line'], append['comment'])

    def add_text(self, text_search, line_to_add, comment) -> None:
        """
        Adds text below particular line in the file.
        :param text_search: string, the search line
        :param line_to_add: string the line to be added
        :param comment: string the comment to be added
        :return: void
        """
        line_to_add = self.__make_line(line_to_add, comment, self.__comment_symbol)
        print("Adding Line: " + line_to_add, end="")

        with fileinput.FileInput(self.__file_path, inplace=True, backup='.bak') as file:
            for file_line in file:
                print(file_line, end='')
                if file_line.startswith(text_search):
                    print(line_to_add, end='')

    def configure_add(self) -> None:
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
            # then check if this line is already appended
            # and if not, add it
            if add['unique']:
                if not self.__line_exists(add):
                    self.__file.add(add['line'], add['after'])
            else:
                self.__file.add(add['line'], add['after'])

    def configure(self):

        print("=====================================")
        print("Configuring " + self.__file_path + " file\n")

        # do changing of lines first
        self.configure_change()

        # then do the appending
        self.configure_append()

        # then do the adding
        self.configure_add()

        # change open permission
        BashConnector.change_file_permission('777', self.__file_path)

        # write to file
        self.__write_file()

        # change closed permission
        BashConnector.change_file_permission(self.__permission, self.__file_path)






