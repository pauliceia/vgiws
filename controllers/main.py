#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create handlers.
"""


# call all controllers (DO NOT REMOVE IT)
from .controllers import *


# create a list with the classes that have the BaseHandler as Superclass
def get_subclasses_from_class(vars_class):
    """
        Use: get_subclasses_from_class(vars()['NAME_CLASS'])
        :param vars_class: vars()['NAME_CLASS']
        :return: list with subclasses in a dict form: {"class_name": "class_name", "class_instance": instance}
    """

    return [{"class_name": cls.__name__, "class_instance": cls} for cls in vars_class.__subclasses__()]


def get_subclasses_from_basehandlerx_classes():
    __LIST_BASEHANDLER_SUBCLASSES__ = []

    # get the variables inside the globals variable
    __vars__ = globals()

    for key in __vars__:
        # if exist a class that starts with BaseHandler (e.g. BaseHandler, BaseHandlerChangeset...)
        if key.startswith("BaseHandler"):
            # ... get its subclasses and extend in the list
            subclasses = get_subclasses_from_class(__vars__[key])
            __LIST_BASEHANDLER_SUBCLASSES__.extend(subclasses)

    return __LIST_BASEHANDLER_SUBCLASSES__


__LIST_BASEHANDLER_SUBCLASSES__ = get_subclasses_from_basehandlerx_classes()
