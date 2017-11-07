#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from json import loads, dumps
from requests import get, Session


class TestAPI(TestCase):

    def test_get_api_create_changeset_without_login(self):
        # do a GET call
        response = get('http://localhost:8888/api/changeset/create/')

        self.assertEqual(response.status_code, 403)

        expected = {'status': 403, 'statusText': 'It needs a user looged to access this URL'}
        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_create_changeset_with_login(self):
        # create a session, simulating a browser. It is necessary to create cookies on server
        s = Session()

        ################################################################################
        # DO LOGIN
        ################################################################################

        response = s.get('http://localhost:8888/auth/login/fake/')

        self.assertEqual(response.status_code, 200)

        ################################################################################
        # CREATE A CHANGESET
        ################################################################################

        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

        # send a JSON with the changeset to create a new one
        changeset = {
            "plc": {
                'changeset': {
                    'tags': [{'k': 'created_by', 'v': 'test_api'},
                             {'k': 'comment', 'v': 'testing create changeset'}],
                    'properties': {'id': -1, "fk_project_id": 1001}
                }
            }
        }

        # do a GET call, sending a changeset to add in DB
        response = s.get('http://localhost:8888/api/changeset/create/', data=dumps(changeset), headers=headers)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertIn("id", resulted)
        self.assertNotEqual(resulted["id"], -1)

        # put the id received in the original JSON of changeset
        changeset["plc"]["changeset"]["properties"]["id"] = resulted["id"]

        # get the id of changeset to use
        fk_id_changeset = changeset["plc"]["changeset"]["properties"]["id"]

        ################################################################################
        # ADD A NODE
        ################################################################################

        # send a JSON with the node to create a new one
        node = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'tags': [{'k': 'event', 'v': 'robbery'},
                             {'k': 'date', 'v': '1910'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_id_changeset': fk_id_changeset,
                                   'version': 1},  # version = 1, because I'm adding in DB, so the node is new
                    'geometry': {
                        'type': 'MultiPoint',
                        'coordinates': [[-23.546421, -46.635722]],
                        'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"}
                    },
                }
            ]
        }

        # do a PUT call, sending a node to add in DB
        response = s.put('http://localhost:8888/api/node/create/', data=dumps(node), headers=headers)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertIn("id", resulted)
        self.assertNotEqual(resulted["id"], -1)

        # put the id received in the original JSON of node
        node["features"][0]["properties"]["id"] = resulted["id"]

        ################################################################################
        # ADD A WAY
        ################################################################################

        # send a JSON with the node to create a new one
        way = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'tags': [{'k': 'highway', 'v': 'residential'},
                             {'k': 'start_date', 'v': '1910-12-08'},
                             {'k': 'end_date', 'v': '1930-03-25'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_id_changeset': fk_id_changeset,
                                   'version': 1},  # version = 1, because I'm adding in DB, so the node is new
                    'geometry': {
                        'type': 'MultiLineString',
                        'coordinates': [[[-54, 33], [-32, 31], [-36, 89]]],
                        'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"}
                    },
                }
            ]
        }

        # do a PUT call, sending a node to add in DB
        response = s.put('http://localhost:8888/api/way/create/', data=dumps(way), headers=headers)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertIn("id", resulted)
        self.assertNotEqual(resulted["id"], -1)

        # put the id received in the original JSON of way
        way["features"][0]["properties"]["id"] = resulted["id"]

        ################################################################################
        # ADD A AREA
        ################################################################################

        # send a JSON with the node to create a new one
        area = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'tags': [{'k': 'building', 'v': 'cathedral'},
                             {'k': 'start_date', 'v': '1900-11-12'},
                             {'k': 'end_date', 'v': '1915-12-25'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_id_changeset': fk_id_changeset,
                                   'version': 1},  # version = 1, because I'm adding in DB, so the node is new
                    'geometry': {
                        'type': 'MultiPolygon',
                        'coordinates': [[[[-12, 32], [-23, 74], [-12, 32]]]],
                        'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"}
                    },
                }
            ]
        }

        # do a PUT call, sending a area to add in DB
        response = s.put('http://localhost:8888/api/area/create/', data=dumps(area), headers=headers)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertIn("id", resulted)
        self.assertNotEqual(resulted["id"], -1)

        # put the id received in the original JSON of area
        area["features"][0]["properties"]["id"] = resulted["id"]

        ################################################################################
        # CLOSE THE CHANGESET
        ################################################################################

        response = s.get('http://localhost:8888/api/changeset/close/{0}'.format(fk_id_changeset))

        self.assertEqual(response.status_code, 200)

        ################################################################################
        # DO LOGOUT
        ################################################################################

        response = s.get('http://localhost:8888/auth/logout')

        self.assertEqual(response.status_code, 200)

        ################################################################################
        # TRY TO CREATE ANOTHER CHANGESET WITHOUT LOGIN
        ################################################################################

        # do a GET call, sending a changeset to add in DB
        response = s.get('http://localhost:8888/api/changeset/create/', data=dumps(changeset), headers=headers)

        # it is not possible to create a changeset without login, so get a 403 Forbidden
        self.assertEqual(response.status_code, 403)




# TODO: create a test to remove the elements added


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
