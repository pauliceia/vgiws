#!/usr/bin/env python
# -*- coding: utf-8 -*-


from json import loads, dumps
from requests import Session


class UtilTester:

    def __init__(self, ut_self):
        # create a session, simulating a browser. It is necessary to create cookies on server
        self.session = Session()
        # headers
        self.headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        # unittest self
        self.ut_self = ut_self

    def do_login(self):
        response = self.session.get('http://localhost:8888/auth/login/fake/')

        self.ut_self.assertEqual(response.status_code, 200)

    def do_logout(self):
        response = self.session.get('http://localhost:8888/auth/logout')

        self.ut_self.assertEqual(response.status_code, 200)

    def create_a_changeset(self):
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
        response = self.session.get('http://localhost:8888/api/changeset/create/',
                                    data=dumps(changeset), headers=self.headers)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertIn("id", resulted)
        self.ut_self.assertNotEqual(resulted["id"], -1)

        # put the id received in the original JSON of changeset
        changeset["plc"]["changeset"]["properties"]["id"] = resulted["id"]

        return changeset

    def close_a_changeset(self, fk_id_changeset):
        response = self.session.get('http://localhost:8888/api/changeset/close/{0}'.format(fk_id_changeset))

        self.ut_self.assertEqual(response.status_code, 200)

    def add_a_node(self, fk_id_changeset):
        # send a JSON with the node to create a new one
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

        # do a PUT call, sending a node to add in DB
        response = self.session.put('http://localhost:8888/api/node/create/',
                                    data=dumps(node), headers=self.headers)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertIn("id", resulted)
        self.ut_self.assertNotEqual(resulted["id"], -1)

        # put the id received in the original JSON of node
        node["features"][0]["properties"]["id"] = resulted["id"]

        return node

    def add_a_way(self, fk_id_changeset):
        # send a JSON with the node to create a new one
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

        # do a PUT call, sending a node to add in DB
        response = self.session.put('http://localhost:8888/api/way/create/',
                                    data=dumps(way), headers=self.headers)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertIn("id", resulted)
        self.ut_self.assertNotEqual(resulted["id"], -1)

        # put the id received in the original JSON of way
        way["features"][0]["properties"]["id"] = resulted["id"]

        return way

    def add_a_area(self, fk_id_changeset):
        # send a JSON with the node to create a new one
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

        # do a PUT call, sending a area to add in DB
        response = self.session.put('http://localhost:8888/api/area/create/',
                                    data=dumps(area), headers=self.headers)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.ut_self.assertIn("id", resulted)
        self.ut_self.assertNotEqual(resulted["id"], -1)

        # put the id received in the original JSON of area
        area["features"][0]["properties"]["id"] = resulted["id"]

        return area

    def delete_element(self, element, id_element):
        response = self.session.delete('http://localhost:8888/api/{0}/?q=[id={1}]'.format(element, id_element))

        self.ut_self.assertEqual(response.status_code, 200)
