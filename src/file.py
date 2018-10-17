#!/usr/bin/python3
import os.path

class File(object):
    """
    Inefficient!
    It manipulates two data structures,
    (__content and __content_list) instead of one.
    TODO Get rid of one of the data structures
    """
    def __init__(self, file_name: str)-> None:
        super().__init__()

        self.__file_path = file_name
        self.__content = self.read_file(file_name)
        self.__content_list = None
        self.__update_content_list()

    def __update_content_list(self):
        self.__content_list = self.__content.splitlines()

    @property
    def content(self):
        return self.__content

    def read_file(self, file_name: str)-> str:
        """
        Reads data from text file.
        :param file_name: the name of the file
        :return: data from text file as string
        """
        if not os.path.exists(file_name):
            raise Exception("The File {} doesn't exists!".format(file_name))

        with open(file_name) as file:
            return file.read().strip()

    def write_file(self):
        """
        After file manipulation is done,
        it writes __content string to file.
        :return:
        """
        file = open(self.__file_path, 'w+')
        file.truncate(0)
        print(self.__content)
        file.close()

    def line_exists(self, search_line)-> bool:
        return search_line in self.__content_list

    def add(self, text: str, after: str):
        """
        Searches for element in list.
        If found inserts new element after it.
        :param text: the element we are looking for
        :param after: the element to be inserted
        :return:
        """
        index = -1

        # loop trough all of the elements
        for i, line in enumerate(self.__content_list, start=0):
            if line.startswith(after):
                # we need the next one
                index = i + 1
                # no need to go further
                break

        # check if found
        if index is -1:
            return

        self.__content_list.insert(index, text)
        self.__content = '\n'.join(self.__content_list)

    def change(self, old: str, new: str):
        self.__content = self.__content.replace(old, new)
        self.__update_content_list()

    def remove(self, text: str):
        """

        :param text:
        :return:
        """
        index = -1

        # loop trough all of the elements
        for i, line in enumerate(self.__content_list, start=0):
            if line == text:
                # we need the next one
                index = i
                # no need to go further
                break

        # delete the element
        del self.__content_list[index]
        self.__content = '\n'.join(self.__content_list)

    def append(self, text: str):
        self.__content = self.__content + "\n" + text
        self.__update_content_list()

    def prepend(self, text: str):
        self.__content = text + "\n" + self.__content
        self.__update_content_list()

