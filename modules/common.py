#!/usr/bin/env python
# -*- coding: utf-8 -*-


from datetime import datetime


def get_current_datetime(formatted=True):
    now = datetime.now()

    if formatted:
        now = now.strftime("%Y-%m-%d %H:%M")

    return now



# from copy import deepcopy
#
#
# __CHANGESET_STRUCT_COOKIE__ = {
#     # information of the user
#     "changeset": {
#         "created_at": "",
#         "closed_at": "",
#         "changes": {
#             "create": {
#                 'type': 'FeatureCollection',
#                 'features': [
#                     # list of features/elements to create, example:
#                     # {
#                     #     'tags': [{'v': 'R. São José', 'k': 'address'},
#                     #              {'v': '1869', 'k': 'start_date'},
#                     #              {'v': '1869', 'k': 'end_date'}],
#                     #     'type': 'Feature',
#                     #     'properties': {},
#                     #     'geometry': {'type': 'MultiPoint', 'coordinates': [[-23.546421, -46.635722]]}
#                     # }
#                 ]
#             },
#             "modify": {
#                 'type': 'FeatureCollection',
#                 'features': [
#                     # list of features/elements to update/modify, example:
#                     # {
#                     #     'tags': [{'id': 1001, 'v': 'R. São José', 'k': 'address'},
#                     #              {'id': 1002, 'v': '1869', 'k': 'start_date'},
#                     #              {'id': 1003, 'v': '1869', 'k': 'end_date'}],
#                     #     'type': 'Feature',
#                     #     'properties': {'id': 1001},
#                     #     'geometry': {'type': 'MultiPoint', 'coordinates': [[-23.546421, -46.635722]]}
#                     # }
#                 ]
#             },
#             "delete": {
#                 'type': 'FeatureCollection',
#                 'features': [
#                     # list of features/elements to delete/remove, example:
#                     # {
#                     #     'tags': [{'id': 1001, 'v': 'R. São José', 'k': 'address'},
#                     #              {'id': 1002, 'v': '1869', 'k': 'start_date'},
#                     #              {'id': 1003, 'v': '1869', 'k': 'end_date'}],
#                     #     'type': 'Feature',
#                     #     'properties': {'id': 1001},
#                     #     'geometry': {'type': 'MultiPoint', 'coordinates': [[-23.546421, -46.635722]]}
#                     # }
#                 ]
#             }
#         }
#     }
# }
#
# def get_new_changeset_struct_cookie():
#     return deepcopy(__CHANGESET_STRUCT_COOKIE__)
