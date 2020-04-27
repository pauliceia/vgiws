#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path as os_path


# Get the `tests` folder path
TESTS_PATH = os_path.sep.join(os_path.abspath(__file__).split(os_path.sep)[:-2])
# Get the `files` folder path
FILES_PATH = '{}/files'.format(TESTS_PATH)


def by_multi_element_get_url_name(multi_element):
    if multi_element == "MultiPoint":
        return "point"
    if multi_element == "MultiLineString":
        return "line"
    if multi_element == "MultiPolygon":
        return "polygon"

    raise Exception("Invalid multi element: {0}".format(multi_element))


def get_url_arguments(**kwargs):
    list_of_arguments = []

    for key in kwargs:
        # it is necessary to exist a value for a key
        if kwargs[key] != "":
            list_of_arguments.append('{0}={1}'.format(key, kwargs[key]))

    # default: if there is no element, so put empty string
    arguments = ""

    if list_of_arguments:
        # if there are elements, put "?" + concat of arguments with "&"
        arguments = "?" + "&".join(list_of_arguments)

    return arguments
