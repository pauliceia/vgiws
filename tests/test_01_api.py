#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from json import loads, dumps
from requests import get, put

from util.tester import UtilTester


# TODO: create cases of test:
# TODO: DELETE A ELEMENT WITH ID THAT DOESN'T EXIST

class TestAPIWihoutLogin(TestCase):
    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_get_api_create_changeset_without_login(self):
        # do a GET call
        response = put('http://localhost:8888/api/changeset/create/')

        self.assertEqual(response.status_code, 403)

        expected = {'status': 403, 'statusText': 'It needs a user looged to access this URL'}
        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_create_changeset_with_and_without_login(self):
        # DO LOGIN
        self.tester.do_login()

        # CREATE A CHANGESET
        changeset = {
            'changeset': {
                'tags': [{'k': 'created_by', 'v': 'test_api'},
                         {'k': 'comment', 'v': 'testing create changeset'}],
                'properties': {'id': -1, "fk_project_id": 1001}
            }
        }
        changeset = self.tester.create_changeset(changeset)

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
        node = self.tester.add_element(node)  # return the same element with the id generated

        # VERIFY IN DB, IF THE ELEMENTS EXIST
        self.tester.verify_if_element_was_add_in_db(node)

        # REMOVE THE ELEMENT CREATED
        self.tester.delete_element(node)

        # CLOSE THE CHANGESET
        self.tester.close_changeset(changeset)

        # DO LOGOUT
        self.tester.do_logout()

        ################################################################################
        # TRY TO CREATE ANOTHER CHANGESET WITHOUT LOGIN
        ################################################################################

        # do a GET call, sending a changeset to add in DB
        response = self.tester.session.put('http://localhost:8888/api/changeset/create/',
                                           data=dumps(changeset), headers=self.tester.headers)

        # it is not possible to create a changeset without login, so get a 403 Forbidden
        self.assertEqual(response.status_code, 403)


class TestAPI(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.do_login()

        # CREATE A PROJECT FOR ALL TESTS
        project = {
            'project': {
                'tags': [{'k': 'created_by', 'v': 'test_api'},
                         {'k': 'name', 'v': 'project of data'},
                         {'k': 'description', 'v': 'description of the project'}],
                'properties': {'id': -1}
            }
        }
        self.project = self.tester.create_project(project)

    def tearDown(self):
        # REMOVE THE PROJECT AFTER THE TESTS
        self.tester.delete_project(self.project)

        # DO LOGOUT AFTER THE TESTS
        self.tester.do_logout()

    def test_get_api_crud_elements_with_login(self):
        # get the id of project to use in create a changeset
        fk_project_id = self.project["project"]["properties"]["id"]

        # CREATE A CHANGESET
        # send a JSON with the changeset to create a new one
        changeset = {
            'changeset': {
                'tags': [{'k': 'created_by', 'v': 'test_api'},
                         {'k': 'comment', 'v': 'testing create changeset'}],
                'properties': {'id': -1, "fk_project_id": fk_project_id}
            }
        }
        changeset = self.tester.create_changeset(changeset)

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
        node = self.tester.add_element(node)  # return the same element with the id generated

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
        way = self.tester.add_element(way)

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
        area = self.tester.add_element(area)

        # VERIFY IN DB, IF THE ELEMENTS EXIST
        self.tester.verify_if_element_was_add_in_db(node)
        self.tester.verify_if_element_was_add_in_db(way)
        self.tester.verify_if_element_was_add_in_db(area)

        # REMOVE THE ELEMENTS CREATED
        self.tester.delete_element(node)
        self.tester.delete_element(way)
        self.tester.delete_element(area)

        # CLOSE THE CHANGESET
        self.tester.close_changeset(changeset)

    def test_get_api_crud_elements_that_not_exist_with_login(self):
        # get the id of project to use in create a changeset
        fk_project_id = self.project["project"]["properties"]["id"]

        # CREATE A CHANGESET
        # send a JSON with the changeset to create a new one
        changeset = {
            'changeset': {
                'tags': [{'k': 'created_by', 'v': 'test_api'},
                         {'k': 'comment', 'v': 'testing create changeset'}],
                'properties': {'id': -1, "fk_project_id": fk_project_id}
            }
        }
        changeset = self.tester.create_changeset(changeset)

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

        way = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'highway', 'v': 'residential'},
                             {'k': 'start_date', 'v': '1910-12-08'},
                             {'k': 'end_date', 'v': '1930-03-25'}],
                    'type': 'Feature',
                    'properties': {'id': -2, 'fk_changeset_id': fk_id_changeset},
                    'geometry': {
                        'type': 'MultiLineString',
                        'coordinates': [[[-54, 33], [-32, 31], [-36, 89]]]
                    },
                }
            ]
        }

        area = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'building', 'v': 'cathedral'},
                             {'k': 'start_date', 'v': '1900-11-12'},
                             {'k': 'end_date', 'v': '1915-12-25'}],
                    'type': 'Feature',
                    'properties': {'id': -3, 'fk_changeset_id': fk_id_changeset},
                    'geometry': {
                        'type': 'MultiPolygon',
                        'coordinates': [[[[-12, 32], [-23, 74], [-12, 32]]]]
                    },
                }
            ]
        }

        # VERIFY IN DB, IF THE ELEMENTS EXIST
        self.tester.verify_if_element_was_not_add_in_db(node)
        self.tester.verify_if_element_was_not_add_in_db(way)
        self.tester.verify_if_element_was_not_add_in_db(area)

        # CLOSE THE CHANGESET
        self.tester.close_changeset(changeset)


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
