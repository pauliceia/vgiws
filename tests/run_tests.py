#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import exit as sys_exit, path as sys_path
from os import path as os_path

from unittest import TestLoader, TextTestRunner


# get the references to use faster
os_path_sep = os_path.sep
os_path_abspath = os_path.abspath

# Get the main folder (vgiws)
PROJECT_PATH = os_path_sep.join(os_path_abspath(__file__).split(os_path_sep)[:-2])
# Put the project path in sys path to use the folders (modules, settings, etc) as modules
sys_path.append(os_path_abspath(PROJECT_PATH))

# Get the current folder, where the run_tests.py is, to use the TestLoader
ROOT_PATH = os_path.dirname(__file__)


# Run the tests of the folder test/
if __name__ == '__main__':
    print("Running the tests \n")

    # Get all the files on current folder that has .py in the final
    tests = TestLoader().discover(ROOT_PATH, "*.py")
    # tests = TestLoader().discover(ROOT_PATH, "test_api_feature_table.py")

    # Run the tests - verbosity=2 increases the level of detail of output
    result = TextTestRunner(verbosity=2).run(tests)

    # If it has happened a problem, close the program
    if not result.wasSuccessful():
        sys_exit(1)
