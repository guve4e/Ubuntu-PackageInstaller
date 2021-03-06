import subprocess


class BashConnector(object):

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

        # use subprocess to execute apt-cache policy
        # pipe it to a variable output
        try:
            c = cache_policy + str(package['package name'])
            proc = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE)
            shell_output = proc.stdout.read()

        except subprocess.CalledProcessError as e:
            shell_output = e.output

        return shell_output

    @classmethod
    def install_package(cls, command)-> None:
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

    @classmethod
    def update(cls):
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

    @classmethod
    def change_file_permission(cls, mode, file)-> None:
        """
        Uses chmod to change the permission of the file.
        :param mode: string chmod mode Ex: '777'
        :param file: the file to be chmod-ed
        :return: void
        :raises: when subprocess fails
        """

        try:
            subprocess.call(['chmod', mode, file])
        except subprocess.CalledProcessError as e:
            output = e.output
            print(output)

