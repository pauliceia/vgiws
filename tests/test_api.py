#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from json import loads
from requests import get


class TestAPI(TestCase):

    def test_get_api_node_return_all_elements_as_wkt(self):
        # do a GET call
        response = get('http://localhost:8888/api/node/?format=wkt')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = [
            {'fk_id_changeset': 1, 'geom': 'MULTIPOINT(-23.546421 -46.635722)', 'id': 1},
            {'fk_id_changeset': 2, 'geom': 'MULTIPOINT(-23.55045 -46.634272)', 'id': 2}
        ]

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_node_return_all_elements_as_geojson(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'fk_id_changeset': 1, 'id': 1},
                    'geometry': {'coordinates': [[-23.546421, -46.635722]], 'type': 'MultiPoint'},
                    'tags': [{'v': 'R. São José', 'k': 'address', 'id': 1},
                             {'v': '1869', 'k': 'start_date', 'id': 2},
                             {'v': '1869', 'k': 'end_date', 'id': 3}],
                    'type': 'Feature'
                },
                {
                    'properties': {'fk_id_changeset': 2, 'id': 2},
                    'geometry': {'coordinates': [[-23.55045, -46.634272]], 'type': 'MultiPoint'},
                    'tags': [{'v': 'R. Marechal Deodoro', 'k': 'address', 'id': 4},
                             {'v': '1878', 'k': 'start_date', 'id': 5},
                             {'v': '1910', 'k': 'end_date', 'id': 6}],
                    'type': 'Feature'}
            ]
        }

        # do a GET call with default format (GeoJSON)
        response = get('http://localhost:8888/api/node/')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

        # do a GET call putting explicit GeoJSON format
        response = get('http://localhost:8888/api/node/?format=geojson')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_node_return_element_with_id_1_as_wkt(self):
        # do a GET call
        response = get('http://localhost:8888/api/node/?q=[id=1]&format=wkt')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = [
            {'id': 1, 'geom': 'MULTIPOINT(-23.546421 -46.635722)', 'fk_id_changeset': 1}
        ]

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_node_return_element_with_id_1_as_geojson(self):
        # do a GET call
        response = get('http://localhost:8888/api/node/?q=[id=1]')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'tags': [{'id': 1, 'v': 'R. São José', 'k': 'address'},
                             {'id': 2, 'v': '1869', 'k': 'start_date'},
                             {'id': 3, 'v': '1869', 'k': 'end_date'}],
                    'type': 'Feature',
                    'properties': {'id': 1, 'fk_id_changeset': 1},
                    'geometry': {'type': 'MultiPoint', 'coordinates': [[-23.546421, -46.635722]]}
                }
            ]
        }

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
