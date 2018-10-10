
class PackageConverter(object):

    def __init__(self, file_name) -> None:
        """
        Reads list of packages from file, makes a JSON with package objects
        :param file_name: string: the name of the file

        """
        self.__list_packages = []
        self.__load_list_packages(file_name)
        self.__list_dict_packages = self.__create_package_dictionary()

    def __load_list_packages(self, file_name) -> None:
        with open(file_name) as fin:
            for line in fin:
                line = self.serialize_line(line)
                self.__list_packages.append(line)

    def __create_package_dictionary(self)-> [{}]:
        """
        Loops trough the list of packages
        and creates dictionary.
        :return:
        """
        list_packages = [{}]

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
