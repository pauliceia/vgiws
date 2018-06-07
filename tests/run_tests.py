#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sys import exit as sys_exit
from os import path as os_path
from unittest import TestLoader, TextTestRunner


# Current folder, where the run_tests.py is
ROOT_PATH = os_path.dirname(__file__)


# Roda os testes da pasta test/
if __name__ == '__main__':
    print("Running the tests \n")

    # Get all the files on current folder that has .py in the final
    tests = TestLoader().discover(ROOT_PATH, "*.py")
    # tests = TestLoader().discover(ROOT_PATH, "test_api_user_layer.py")

    # Run the tests - verbosity=2 increases the level of detail of output
    result = TextTestRunner(verbosity=2).run(tests)

    # If it has happened a problem, close the program
    if not result.wasSuccessful():
        sys_exit(1)
