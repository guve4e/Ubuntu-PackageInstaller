#!/usr/bin/python3
import json
import time

from src.package import Package
from src.config_file import ConfigurationFile

def install_programs():
    start_time = time.time()

    try:
        with open('/jsonfiles/programs.json') as json_data:
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
    php = ConfigurationFile("jsonfiles/php.json")
    php.configure()


def config_apache():
    pass

def config_mysql():
    pass

def config_git():
    pass

if __name__ == "__main__":

    start_time_global = time.time()

    # install packages first
    #install_programs()

    # then do the adjustments

    # start by adjusting the
    # php configuration file
    config_php()
    config_apache()
    config_mysql()
    config_git()


    end_time_global = time.time()
    elapsed_time = round((end_time_global - start_time_global), 2)
    print("=====================================")
    print("It took " + str(elapsed_time) + " seconds to run script!")
