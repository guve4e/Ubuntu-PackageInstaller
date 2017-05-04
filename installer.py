#!/usr/bin/python3
import json
import time
from Package import Package


if __name__ == "__main__":

    start_time = time.time()

    try:
        with open('programs.json') as json_data:
            # load json
            programs = json.load(json_data)
            # parse json
            Package.parse(programs)

    except IOError as e:
        print(e.strerror)

    end_time = time.time()
    elapsed_time = round((end_time - start_time), 2)
    print("=====================================")
    print("It took " + str(elapsed_time) + " seconds to run script!")
