#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase, skip
from util.tester import UtilTester


class TestAPI(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN BEFORE THE TESTS
        self.tester.auth_login_fake()

        # create a project
        project = {
            'type': 'Project',
            'properties': {'id': -1, 'fk_group_id': 1001},
            'tags': {'name': 'test project', 'url': 'http://somehost.com'}
        }
        self.project = self.tester.api_project_create(project)

        project_id = self.project["properties"]["id"]

        # CREATE A layer FOR ALL TESTS
        layer = {
            'tags': {'created_by': 'test_api', 'name': 'layer of data', 'description': 'description of the layer'},
            'properties': {'id': -1, 'fk_project_id': project_id},
            'type': 'Layer'
        }
        self.layer = self.tester.api_layer_create(layer)

    def tearDown(self):
        # get the id of layer to REMOVE it
        layer_id = self.layer["properties"]["id"]

        # REMOVE THE layer AFTER THE TESTS
        self.tester.api_layer_delete(layer_id)

        # get the id of feature to REMOVE it
        project_id = self.project["properties"]["id"]

        # REMOVE THE project AFTER THE TESTS
        self.tester.api_project_delete(project_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_crud_elements_with_login(self):
        # get the id of layer to use in create a changeset
        fk_layer_id = self.layer["properties"]["id"]

        # CREATE A CHANGESET
        changeset = {
            'tags': {'created_by': 'test_api', 'comment': 'testing create changeset'},
            'properties': {'id': -1, "fk_layer_id": fk_layer_id},
            'type': 'Changeset'
        }
        changeset = self.tester.api_changeset_create(changeset)

        # get the id of changeset to use in ADD element and CLOSE changeset
        changeset_id = changeset["properties"]["id"]

        # ADD ELEMENTS
        node = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': {'date': '1910', 'event': 'robbery'},
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
        way = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': {'end_date': '1930-03-25', 'highway': 'residential', 'start_date': '1910-12-08'},
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': changeset_id, 'version': 1, 'visible': True},
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
                    'tags': {'building': 'cathedral', 'end_date': '1915-12-25', 'start_date': '1900-11-12'},
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': changeset_id, 'version': 1, 'visible': True},
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
        self.tester.api_element_delete(node)
        self.tester.api_element_delete(way)
        self.tester.api_element_delete(area)

        # CLOSE THE CHANGESET
        self.tester.api_changeset_close(changeset_id)

        # DELETE THE CHANGESET
        self.tester.api_changeset_delete(changeset_id)

        # TRY TO ADD NEW ELEMENTS WITH THE CLOSED CHANGESET
        self.tester.api_element_create_error_409_conflict(node)
        self.tester.api_element_create_error_409_conflict(way)
        self.tester.api_element_create_error_409_conflict(area)

    def test_crud_elements_that_not_exist_with_login(self):
        # get the id of layer to use in create a changeset
        fk_layer_id = self.layer["properties"]["id"]

        # CREATE A CHANGESET
        # send a JSON with the changeset to create a new one
        changeset = {
            'tags': {'created_by': 'test_api', 'comment': 'testing create changeset'},
            'properties': {'id': -1, "fk_layer_id": fk_layer_id},
            'type': 'Changeset'
        }
        changeset = self.tester.api_changeset_create(changeset)

        # get the id of changeset to use in ADD element and CLOSE changeset
        changeset_id = changeset["properties"]["id"]

        # ADD ELEMENTS
        node = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': {'event': 'assault', 'date': '1912'},
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
                    'tags': {'highway': 'residential', 'start_date': '1914-02-18', 'end_date': '1927-03-21'},
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
                    'tags': {'building': 'church', 'start_date': '1880-03-30'},
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

        # DELETE THE CHANGESET
        self.tester.api_changeset_delete(changeset_id)


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
