#!/usr/bin/env python
# -*- coding: utf-8 -*-


def is_a_invalid_id(feature_id):
    """
    Verify if the id of some feature is valid or not.
    For a id to be valid, it needs to be:
        (1) not None; (2) a integer (a digit); (3) if is a integer, so different of 0.
    IDs are integer numbers greater than zero.
    :param feature_id: id of a feature in string format.
    :return: if id is invalid, return True, else False
    """
    return (feature_id is not None and not feature_id.isdigit()) or \
           (feature_id is not None and feature_id.isdigit() and feature_id == "0")


def are_arguments_valid_to_get_elements(**arguments):
    # the ids are just valid if there are numbers
    if "element_id" in arguments and is_a_invalid_id(arguments["element_id"]):
        return False
    elif "project_id" in arguments and is_a_invalid_id(arguments["project_id"]):
        return False
    elif "changeset_id" in arguments and is_a_invalid_id(arguments["changeset_id"]):
        return False
    else:
        return True
