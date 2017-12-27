#!/usr/bin/python3
import json
import time
import sys
import os

from os import listdir
from os.path import isfile, join
from src.package import Package
from src.config_file import ConfigurationFile
from src.parse_cmd_args import CmdArgumentsParser

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
    json_files = filter(lambda k: not 'programs' in k, json_files)
    files_list = list(json_files)
    # adjust each element
    file_names = map(lambda x: conf_name + "/" + x, files_list)

    return list(file_names)


def install_programs(config_name):
    """
    Searches for programs.json file in the
    directory and it tries to install each
    package
    :param config_name:
    :return: void
    """
    start_time = time.time()

    # get the right path
    dir_name = os.path.dirname(__file__)
    file = dir_name + "/configs/" + config_name + '/programs.json'

    try:
        with open(file) as json_data:
            # for each json object, load json
            programs = json.load(json_data)
            # parse json
            Package.parse(programs)

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

    # install packages first
    install_programs(cmd.config_name)

    # then do the adjustments
    configure_files(cmd.config_name)

    end_time_global = time.time()
    elapsed_time = round((end_time_global - start_time_global), 2)
    print("=====================================")
    print("It took " + str(elapsed_time) + " seconds to run script!")
