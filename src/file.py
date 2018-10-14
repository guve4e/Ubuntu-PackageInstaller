#!/usr/bin/python3
import fileinput


class File(object):

    def __init__(self, file_name: str)-> None:
        super().__init__()

        self.__content = self.__read_file(file_name)

    def __read_file(self, file_name: str)-> str:
        """
        Reads data from text file.
        :param file_name: the name of the file
        :return: data from text file as string
        """
        with open(file_name) as file:
            return file.read().strip()

    @property
    def content(self):
        return self.__content

    def __add_line(self):
        pass

    def add(self, text: str, after: str):
        pass

    def change(self, old: str, new: str):
        pass

    def remove(self, text: str):
        pass

    def append(self, text: str):
        a = self.__content
        pass

    def prepend(self, text: str):
        pass

