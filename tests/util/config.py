#!/usr/bin/env python
# -*- coding: utf-8 -*-


from sys import path as sys_path
from os import path as os_path

# get the reference of the function (to be faster)
sys_path_append = sys_path.append
os_path_abspath = os_path.abspath

# Folder before the current folder (root of project)
ROOT_PROJECT_PATH = os_path.sep.join(os_path.abspath(__file__).split(os_path.sep)[:-3])

# add in sys.path the root folder to can import modules outside of test folder
sys_path_append(os_path_abspath(ROOT_PROJECT_PATH))
