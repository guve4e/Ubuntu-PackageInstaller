import json

from src.package import Package


class PackageConverter(object):

    def __init__(self, file_name) -> None:
        """
        Reads list of packages from file, makes a JSON with package objects
        :param file_name: string: the name of the file

        """
        self.list_packages = []
        self.json_packages = None

        with open(file_name) as fin:
            for line in fin:
                line = self.serialize_line()

                self.list_packages.append(line)

        dict_packages = self.create_package_dictionary()

        self.dump_json(dict_packages)

    def create_package_dictionary(self) -> [{}]:
        """
        Loops trough the list of packages
        and creates dictionary.
        :return:
        """
        list_packages = [{}]

        for package in self.list_packages:
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

    def dump_json(self, list_packages: []):
        self.json_packages = json.dumps(list_packages)

    def serialize_line(self, line: str):
        s = str.strip("\t")
        s = s.strip("\n")
        s = s.strip("install")
        return s


if __name__ == "__main__":

    packages = PackageConverter("installed.txt")

    # parse json
    Package.parse(packages)

