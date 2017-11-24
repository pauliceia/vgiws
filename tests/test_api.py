#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


class TestAPI(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login()

        # CREATE A PROJECT FOR ALL TESTS
        project = {
            'project': {
                'tags': [{'k': 'created_by', 'v': 'test_api'},
                         {'k': 'name', 'v': 'project of data'},
                         {'k': 'description', 'v': 'description of the project'}],
                'properties': {'id': -1}
            }
        }
        self.project = self.tester.api_project_create(project)

    def tearDown(self):
        # get the id of project to REMOVE it
        project_id = self.project["project"]["properties"]["id"]

        # REMOVE THE PROJECT AFTER THE TESTS
        self.tester.api_project_delete(project_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_crud_elements_with_login(self):
        # get the id of project to use in create a changeset
        fk_project_id = self.project["project"]["properties"]["id"]

        # CREATE A CHANGESET
        changeset = {
            'changeset': {
                'tags': [{'k': 'created_by', 'v': 'test_api'},
                         {'k': 'comment', 'v': 'testing create changeset'}],
                'properties': {'id': -1, "fk_project_id": fk_project_id}
            }
        }
        changeset = self.tester.api_changeset_create(changeset)

        # get the id of changeset to use in ADD element and CLOSE changeset
        changeset_id = changeset["changeset"]["properties"]["id"]

        # ADD ELEMENTS
        node = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'event', 'v': 'robbery'},
                             {'k': 'date', 'v': '1910'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': changeset_id},
                    'geometry': {
                        'type': 'MultiPoint',
                        'coordinates': [[-23.546421, -46.635722]]
                    },
                }
            ]
        }
        node = self.tester.api_element_create(node)  # return the same element with the id generated
        way = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'highway', 'v': 'residential'},
                             {'k': 'start_date', 'v': '1910-12-08'},
                             {'k': 'end_date', 'v': '1930-03-25'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': changeset_id},
                    'geometry': {
                        'type': 'MultiLineString',
                        'coordinates': [[[-54, 33], [-32, 31], [-36, 89]]]
                    },
                }
            ]
        }
        way = self.tester.api_element_create(way)
        area = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'building', 'v': 'cathedral'},
                             {'k': 'start_date', 'v': '1900-11-12'},
                             {'k': 'end_date', 'v': '1915-12-25'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': changeset_id},
                    'geometry': {
                        'type': 'MultiPolygon',
                        'coordinates': [[[[-12, 32], [-23, 74], [-12, 32]]]]
                    },
                }
            ]
        }
        area = self.tester.api_element_create(area)

        # VERIFY IN DB, IF THE ELEMENTS EXIST
        self.tester.verify_if_element_was_add_in_db(node)
        self.tester.verify_if_element_was_add_in_db(way)
        self.tester.verify_if_element_was_add_in_db(area)

        # REMOVE THE ELEMENTS CREATED
        element_id = node["features"][0]["properties"]["id"]  # get the id of element
        self.tester.api_element_delete("node", element_id=element_id)
        element_id = way["features"][0]["properties"]["id"]  # get the id of element
        self.tester.api_element_delete("way", element_id=element_id)
        element_id = area["features"][0]["properties"]["id"]  # get the id of element
        self.tester.api_element_delete("area", element_id=element_id)

        # CLOSE THE CHANGESET
        self.tester.api_changeset_close(changeset_id)

        # TRY TO ADD NEW ELEMENTS WITH THE CLOSED CHANGESET
        self.tester.api_element_create_error_400_bad_request(node)
        self.tester.api_element_create_error_400_bad_request(way)
        self.tester.api_element_create_error_400_bad_request(area)

    def test_crud_elements_that_not_exist_with_login(self):
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
        changeset = self.tester.api_changeset_create(changeset)

        # get the id of changeset to use in ADD element and CLOSE changeset
        changeset_id = changeset["changeset"]["properties"]["id"]

        # ADD ELEMENTS
        node = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'event', 'v': 'assault'},
                             {'k': 'date', 'v': '1912'}],
                    'type': 'Feature',
                    'properties': {'id': 5000, 'fk_changeset_id': changeset_id},
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
                             {'k': 'start_date', 'v': '1914-02-18'},
                             {'k': 'end_date', 'v': '1927-03-21'}],
                    'type': 'Feature',
                    'properties': {'id': 5001, 'fk_changeset_id': changeset_id},
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
                    'tags': [{'k': 'building', 'v': 'church'},
                             {'k': 'start_date', 'v': '1880-03-30'}],
                    'type': 'Feature',
                    'properties': {'id': 5002, 'fk_changeset_id': changeset_id},
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
        self.tester.api_changeset_close(changeset_id)


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
