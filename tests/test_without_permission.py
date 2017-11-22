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
            'changeset': {
                'tags': [{'k': 'created_by', 'v': 'test_api'},
                         {'k': 'comment', 'v': 'testing create changeset'}],
                'properties': {'id': 1500, "fk_project_id": 1500}
            }
        }
        self.tester.api_changeset_create_without_permission(changeset)

        # get the id of changeset to use in ADD element and CLOSE changeset
        fk_id_changeset = changeset["changeset"]["properties"]["id"]

        # ADD ELEMENTS
        node = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'event', 'v': 'robbery'},
                             {'k': 'date', 'v': '1910'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': fk_id_changeset},
                    'geometry': {
                        'type': 'MultiPoint',
                        'coordinates': [[-23.546421, -46.635722]]
                    },
                }
            ]
        }
        self.tester.api_element_create_without_permission(node)  # return the same element with the id generated

        way = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'highway', 'v': 'residential'},
                             {'k': 'start_date', 'v': '1910-12-08'},
                             {'k': 'end_date', 'v': '1930-03-25'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': fk_id_changeset},
                    'geometry': {
                        'type': 'MultiLineString',
                        'coordinates': [[[-54, 33], [-32, 31], [-36, 89]]]
                    },
                }
            ]
        }
        self.tester.api_element_create_without_permission(way)

        area = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'building', 'v': 'cathedral'},
                             {'k': 'start_date', 'v': '1900-11-12'},
                             {'k': 'end_date', 'v': '1915-12-25'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': fk_id_changeset},
                    'geometry': {
                        'type': 'MultiPolygon',
                        'coordinates': [[[[-12, 32], [-23, 74], [-12, 32]]]]
                    },
                }
            ]
        }
        self.tester.api_element_create_without_permission(area)

        # REMOVE THE ELEMENTS CREATED
        self.tester.api_element_delete_without_persmission(node)
        self.tester.api_element_delete_without_persmission(way)
        self.tester.api_element_delete_without_persmission(area)

        # CLOSE THE CHANGESET
        self.tester.api_changeset_close_without_permission(changeset)

    def test_api_changeset_create_and_close_without_login(self):
        # do a GET call
        changeset = {
            'changeset': {
                'tags': [{'k': 'created_by', 'v': 'test_api'},
                         {'k': 'comment', 'v': 'testing create changeset'}],
                'properties': {'id': 1700, "fk_project_id": 1700}
            }
        }
        self.tester.api_changeset_create_without_permission(changeset)

        self.tester.api_changeset_close_without_permission(changeset)

    def test_api_create_changeset_with_and_without_login(self):
            # DO LOGIN
            self.tester.auth_login()

            # CREATE A CHANGESET
            changeset = {
                'changeset': {
                    'tags': [{'k': 'created_by', 'v': 'test_api'},
                             {'k': 'comment', 'v': 'testing create changeset'}],
                    'properties': {'id': -1, "fk_project_id": 1001}
                }
            }
            changeset = self.tester.api_changeset_create(changeset)

            # get the id of changeset to use in ADD element and CLOSE changeset
            fk_id_changeset = changeset["changeset"]["properties"]["id"]

            # ADD ELEMENT
            node = {
                'type': 'FeatureCollection',
                'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
                'features': [
                    {
                        'tags': [{'k': 'event', 'v': 'robbery'},
                                 {'k': 'date', 'v': '1910'}],
                        'type': 'Feature',
                        'properties': {'id': -1, 'fk_changeset_id': fk_id_changeset},
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
            self.tester.api_changeset_close(changeset)

            # DO LOGOUT
            self.tester.auth_logout()

            ################################################################################
            # TRY TO CREATE ANOTHER CHANGESET WITHOUT LOGIN
            ################################################################################

            # do a GET call, sending a changeset to add in DB
            response = self.tester.session.put('http://localhost:8888/api/changeset/create/',
                                               data=dumps(changeset), headers=self.tester.headers)

            # it is not possible to create a changeset without login, so get a 403 Forbidden
            self.assertEqual(response.status_code, 403)


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
