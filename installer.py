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


def get_file_list(dir_path):
    """
    Retrieves the names of files in
    certain directory.
    :param dir_path:
    :return:
    """
    files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    # we need only json files
    files = filter(lambda k: '.json' in k, files)

    return list(files)

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


def config_php():
    """
    Configures the php ini file.
    Loads json file with new
    configurations.
    :return: void
    """
    php = ConfigurationFile("configs/php.json")
    php.configure()


def config_apache():
    php = ConfigurationFile("configs/apache.json")
    php.configure()


def config_mysql():
    php = ConfigurationFile("configs/mysql.json")
    php.configure()

if __name__ == "__main__":

    start_time_global = time.time()

    #cmd = CmdArgumentsParser(sys.argv)
    conf_name = "home"

    dir = os.path.dirname(__file__)

    filename = os.path.join(dir, "configs", conf_name)


    files = get_file_list(filename)

    ## loop trough all of them and
    ## call a generic method passing a path


    # install packages first
    #install_programs()

    # then do the adjustments
    # config_php()
    # config_apache()
    # config_mysql()

    end_time_global = time.time()
    elapsed_time = round((end_time_global - start_time_global), 2)
    print("=====================================")
    print("It took " + str(elapsed_time) + " seconds to run script!")
