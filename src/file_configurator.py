#!/usr/bin/python3

from src.json_parser import JsonParser
from src.bash_connector import BashConnector
from src.file import File


class FileConfigurator(object):

    def __init__(self, json_parser: JsonParser, bash_connector: BashConnector)-> None:
        super().__init__()

        self.__json_parser = json_parser
        self.__bash_connector = bash_connector

        try:
            self.__file_path = self.__json_parser.json_data['file_path']
            self.__comment_symbol = self.__json_parser.json_data['comment_symbol']
            self.__permission = self.__json_parser.json_data['permission']
            self.__config_list = self.__json_parser.json_data['config']

        except Exception as e:
            print("Wrong JSON file! Exception : " + str(e))

        self.__file = File(self.__file_path)

    @property
    def file(self):
        return self.__file

    def __text_exists(self, text: str)-> bool:
        """
        Determines if the text string has \n character.
        If it does, calls file.text_exist,
        if it does not, it calls file.line_exist
        :param text: the text to search for
        :return: boolean value
        """
        if "\n" in text:
            result = self.__file.text_exists(text)
        else:
            result = self.__file.line_exists(text)

        return result

    def configure_change(self, config: {}) -> None:
        """
        Changes content to file. Searches for a substring
        and replaces it with the given text
        """
        self.__file.change(config['search_text'], config['text'])

    def configure_append(self, config: {})-> None:
        """
        Appends content to file.
        :return: void, returns early if the config specifies
        that the line is unique and the line actually exists
        """
        if config['unique']:
            if self.__text_exists(config['text']):
                return

        self.__file.append(config['text'])

    def configure_add(self, config: {})-> None:
        """
        Adds content to file, after a particular piece of text.
        :return: void, returns early if the config specifies
        that the line is unique and the line actually exists
        """
        if config['unique']:
            if self.__text_exists(config['text']):
                return

        self.__file.add(config['text'], config['after'])

    def configure(self):
        """
        Wrapper
        :return:
        """
        print("=====================================")
        print("Configuring " + self.__file_path + " file\n")

        for config in self.__config_list:
            if config['verb'] == 'add':
                self.configure_add(config)
            elif config['verb'] == 'change':
                self.configure_change(config)
            elif config['verb'] == 'append':
                self.configure_append(config)
            elif config['verb'] == 'remove':
                # TODO not implemented yet
                pass
            else:
                raise Exception("Bad verb in config json file!")

        # change open permission
        self.__bash_connector.change_file_permission('777', self.__file_path)

        # write to file
        self.__file.write_file()

        # change closed permission
        self.__bash_connector.change_file_permission(self.__permission, self.__file_path)






