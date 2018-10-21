import subprocess


class BashConnector(object):

    @classmethod
    def __shell(self, command: str)-> str:
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        return proc.stdout.read()

    @classmethod
    def apt_cache(cls, package: {})-> str:
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
        command = cache_policy + str(package['package name'])
        return BashConnector.__shell(command)

    @classmethod
    def install_package(cls, command)-> str:
        """
        Runs a terminal command.
        Ex:
        sudo apt-get install chromium-browser -y
        :param command: string containing ubuntu commands to
        install package.
        Ex: sudo apt-get install chromium-browser -y
        :return: void
        """
        return BashConnector.__shell(str(command['command']))

    @classmethod
    def update(cls)-> str:
        """
        Downloads the package lists from the repositories and "updates"
        them to get information on the newest versions of packages and their dependencies
        :return: void
        """
        return BashConnector.__shell("sudo apt update")

    @classmethod
    def change_file_permission(cls, mode, file)-> str:
        """
        Uses chmod to change the permission of the file.
        :param mode: string chmod mode Ex: '777'
        :param file: the file to be chmod-ed
        :return: void
        :raises: when subprocess fails
        """
        command_str = ''.join(['chmod', mode, file])
        return BashConnector.__shell(command_str)


