#!/usr/bin/python3
import json
import time
import sys
import os

from os import listdir
from os.path import isfile, join

from src.package_converter import PackageConverter
from src.config_file import ConfigurationFile
from src.package_installer import PackageInstaller
from src.parse_cmd_args import CmdArgumentsParser
from src.program_installer import ProgramInstaller

"""
Driver file.
"""


def get_file_list(conf_name) -> []:
    """
    Retrieves a list of file names (paths)
    :param conf_name: the name of config folder
    :return: list of file names
    """

    dir_name = os.path.dirname(__file__)
    conf_dir_path = dir_name + "/configs/" + conf_name

    if not os.path.exists(conf_dir_path):
        raise IOError(conf_name + " is not a valid configuration folder" + "\n")

    file_path = os.path.join(dir_name, "configs", conf_name)
    all_files = [f for f in listdir(file_path) if isfile(join(file_path, f))]

    # we need only json files
    json_files = filter(lambda k: '.json' in k, all_files)
    json_files = filter(lambda k: not 'packages' in k and not 'programs' in k, json_files)
    files_list = list(json_files)

    # adjust each element
    file_names = map(lambda x: conf_name + "/" + x, files_list)

    return list(file_names)


def install_programs(config_name):
    """
    Searches for programs.json file in the
    directory and it tries to install each
    program
    :param config_name:
    :return: void
    """
    start_time = time.time()

    # get the right path
    dir_name = os.path.dirname(__file__)
    file = dir_name + "/configs/" + config_name + '/programs.json'

    p = ProgramInstaller(file)
    p.install_programs()

    end_time = time.time()
    elapsed_time = round((end_time - start_time), 2)
    print("=====================================")
    print("It took " + str(elapsed_time) + " seconds to install packages!")


def install_packages(packages: [{}]) -> None:
    installer = PackageInstaller(packages)
    print("Total installed packages: {}".format(installer.get_num_installed_packages()))


def load_packages(config_name):
    """
    Searches for packages.json file in the
    directory and it tries to install each
    package
    :param config_name:
    :return: void
    """
    start_time = time.time()

    # get the right path
    dir_name = os.path.dirname(__file__)
    file = dir_name + "/configs/" + config_name + '/packages.json'

    try:
        with open(file) as json_data:
            # for each json object, load json
            packages = json.load(json_data)
            # parse json
            install_packages(packages)

    except IOError as e:
        print(e.strerror)

    end_time = time.time()
    elapsed_time = round((end_time - start_time), 2)
    print("=====================================")
    print("It took " + str(elapsed_time) + " seconds to install packages!")


def configure_files(config_name):
    """
    Loops for all json files except programs.json
    and it configures each config file accordingly.
    :param config_name: the name of the configuration
    :return: void
    """

    start_time = time.time()

    try:
        files = get_file_list(config_name)

        for file in files:
            config("configs/" + file)

    except IOError as e:
        print(e.strerror)

    end_time = time.time()
    elapsed_time = round((end_time - start_time), 2)
    print("=====================================")
    print("It took " + str(elapsed_time) + " seconds to configure files!")


def config(file_path):
    """
    Configures the php ini file.
    Loads json file with new
    configurations.
    :return: void
    """
    cf = ConfigurationFile(file_path)
    cf.configure()


if __name__ == "__main__":

    start_time_global = time.time()

    cmd = CmdArgumentsParser(sys.argv)

    # if user specifies to install packages only
    # from text file
    if cmd.is_raw_packages():
        packages = PackageConverter(cmd.file_name)
        p = packages.get_packages()
        install_packages(p)
    else:
        # install packages first
        load_packages(cmd.config_name)

        # then install programs
        install_programs(cmd.config_name)

        # then do the adjustments
        configure_files(cmd.config_name)

    end_time_global = time.time()
    elapsed_time = round((end_time_global - start_time_global), 2)
    print("=====================================")
    print("It took " + str(elapsed_time) + " seconds to run script!")
