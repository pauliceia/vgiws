#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/


class TestAPIGETElement(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    ################################################################################
    # NODE
    ################################################################################

    def test_get_api_node_return_all_elements(self):
        expected = {
            'type': 'FeatureCollection',
            'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
            'features': [
                {
                    'type': 'Feature',
                    'tags': [{'v': 'R. São José', 'k': 'address'},
                             {'v': '1869', 'k': 'start_date'},
                             {'v': '1869', 'k': 'end_date'}],
                    'properties': {'id': 1001, 'fk_changeset_id': 1001},
                    'geometry': {'type': 'MultiPoint', 'coordinates': [[-23.546421, -46.635722]]}
                },
                {
                    'type': 'Feature',
                    'tags': [{'v': 'R. Marechal Deodoro', 'k': 'address'},
                             {'v': '1878', 'k': 'start_date'},
                             {'v': '1910', 'k': 'end_date'}],
                    'properties': {'id': 1002, 'fk_changeset_id': 1002},
                    'geometry': {'type': 'MultiPoint', 'coordinates': [[-23.55045, -46.634272]]}
                },
                {
                    'type': 'Feature',
                    'tags': None,
                    'properties': {'id': 1006, 'fk_changeset_id': 1003},
                    'geometry': {'type': 'MultiPoint', 'coordinates': [[-54, 33]]}
                },
                {
                    'type': 'Feature',
                    'tags': None,
                    'properties': {'id': 1007, 'fk_changeset_id': 1002},
                    'geometry': {'type': 'MultiPoint', 'coordinates': [[-21, 42]]}
                }
            ]
        }

        self.tester.api_element("node", expected, element_id="")

    def test_get_api_node_return_element_with_id_1001(self):
        expected = {
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'type': 'FeatureCollection',
            'features': [
                {
                    'tags': [{'v': 'R. São José', 'k': 'address'},
                             {'v': '1869', 'k': 'start_date'},
                             {'v': '1869', 'k': 'end_date'}],
                    'type': 'Feature',
                    'properties': {'id': 1001, 'fk_changeset_id': 1001},
                    'geometry': {'type': 'MultiPoint', 'coordinates': [[-23.546421, -46.635722]]}
                }
            ]
        }

        self.tester.api_element("node", expected, element_id="1001")

    ################################################################################
    # WAY
    ################################################################################

    def test_get_api_way_return_all_elements(self):
        expected = {
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'type': 'FeatureCollection',
            'features': [
                {
                    'geometry': {'type': 'MultiLineString', 'coordinates': [[[333188.261004703, 7395284.32488995], [333205.817689791, 7395247.71277836], [333247.996555184, 7395172.56160195], [333261.133400433, 7395102.3470075], [333270.981533908, 7395034.48052247], [333277.885095545, 7394986.25678192]]]},
                    'tags': [{'k': 'name', 'v': 'rua boa vista'},
                             {'k': 'start_date', 'v': '1930'},
                             {'k': 'end_date', 'v': '1930'}],
                    'type': 'Feature',
                    'properties': {'fk_changeset_id': 1001, 'id': 1001}
                },
                {
                    'geometry': {'type': 'MultiLineString', 'coordinates': [[[333270.653184563, 7395036.74327773], [333244.47769325, 7395033.35326418], [333204.141105934, 7395028.41654752], [333182.467715735, 7395026.2492085]]]},
                    'tags': [{'k': 'address', 'v': 'rua tres de dezembro'},
                             {'k': 'start_date', 'v': '1930'},
                             {'k': 'end_date', 'v': '1930'}],
                    'type': 'Feature',
                    'properties': {'fk_changeset_id': 1002, 'id': 1002}
                }
            ]
        }

        self.tester.api_element("way", expected, element_id="")

    def test_get_api_way_return_element_with_id_1001(self):
        expected = {
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {'coordinates': [
                        [[333188.261004703, 7395284.32488995], [333205.817689791, 7395247.71277836],
                         [333247.996555184, 7395172.56160195], [333261.133400433, 7395102.3470075],
                         [333270.981533908, 7395034.48052247], [333277.885095545, 7394986.25678192]]],
                                 'type': 'MultiLineString'},
                    'tags': [{'v': 'rua boa vista', 'k': 'name'},
                             {'v': '1930', 'k': 'start_date'},
                             {'v': '1930', 'k': 'end_date'}],
                    'properties': {'id': 1001, 'fk_changeset_id': 1001}
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_element("way", expected, element_id="1001")

    ################################################################################
    # AREA
    ################################################################################

    def test_get_api_area_return_all_elements(self):
        expected = {
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'type': 'FeatureCollection',
            'features': [
                {
                    'tags': [{'v': 'hotel', 'k': 'building'},
                             {'v': '1870', 'k': 'start_date'},
                             {'v': '1900', 'k': 'end_date'}],
                    'type': 'Feature',
                    'geometry': {'type': 'MultiPolygon', 'coordinates': [[[[0, 0], [1, 1], [2, 2], [3, 3], [0, 0]]]]},
                    'properties': {'id': 1001, 'fk_changeset_id': 1001}
                },
                {
                    'tags': [{'v': 'theater', 'k': 'building'},
                             {'v': '1920', 'k': 'start_date'},
                             {'v': '1930', 'k': 'end_date'}],
                    'type': 'Feature',
                    'geometry': {'type': 'MultiPolygon', 'coordinates': [[[[2, 2], [3, 3], [4, 4], [5, 5], [2, 2]]]]},
                    'properties': {'id': 1002, 'fk_changeset_id': 1002}
                }
            ]
        }

        self.tester.api_element("area", expected, element_id="")

    def test_get_api_area_return_element_with_id_1001(self):
        expected = {
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'properties': {'id': 1001, 'fk_changeset_id': 1001},
                    'tags': [{'k': 'building', 'v': 'hotel'},
                             {'k': 'start_date', 'v': '1870'},
                             {'k': 'end_date', 'v': '1900'}],
                    'geometry': {'type': 'MultiPolygon', 'coordinates': [[[[0, 0], [1, 1], [2, 2], [3, 3], [0, 0]]]]},
                    'type': 'Feature'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_element("area", expected, element_id="1001")

    # def test_get_api_element_with_invalid_element_id(self):
    #     self.tester.api_element_invalid_parameter("node", "abc")
    #     self.tester.api_element_invalid_parameter("node", 0)
    #     self.tester.api_element_invalid_parameter("node", -1)
    #     self.tester.api_element_invalid_parameter("node", "-1")
    #     self.tester.api_element_invalid_parameter("node", "0")

    # helper
    # def test_helper_execute(self):
    #     # do a GET call
    #     response = get('http://localhost:8888/helper/execute/')
    #
    #     self.assertTrue(response.ok)
    #     self.assertEqual(response.status_code, 200)
    #
    #     expected = []
    #
    #     resulted = loads(response.text)  # convert string to dict/JSON
    #
    #     self.assertEqual(expected, resulted)


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
