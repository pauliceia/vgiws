#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from json import loads
from requests import get


class TestAPIWay(TestCase):

    def test_get_api_waye_return_all_elements_as_wkt(self):
        # do a GET call
        response = get('http://localhost:8888/api/way/?format=wkt')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = [
            {'fk_id_changeset': 1, 'id': 1, 'geom': 'MULTILINESTRING((333188.261004703 7395284.32488995,333205.817689791 7395247.71277836,333247.996555184 7395172.56160195,333261.133400433 7395102.3470075,333270.981533908 7395034.48052247,333277.885095545 7394986.25678192))'},
            {'fk_id_changeset': 2, 'id': 2, 'geom': 'MULTILINESTRING((333270.653184563 7395036.74327773,333244.47769325 7395033.35326418,333204.141105934 7395028.41654752,333182.467715735 7395026.2492085))'}
        ]

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_way_return_all_elements_as_geojson(self):

        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'geometry': {'type': 'MultiLineString', 'coordinates': [[[333188.261004703, 7395284.32488995], [333205.817689791, 7395247.71277836], [333247.996555184, 7395172.56160195], [333261.133400433, 7395102.3470075], [333270.981533908, 7395034.48052247], [333277.885095545, 7394986.25678192]]]},
                    'tags': [{'k': 'name', 'id': 1, 'v': 'rua boa vista'},
                             {'k': 'start_date', 'id': 2, 'v': '1930'},
                             {'k': 'end_date', 'id': 3, 'v': '1930'}],
                    'type': 'Feature',
                    'properties': {'fk_id_changeset': 1, 'id': 1}
                },
                {
                    'geometry': {'type': 'MultiLineString', 'coordinates': [[[333270.653184563, 7395036.74327773], [333244.47769325, 7395033.35326418], [333204.141105934, 7395028.41654752], [333182.467715735, 7395026.2492085]]]},
                    'tags': [{'k': 'address', 'id': 4, 'v': 'rua tres de dezembro'},
                             {'k': 'start_date', 'id': 5, 'v': '1930'},
                             {'k': 'end_date', 'id': 6, 'v': '1930'}],
                    'type': 'Feature',
                    'properties': {'fk_id_changeset': 2, 'id': 2}
                }
            ]
        }

        # do a GET call with default format (GeoJSON)
        response = get('http://localhost:8888/api/way/')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

        # do a GET call putting explicit GeoJSON format
        response = get('http://localhost:8888/api/way/?format=geojson')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_way_return_element_with_id_1_as_wkt(self):
        # do a GET call
        response = get('http://localhost:8888/api/way/?q=[id=1]&format=wkt')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = [
            {'id': 1, 'fk_id_changeset': 1, 'geom': 'MULTILINESTRING((333188.261004703 7395284.32488995,333205.817689791 7395247.71277836,333247.996555184 7395172.56160195,333261.133400433 7395102.3470075,333270.981533908 7395034.48052247,333277.885095545 7394986.25678192))'}
        ]

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_way_return_element_with_id_1_as_geojson(self):
        # do a GET call
        response = get('http://localhost:8888/api/way/?q=[id=1]')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = {
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {'coordinates': [[[333188.261004703, 7395284.32488995], [333205.817689791, 7395247.71277836], [333247.996555184, 7395172.56160195], [333261.133400433, 7395102.3470075], [333270.981533908, 7395034.48052247], [333277.885095545, 7394986.25678192]]], 'type': 'MultiLineString'},
                    'tags': [{'v': 'rua boa vista', 'k': 'name', 'id': 1},
                             {'v': '1930', 'k': 'start_date', 'id': 2},
                             {'v': '1930', 'k': 'end_date', 'id': 3}],
                    'properties': {'id': 1, 'fk_id_changeset': 1}
                }
            ],
            'type': 'FeatureCollection'
        }

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
