import subprocess


class PackageInstaller(object):
    """
    Installs packages
    """
    def __init__(self, packages) -> None:

        self.__packages_installed = 0
        self.__packages = packages

        for package in self.__packages:
            self.__run_package_installer(package)

    @classmethod
    def found_char(cls, string: str, char: str) -> bool:
        """
        It is looking for a particular char
        in a string
        :param string: the string
        :param char: the char it is looking for
        :return: boolean
        """
        str_version = str(string)
        # try to find substring
        find = str_version.find(char)

        if find == -1:
            # if not found
            return False
        else:
            # found
            return True

    @classmethod
    def split_string(cls, string: str, char: str) -> str:
        """
        Splits string and returns
        the first part
        :param string: the string to be split
        :param char: delimiter
        :return: the first part of the string
        """
        string = string.split(char, 1)[0]
        return string

    @classmethod
    def sanitize_str(cls, string: str) -> str:
        """
        Removes 'b' and ' from a string
        :param string: the string to be sanitized
        :return: newly created string
        """

        # convert to string
        string = str(string)
        # remove "b"
        string = string.replace("b'", "")
        # remove '
        string = string.replace("'", "")
        return string

    @classmethod
    def remove_chars(cls, string: str) -> str:
        """
        Removes unnecessary characters from
        the string.
        :param string: the string to be manipulated
        :return: newly created string
        """

        # sanitize the string
        string = cls.sanitize_str(string)

        # remove unnecessary things
        if cls.found_char(string, "-"):
            string = string.split("-", 1)[0]
        elif cls.found_char(string, "ubuntu"):
            string = string.split("ubuntu", 1)[0]

        if cls.found_char(string, "+"):
            string = string.split("+", 1)[0]

        return string

    @classmethod
    def __apt_cache(cls, package: {}) -> str:
        """
        Script uses apt-cache policy (ubuntu program)
        to gather information for a package (installed
        or not and version).
        Assumes that it is installed since
        any version after 14 has it by default.
        :param package: json object representing package
        :return: The output of executed apt-cache policy
        program.
        """

        cache_policy = "apt-cache policy "

        # use subprocess to execute apt-cache policy
        # pipe it to a variable output
        try:
            c = cache_policy + str(package['package name'])
            proc = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE)
            shell_output = proc.stdout.read()

        except subprocess.CalledProcessError as e:
            shell_output = e.output

        return shell_output

    def __install_package(self, command) -> None:
        """
        Runs a terminal command.
        Ex:
        sudo apt-get install chromium-browser -y
        :param command: string containing ubuntu commands to
        install package.
        Ex: sudo apt-get install chromium-browser -y
        :return: void
        """

        try:
            subprocess.run(str(command['command']), shell=True, check=True)
            # increment the number of installed packages
            self.__packages_installed = self.__packages_installed + 1
        except subprocess.CalledProcessError as e:
            output = e.output
            print(output)

    @classmethod
    def __update(cls):
        """
        Downloads the package lists from the repositories and "updates"
        them to get information on the newest versions of packages and their dependencies
        :return: void
        """

        try:
            subprocess.run("sudo apt-get update ", shell=True, check=True)
        except subprocess.CalledProcessError as e:
            output = e.output
            print(output)

    def __install(self, package) -> None:
        """
        Wrapper around install_package
        :param package: json object representing package
        :return: void
        """
        i = 0
        for command in package['commands']:
            i += 1
            print("Command Description " + str(i) + ": " + str(command['commandDescription']))
            print("Command :" + str(command['command']))
            self.__install_package(command)

    @classmethod
    def __is_installed(cls, version: str) -> bool:
        """
        Checks if package is installed.
        :param version: string version of the package
        :return: boolean true/false
        """

        if not version:
            return False

        found = cls.found_char(version, "none")
        if not found:
            return True
        else:
            return False

    @classmethod
    def __extract_version(cls, output: str):
        """
        Gets the version of the package
        :param output: string containing the version
        or 'b if there is none
        :return: the version of the package
        """

        # split the output and extract the
        # installed part as:
        # Installed: 1.6-2

        if not output:
            return 0
        tmp = output.split()
        version = tmp[2]

        return version

    @classmethod
    def __print_info(cls, package) -> None:
        # print some info
        print("###################################################")
        print("Installing : " + package['name'])
        print("Comments   : " + package['comment'])
        print("Version    : " + package['version'])

    def __run_package_installer(self, package):
        # print info
        PackageInstaller.__print_info(package)
        # execute apt-cache
        output = PackageInstaller.__apt_cache(package)
        # get the version
        version = PackageInstaller.__extract_version(output)

        # check if installed
        if not PackageInstaller.__is_installed(version):
            # if not, installed it
            self.__install(package)
        else:
            # else, just address the user
            # remove certain chars
            version = PackageInstaller.remove_chars(version)

            print("This Package is already installed! Version is " + version + "\n")

        # update
        PackageInstaller.__update()

    def get_num_installed_packages(self) -> int:
        return self.__packages_installed
