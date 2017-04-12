#!/usr/bin/python3
import json
import subprocess


class Package(object):
    # Package class to describe packages and their behavior

    @staticmethod
    def apt_cache(d):
        # script uses apt-cache policy
        # assume that it is installed since
        # any version after 14 has it by default
        cache_policy = "apt-cache policy "

        # stores the output from apt-cache policy
        output = None

        # use subprocess to execute apt-cache policy
        # pipe it to a variable output
        try:
            c = cache_policy + str(d['package name'])
            proc = subprocess.Popen(c, shell=True, stdout=subprocess.PIPE)
            output = proc.stdout.read()

        except subprocess.CalledProcessError as e:
            output = e.output

        return output

    @staticmethod
    def install_package(command):
        try:
            subprocess.run(str(command['command']), shell=True, check=True)
        except subprocess.CalledProcessError as e:
            output = e.output
            print(output)

    @staticmethod
    def update():
        # Downloads the package lists from the repositories and "updates"
        # them to get information on the newest versions of packages and their dependencies
        try:
            subprocess.run("sudo apt-get update ", shell=True, check=True)
        except subprocess.CalledProcessError as e:
            output = e.output
            print(output)

    @staticmethod
    def install(d):
        i = 0
        for command in d['commands']:
            i += 1
            print("Command Description " + str(i) + ": " + str(command['commandDescription']))
            print("Command :" + str(command['command']))
            output = None
            Package.install_package(command)

    @staticmethod
    def is_installed(version):
        if version == "(none)":
            return True
        else:
            return False

    @staticmethod
    def extract_version(output):
        # split the output and extract the
        # installed part as:
        # Installed: 1.6-2
        l = output.split()
        version = l[2]
        return version

    @staticmethod
    def print_info(d):
        # print some info
        print("Installing : " + d['name'])
        print("Comments : " + d['comment'])
        print("Version : " + d['version'])

    @staticmethod
    def parse(program):
        # parse the json file
        for d in program:
            # print info
            Package.print_info(d)
            # execute apt-cache
            output = Package.apt_cache(d)
            # get the version
            version = Package.extract_version(output)

            # check if installed
            if Package.is_installed(version):
                # if not, installed it
                Package.install(d)
            else:
                # else, just address the user
                print("This Package is already installed! Version is " + str(version))


if __name__ == "__main__":

    try:
        with open('programs.json') as json_data:
            # load json
            programs = json.load(json_data)
            # parse json
            Package.parse(programs)

    except IOError as e:
        print(e.strerror)
