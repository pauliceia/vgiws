#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase

from json import dumps
from requests import put

from util.tester import UtilTester


class TestAPIWihoutLogin(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_do_operations_without_persmission(self):
        # CREATE A CHANGESET
        # send a JSON with the changeset to create a new one
        changeset = {
            'tags': {'created_by': 'test_api', 'comment': 'testing create changeset'},
            'properties': {'id': 1500, "fk_layer_id": 1500},
            'type': 'Changeset'
        }
        self.tester.api_changeset_create_error_403_forbidden(changeset)

        # get the id of changeset to use in ADD element and CLOSE changeset
        changeset_id = changeset["properties"]["id"]

        # ADD ELEMENTS
        node = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'date', 'v': '1910'}, {'k': 'event', 'v': 'robbery'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': changeset_id, 'version': 1, 'visible': True},
                    'geometry': {
                        'type': 'MultiPoint',
                        'coordinates': [[-23.546421, -46.635722]]
                    },
                }
            ]
        }
        self.tester.api_element_create_error_403_forbidden(node)  # return the same element with the id generated

        way = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'end_date', 'v': '1930-03-25'},
                             {'k': 'highway', 'v': 'residential'},
                             {'k': 'start_date', 'v': '1910-12-08'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': changeset_id, 'version': 1, 'visible': True},
                    'geometry': {
                        'type': 'MultiLineString',
                        'coordinates': [[[-54, 33], [-32, 31], [-36, 89]]]
                    },
                }
            ]
        }
        self.tester.api_element_create_error_403_forbidden(way)

        area = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'building', 'v': 'cathedral'},
                             {'k': 'end_date', 'v': '1915-12-25'},
                             {'k': 'start_date', 'v': '1900-11-12'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': changeset_id, 'version': 1, 'visible': True},
                    'geometry': {
                        'type': 'MultiPolygon',
                        'coordinates': [[[[-12, 32], [-23, 74], [-12, 32]]]]
                    },
                }
            ]
        }
        self.tester.api_element_create_error_403_forbidden(area)

        # REMOVE THE ELEMENTS CREATED
        element_id = node["features"][0]["properties"]["id"]  # get the id of element
        self.tester.api_element_delete_error_403_forbidden("point", element_id=element_id)
        element_id = way["features"][0]["properties"]["id"]  # get the id of element
        self.tester.api_element_delete_error_403_forbidden("line", element_id=element_id)
        element_id = area["features"][0]["properties"]["id"]  # get the id of element
        self.tester.api_element_delete_error_403_forbidden("polygon", element_id=element_id)

        # CLOSE THE CHANGESET
        self.tester.api_changeset_close_error_403_forbidden(changeset_id)

    def test_api_changeset_create_and_close_without_login(self):
        # do a GET call
        changeset = {
            'tags': {'comment': 'testing create changeset', 'created_by': 'test_api'},
            'properties': {'id': 1700, "fk_layer_id": 1700},
            'type': 'Changeset'
        }
        self.tester.api_changeset_create_error_403_forbidden(changeset)

        # get the id of changeset to CLOSE changeset
        changeset_id = changeset["properties"]["id"]

        self.tester.api_changeset_close_error_403_forbidden(changeset_id)

    def test_api_create_changeset_with_and_without_login(self):
            # DO LOGIN
            self.tester.auth_login_fake()

            # CREATE A CHANGESET
            changeset = {
                'tags': {'comment': 'testing create changeset', 'created_by': 'test_api'},
                'properties': {'id': -1, "fk_layer_id": 1003},
                'type': 'Changeset'
            }
            changeset = self.tester.api_changeset_create(changeset)

            # get the id of changeset to use in ADD element and CLOSE changeset
            changeset_id = changeset["properties"]["id"]

            # ADD ELEMENT
            node = {
                'type': 'FeatureCollection',
                'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
                'features': [
                    {
                        'tags': [{'k': 'date', 'v': '1910'}, {'k': 'event', 'v': 'robbery'}],
                        'type': 'Feature',
                        'properties': {'id': -1, 'fk_changeset_id': changeset_id, 'version': 1, 'visible': True},
                        'geometry': {
                            'type': 'MultiPoint',
                            'coordinates': [[-23.546421, -46.635722]]
                        },
                    }
                ]
            }
            node = self.tester.api_element_create(node)  # return the same element with the id generated

            # VERIFY IN DB, IF THE ELEMENTS EXIST
            self.tester.verify_if_element_was_add_in_db(node)

            # REMOVE THE ELEMENT CREATED
            self.tester.api_element_delete(node)

            # CLOSE THE CHANGESET
            self.tester.api_changeset_close(changeset_id)

            # DELETE THE CHANGESET
            self.tester.api_changeset_delete(changeset_id)

            # DO LOGOUT
            self.tester.auth_logout()

            ################################################################################
            # TRY TO CREATE ANOTHER CHANGESET WITHOUT LOGIN
            ################################################################################

            self.tester.api_changeset_create_error_403_forbidden(changeset)


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
