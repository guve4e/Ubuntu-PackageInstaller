#!/usr/bin/python3
import subprocess


class Package(object):
    """
    Package class to describe packages and their behavior
    """

    @staticmethod
    def found_char(string, char):
        """
        It is looking for a particular char
        in a string
        :param string: the string
        :param char: the char it is looking for
        :return:
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

    @staticmethod
    def split_string(string, char):
        """
        Splits string and returns
        the first part
        :param string: the string to be split
        :param char: delimiter
        :return: the first part of the string
        """
        string = string.split(char, 1)[0]
        return string

    @staticmethod
    def sanitize_str(string):
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

    @staticmethod
    def remove_chars(string):
        """
        Removes unnecessary characters from
        the string.
        :param string: the string to be manipulated
        :return: newly created string
        """

        # sanitize the string
        string = Package.sanitize_str(string)

        # remove unnecessary things
        if Package.found_char(string, "-"):
            string = string.split("-", 1)[0]
        elif Package.found_char(string, "ubuntu"):
            string = string.split("ubuntu", 1)[0]

        if Package.found_char(string, "+"):
            string = string.split("+", 1)[0]

        return string

    @staticmethod
    def apt_cache(package):
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

        # stores the output from apt-cache policy
        output = None

        # use subprocess to execute apt-cache policy
        # pipe it to a variable output
        try:
            c = cache_policy + str(package['package name'])
            proc = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE)
            output = proc.stdout.read()

        except subprocess.CalledProcessError as e:
            output = e.output

        return output

    @staticmethod
    def install_package(command):
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
        except subprocess.CalledProcessError as e:
            output = e.output
            print(output)

    @staticmethod
    def update():
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

    @staticmethod
    def install(package):
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
            Package.install_package(command)

    @staticmethod
    def is_installed(version):
        """
        Checks if package is installed.
        :param version: string ersion of the package
        :return: boolean true/false
        """

        if not version:
            return False

        found = Package.found_char(version, "none")
        if not found:
            return True
        else:
            return False

    @staticmethod
    def extract_version(output):
        """
        Gets the version of the package
        :param output: string containing the version
        or 'b if there is non
        :return: the version of the package
        """

        # split the output and extract the
        # installed part as:
        # Installed: 1.6-2

        if not output:
            return 0
        l = output.split()
        version = l[2]
        return version

    @staticmethod
    def print_info(package):
        # print some info
        print("###################################################")
        print("Installing : " + package['name'])
        print("Comments   : " + package['comment'])
        print("Version    : " + package['version'])

    @staticmethod
    def run_package_installer(element):
        # print info
        Package.print_info(element)
        # execute apt-cache
        output = Package.apt_cache(element)
        # get the version
        version = Package.extract_version(output)

        # check if installed
        if not Package.is_installed(version):
            # if not, installed it
            Package.install(element)
        else:
            # else, just address the user
            # remove certain chars
            version = Package.remove_chars(version)

            print("This Package is already installed! Version is " + version + "\n")

    @staticmethod
    def parse(package):
        """
        Parses each json object
        :param package: is json object containing
        information about the program to be installed
        :return: void
        """
        for element in package:
            Package.run_package_installer(element)