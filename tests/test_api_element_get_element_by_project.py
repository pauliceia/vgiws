#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/

class TestAPIGETElementByProjectAndChangeset(TestCase):

    # TODO: CREATE A INVALID TEST -         arguments.append('abc=123')

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    ################################################################################
    # NODE
    ################################################################################

    def test_get_api_element_return_all_elements_by_project_id(self):
        expected = {
            'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'fk_changeset_id': 1001, 'id': 1001},
                    'type': 'Feature',
                    'geometry': {'coordinates': [[-23.546421, -46.635722]], 'type': 'MultiPoint'},
                    'tags': [{'k': 'address', 'v': 'R. São José'},
                             {'k': 'start_date', 'v': '1869'},
                             {'k': 'end_date', 'v': '1869'}]
                },
                {
                    'properties': {'fk_changeset_id': 1003, 'id': 1006},
                    'type': 'Feature',
                    'geometry': {'coordinates': [[-54, 33]], 'type': 'MultiPoint'},
                    'tags': None
                }
            ]
        }

        self.tester.api_element("node", expected, project_id="1001")

        expected = {
            'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
            'type': 'FeatureCollection',
            'features': [
                {
                    'tags': [{'k': 'name', 'v': 'rua boa vista'},
                             {'k': 'start_date', 'v': '1930'},
                             {'k': 'end_date', 'v': '1930'}],
                    'type': 'Feature',
                    'geometry': {'type': 'MultiLineString', 'coordinates': [[[333188.261004703, 7395284.32488995], [333205.817689791, 7395247.71277836], [333247.996555184, 7395172.56160195], [333261.133400433, 7395102.3470075], [333270.981533908, 7395034.48052247], [333277.885095545, 7394986.25678192]]]},
                    'properties': {'fk_changeset_id': 1001, 'id': 1001}
                }
            ]
        }

        self.tester.api_element("way", expected, project_id="1001")

        expected = {
            'crs': {'properties': {'name': 'EPSG:4326'}, 'type': 'name'},
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'id': 1001, 'fk_changeset_id': 1001},
                    'type': 'Feature',
                    'tags': [{'v': 'hotel', 'k': 'building'},
                             {'v': '1870', 'k': 'start_date'},
                             {'v': '1900', 'k': 'end_date'}],
                    'geometry': {'type': 'MultiPolygon', 'coordinates': [[[[0, 0], [1, 1], [2, 2], [3, 3], [0, 0]]]]}
                }
            ]
        }

        self.tester.api_element("area", expected, project_id="1001")

    def test_get_api_element_return_all_elements_by_changeset_id(self):
        expected = {
            'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'fk_changeset_id': 1001, 'id': 1001},
                    'type': 'Feature',
                    'geometry': {'coordinates': [[-23.546421, -46.635722]], 'type': 'MultiPoint'},
                    'tags': [{'k': 'address', 'v': 'R. São José'},
                             {'k': 'start_date', 'v': '1869'},
                             {'k': 'end_date', 'v': '1869'}]
                }
            ]
        }

        self.tester.api_element("node", expected, changeset_id="1001")

        expected = {
            'type': 'FeatureCollection',
            'crs': {'properties': {'name': 'EPSG:4326'}, 'type': 'name'},
            'features': [
                {
                    'properties': {'id': 1001, 'fk_changeset_id': 1001},
                    'tags': [{'k': 'name', 'v': 'rua boa vista'},
                             {'k': 'start_date', 'v': '1930'},
                             {'k': 'end_date', 'v': '1930'}],
                    'geometry': {'type': 'MultiLineString', 'coordinates': [[[333188.261004703, 7395284.32488995], [333205.817689791, 7395247.71277836], [333247.996555184, 7395172.56160195], [333261.133400433, 7395102.3470075], [333270.981533908, 7395034.48052247], [333277.885095545, 7394986.25678192]]]},
                    'type': 'Feature'
                }
            ]
        }

        self.tester.api_element("way", expected, changeset_id="1001")

        expected = {
            'features': [
                {
                    'geometry': {'coordinates': [[[[0, 0], [1, 1], [2, 2], [3, 3], [0, 0]]]], 'type': 'MultiPolygon'},
                    'tags': [{'v': 'hotel', 'k': 'building'},
                             {'v': '1870', 'k': 'start_date'},
                             {'v': '1900', 'k': 'end_date'}],
                    'type': 'Feature',
                    'properties': {'fk_changeset_id': 1001, 'id': 1001}}
            ],
            'type': 'FeatureCollection',
            'crs': {'properties': {'name': 'EPSG:4326'}, 'type': 'name'}
        }

        self.tester.api_element("area", expected, changeset_id="1001")

    def test_get_api_element_return_all_elements_by_project_id_and_changeset_id(self):
        expected = {
            'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'fk_changeset_id': 1001, 'id': 1001},
                    'type': 'Feature',
                    'geometry': {'coordinates': [[-23.546421, -46.635722]], 'type': 'MultiPoint'},
                    'tags': [{'k': 'address', 'v': 'R. São José'},
                             {'k': 'start_date', 'v': '1869'},
                             {'k': 'end_date', 'v': '1869'}]
                }
            ]
        }

        self.tester.api_element("node", expected, project_id="1001", changeset_id="1001")

        expected = {
            'type': 'FeatureCollection',
            'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
            'features': [
                {
                    'geometry': {'type': 'MultiLineString', 'coordinates': [[[333188.261004703, 7395284.32488995], [333205.817689791, 7395247.71277836], [333247.996555184, 7395172.56160195], [333261.133400433, 7395102.3470075], [333270.981533908, 7395034.48052247], [333277.885095545, 7394986.25678192]]]},
                    'type': 'Feature',
                    'properties': {'fk_changeset_id': 1001, 'id': 1001},
                    'tags': [{'k': 'name', 'v': 'rua boa vista'},
                             {'k': 'start_date', 'v': '1930'},
                             {'k': 'end_date', 'v': '1930'}]
                }
            ]
        }

        self.tester.api_element("way", expected, project_id="1001", changeset_id="1001")

        expected = {
            'type': 'FeatureCollection',
            'features': [
                {'type': 'Feature',
                 'geometry': {'type': 'MultiPolygon', 'coordinates': [[[[0, 0], [1, 1], [2, 2], [3, 3], [0, 0]]]]},
                 'tags': [{'v': 'hotel', 'k': 'building'},
                          {'v': '1870', 'k': 'start_date'},
                          {'v': '1900', 'k': 'end_date'}],
                 'properties': {'id': 1001, 'fk_changeset_id': 1001}
                 }
            ],
            'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}}
        }

        self.tester.api_element("area", expected, project_id="1001", changeset_id="1001")


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
