#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create handlers.
"""

# call all controllers
from .controllers import *


# create a list with the classes that have the BaseHandler as Superclass
def get_subclasses_from_class(vars_class):
    """
        Use: get_subclasses_from_class(vars()['NAME_CLASS'])
        :param vars_class: vars()['NAME_CLASS']
        :return: list with subclasses in a dict form: {"class_name": "class_name", "class_instance": instance}
    """

    return [{"class_name": cls.__name__, "class_instance": cls} for cls in vars_class.__subclasses__()]

__LIST_BASEHANDLER_SUBCLASSES__ = get_subclasses_from_class(vars()['BaseHandler'])
