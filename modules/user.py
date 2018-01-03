#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy


__USER_STRUCT_COOKIE__ = {
    # information of the user
    "user": {}
}


def get_new_user_struct_cookie():
    return deepcopy(__USER_STRUCT_COOKIE__)
