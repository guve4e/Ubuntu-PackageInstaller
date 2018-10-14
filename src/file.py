#!/usr/bin/python3
import fileinput


class File(object):

    def __init__(self, file_name: str)-> None:
        super().__init__()

        self.__file_path = file_name
        self.__content = self.__read_file(file_name)
        self.__content_list = self.__content.splitlines()

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

    def prepend(self, text: str):
        self.__content = text + "\n" + self.__content

