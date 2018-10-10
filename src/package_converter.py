
class PackageConverter(object):

    def __init__(self, file_name) -> None:
        """
        Reads list of packages from file, makes a JSON with package objects
        :param file_name: string: the name of the file

        """
        self.__list_packages = []
        packages_str = self.__read_list_packages(file_name)
        self.__load_list_packages(packages_str)
        self.__list_dict_packages = self.__create_package_dictionary()

    def __read_list_packages(self, file_name: str) -> str:
        """
        Reads data from text file.
        :param file_name: the name of the file
        :return: data from text file as string
        """
        with open(file_name) as file:
            return file.read().strip()


    def __load_list_packages(self, file_data: str) -> None:
        """
        Splits the file data with new line delimiter.
        Updates __list_dict_packages member.
        :param file_name: file data
        :return: None
        """
        self.__list_packages = file_data.splitlines()


    def __create_package_dictionary(self)-> []:
        """
        Loops trough the list of packages
        and creates dictionary.
        :return:
        """
        list_packages = []

        for package in self.__list_packages:
            package_dict = {
                "name": package.title(),
                "comment": "No comment",
                "package name": package,
                "version": "Latest",
                "commands": [
                        {
                            "commandDescription": "install",
                            "command": "sudo apt install {} -y".format(package)
                        }
                    ]}
            list_packages.append(package_dict)

        return list_packages

    def serialize_line(self, line: str):
        s = line.replace("\t", "")
        s = s.replace("\n", "")
        s = s.replace("install", "")
        return s

    def get_packages(self) -> []:
        return self.__list_dict_packages
