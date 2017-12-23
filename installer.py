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

    filepath = os.path.join(dir_name, "configs", conf_name)
    all_files = [f for f in listdir(filepath) if isfile(join(filepath, f))]

    # we need only json files
    json_files = filter(lambda k: '.json' in k, all_files)
    files_list = list(json_files)
    # adjust each element
    fileNames = map(lambda x: conf_name + "/" + x, files_list)

    return list(fileNames)


def install_programs():
    start_time = time.time()

    try:
        with open('/configs/programs.json') as json_data:
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
    start_time = time.time()

    files = get_file_list(config_name)

    for file in files:
        config("configs/" + file)

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
    # install_programs()

    # then do the adjustments
    configure_files(cmd.config_name)

    end_time_global = time.time()
    elapsed_time = round((end_time_global - start_time_global), 2)
    print("=====================================")
    print("It took " + str(elapsed_time) + " seconds to run script!")
