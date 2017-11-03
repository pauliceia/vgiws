#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from json import loads
from requests import get


class TestAPIArea(TestCase):

    def test_get_api_area_return_all_elements_as_wkt(self):
        # do a GET call
        response = get('http://localhost:8888/api/area/?format=wkt')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = [
            {'id': 1, 'fk_id_changeset': 1, 'geom': 'MULTIPOLYGON(((0 0,1 1,2 2,3 3,0 0)))'},
            {'id': 2, 'fk_id_changeset': 2, 'geom': 'MULTIPOLYGON(((2 2,3 3,4 4,5 5,2 2)))'}
        ]

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_area_return_all_elements_as_geojson(self):

        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'tags': [{'id': 1, 'v': 'hotel', 'k': 'building'},
                             {'id': 2, 'v': '1870', 'k': 'start_date'},
                             {'id': 3, 'v': '1900', 'k': 'end_date'}],
                    'type': 'Feature',
                    'geometry': {'type': 'MultiPolygon', 'coordinates': [[[[0, 0], [1, 1], [2, 2], [3, 3], [0, 0]]]]},
                    'properties': {'id': 1, 'fk_id_changeset': 1}
                },
                {
                    'tags': [{'id': 4, 'v': 'theater', 'k': 'building'},
                             {'id': 5, 'v': '1920', 'k': 'start_date'},
                             {'id': 6, 'v': '1930', 'k': 'end_date'}],
                    'type': 'Feature',
                    'geometry': {'type': 'MultiPolygon', 'coordinates': [[[[2, 2], [3, 3], [4, 4], [5, 5], [2, 2]]]]},
                    'properties': {'id': 2, 'fk_id_changeset': 2}
                }
            ]
        }

        # do a GET call with default format (GeoJSON)
        response = get('http://localhost:8888/api/area/')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

        # do a GET call putting explicit GeoJSON format
        response = get('http://localhost:8888/api/area/?format=geojson')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_area_return_element_with_id_1_as_wkt(self):
        # do a GET call
        response = get('http://localhost:8888/api/area/?q=[id=1]&format=wkt')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = [
            {'geom': 'MULTIPOLYGON(((0 0,1 1,2 2,3 3,0 0)))', 'fk_id_changeset': 1, 'id': 1}
        ]

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_area_return_element_with_id_1_as_geojson(self):
        # do a GET call
        response = get('http://localhost:8888/api/area/?q=[id=1]')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = {
            'features': [
                {
                    'properties': {'id': 1, 'fk_id_changeset': 1},
                    'tags': [{'k': 'building', 'v': 'hotel', 'id': 1},
                             {'k': 'start_date', 'v': '1870', 'id': 2},
                             {'k': 'end_date', 'v': '1900', 'id': 3}],
                    'geometry': {'type': 'MultiPolygon', 'coordinates': [[[[0, 0], [1, 1], [2, 2], [3, 3], [0, 0]]]]},
                    'type': 'Feature'
                }
            ],
            'type': 'FeatureCollection'
        }

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
