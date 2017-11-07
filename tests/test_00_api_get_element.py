#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from json import loads
from requests import get

from tests.db_test_connection import prepare_test_db_before_tests


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/

class TestAPINode(TestCase):
    # def tests(self):
    #     print("\n")
    #     print("response: ", response)
    #     print("response.ok: ", response.ok)
    #     print("response.status_code: ", response.status_code)
    #     print("response.headers: ", response.headers)
    #     print("response.text: ", response.text)
    #     print("type(response.text): ", type(response.text))
    #     print("\n")

    @classmethod
    def setUpClass(cls):
        prepare_test_db_before_tests()

    ################################################################################
    # NODE
    ################################################################################

    def test_get_api_node_return_all_elements_as_wkt(self):
        # do a GET call
        response = get('http://localhost:8888/api/node/?format=wkt')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = [
            {'fk_changeset_id': 1001, 'geom': 'MULTIPOINT(-23.546421 -46.635722)', 'id': 1001},
            {'fk_changeset_id': 1002, 'geom': 'MULTIPOINT(-23.55045 -46.634272)', 'id': 1002}
        ]

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_node_return_all_elements_as_geojson(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'fk_changeset_id': 1001, 'id': 1001},
                    'geometry': {'coordinates': [[-23.546421, -46.635722]], 'type': 'MultiPoint'},
                    'tags': [{'v': 'R. São José', 'k': 'address', 'id': 1001},
                             {'v': '1869', 'k': 'start_date', 'id': 1002},
                             {'v': '1869', 'k': 'end_date', 'id': 1003}],
                    'type': 'Feature'
                },
                {
                    'properties': {'fk_changeset_id': 1002, 'id': 1002},
                    'geometry': {'coordinates': [[-23.55045, -46.634272]], 'type': 'MultiPoint'},
                    'tags': [{'v': 'R. Marechal Deodoro', 'k': 'address', 'id': 1004},
                             {'v': '1878', 'k': 'start_date', 'id': 1005},
                             {'v': '1910', 'k': 'end_date', 'id': 1006}],
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
        response = get('http://localhost:8888/api/node/?q=[id=1001]&format=wkt')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = [
            {'id': 1001, 'geom': 'MULTIPOINT(-23.546421 -46.635722)', 'fk_changeset_id': 1001}
        ]

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_node_return_element_with_id_1_as_geojson(self):
        # do a GET call
        response = get('http://localhost:8888/api/node/?q=[id=1001]')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'tags': [{'id': 1001, 'v': 'R. São José', 'k': 'address'},
                             {'id': 1002, 'v': '1869', 'k': 'start_date'},
                             {'id': 1003, 'v': '1869', 'k': 'end_date'}],
                    'type': 'Feature',
                    'properties': {'id': 1001, 'fk_changeset_id': 1001},
                    'geometry': {'type': 'MultiPoint', 'coordinates': [[-23.546421, -46.635722]]}
                }
            ]
        }

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)


    ################################################################################
    # WAY
    ################################################################################

    def test_get_api_way_return_all_elements_as_wkt(self):
        # do a GET call
        response = get('http://localhost:8888/api/way/?format=wkt')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = [
            {'fk_changeset_id': 1001, 'id': 1001, 'geom': 'MULTILINESTRING((333188.261004703 7395284.32488995,333205.817689791 7395247.71277836,333247.996555184 7395172.56160195,333261.133400433 7395102.3470075,333270.981533908 7395034.48052247,333277.885095545 7394986.25678192))'},
            {'fk_changeset_id': 1002, 'id': 1002, 'geom': 'MULTILINESTRING((333270.653184563 7395036.74327773,333244.47769325 7395033.35326418,333204.141105934 7395028.41654752,333182.467715735 7395026.2492085))'}
        ]

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_way_return_all_elements_as_geojson(self):

        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'geometry': {'type': 'MultiLineString', 'coordinates': [[[333188.261004703, 7395284.32488995], [333205.817689791, 7395247.71277836], [333247.996555184, 7395172.56160195], [333261.133400433, 7395102.3470075], [333270.981533908, 7395034.48052247], [333277.885095545, 7394986.25678192]]]},
                    'tags': [{'k': 'name', 'id': 1001, 'v': 'rua boa vista'},
                             {'k': 'start_date', 'id': 1002, 'v': '1930'},
                             {'k': 'end_date', 'id': 1003, 'v': '1930'}],
                    'type': 'Feature',
                    'properties': {'fk_changeset_id': 1001, 'id': 1001}
                },
                {
                    'geometry': {'type': 'MultiLineString', 'coordinates': [[[333270.653184563, 7395036.74327773], [333244.47769325, 7395033.35326418], [333204.141105934, 7395028.41654752], [333182.467715735, 7395026.2492085]]]},
                    'tags': [{'k': 'address', 'id': 1004, 'v': 'rua tres de dezembro'},
                             {'k': 'start_date', 'id': 1005, 'v': '1930'},
                             {'k': 'end_date', 'id': 1006, 'v': '1930'}],
                    'type': 'Feature',
                    'properties': {'fk_changeset_id': 1002, 'id': 1002}
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
        response = get('http://localhost:8888/api/way/?q=[id=1001]&format=wkt')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = [
            {'id': 1001, 'fk_changeset_id': 1001, 'geom': 'MULTILINESTRING((333188.261004703 7395284.32488995,333205.817689791 7395247.71277836,333247.996555184 7395172.56160195,333261.133400433 7395102.3470075,333270.981533908 7395034.48052247,333277.885095545 7394986.25678192))'}
        ]

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_way_return_element_with_id_1_as_geojson(self):
        # do a GET call
        response = get('http://localhost:8888/api/way/?q=[id=1001]')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = {
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {'coordinates': [[[333188.261004703, 7395284.32488995], [333205.817689791, 7395247.71277836], [333247.996555184, 7395172.56160195], [333261.133400433, 7395102.3470075], [333270.981533908, 7395034.48052247], [333277.885095545, 7394986.25678192]]], 'type': 'MultiLineString'},
                    'tags': [{'v': 'rua boa vista', 'k': 'name', 'id': 1001},
                             {'v': '1930', 'k': 'start_date', 'id': 1002},
                             {'v': '1930', 'k': 'end_date', 'id': 1003}],
                    'properties': {'id': 1001, 'fk_changeset_id': 1001}
                }
            ],
            'type': 'FeatureCollection'
        }

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    ################################################################################
    # AREA
    ################################################################################

    def test_get_api_area_return_all_elements_as_wkt(self):
        # do a GET call
        response = get('http://localhost:8888/api/area/?format=wkt')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = [
            {'id': 1001, 'fk_changeset_id': 1001, 'geom': 'MULTIPOLYGON(((0 0,1 1,2 2,3 3,0 0)))'},
            {'id': 1002, 'fk_changeset_id': 1002, 'geom': 'MULTIPOLYGON(((2 2,3 3,4 4,5 5,2 2)))'}
        ]

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_area_return_all_elements_as_geojson(self):

        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'tags': [{'id': 1001, 'v': 'hotel', 'k': 'building'},
                             {'id': 1002, 'v': '1870', 'k': 'start_date'},
                             {'id': 1003, 'v': '1900', 'k': 'end_date'}],
                    'type': 'Feature',
                    'geometry': {'type': 'MultiPolygon', 'coordinates': [[[[0, 0], [1, 1], [2, 2], [3, 3], [0, 0]]]]},
                    'properties': {'id': 1001, 'fk_changeset_id': 1001}
                },
                {
                    'tags': [{'id': 1004, 'v': 'theater', 'k': 'building'},
                             {'id': 1005, 'v': '1920', 'k': 'start_date'},
                             {'id': 1006, 'v': '1930', 'k': 'end_date'}],
                    'type': 'Feature',
                    'geometry': {'type': 'MultiPolygon', 'coordinates': [[[[2, 2], [3, 3], [4, 4], [5, 5], [2, 2]]]]},
                    'properties': {'id': 1002, 'fk_changeset_id': 1002}
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
        response = get('http://localhost:8888/api/area/?q=[id=1001]&format=wkt')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = [
            {'geom': 'MULTIPOLYGON(((0 0,1 1,2 2,3 3,0 0)))', 'fk_changeset_id': 1001, 'id': 1001}
        ]

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_area_return_element_with_id_1_as_geojson(self):
        # do a GET call
        response = get('http://localhost:8888/api/area/?q=[id=1001]')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = {
            'features': [
                {
                    'properties': {'id': 1001, 'fk_changeset_id': 1001},
                    'tags': [{'k': 'building', 'v': 'hotel', 'id': 1001},
                             {'k': 'start_date', 'v': '1870', 'id': 1002},
                             {'k': 'end_date', 'v': '1900', 'id': 1003}],
                    'geometry': {'type': 'MultiPolygon', 'coordinates': [[[[0, 0], [1, 1], [2, 2], [3, 3], [0, 0]]]]},
                    'type': 'Feature'
                }
            ],
            'type': 'FeatureCollection'
        }

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)


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




#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import json
# from urllib.request import urlopen

# https://www.google.com.br/search?client=ubuntu&hs=nkZ&channel=fs&dcr=0&q=python+unit+test+web+service+method&oq=python+unit+test+web+service+method&gs_l=psy-ab.3..0i71k1l4.3548.3659.0.3755.2.2.0.0.0.0.0.0..0.0.foo%2Ccfro%3D1%2Cnso-ehuqi%3D1%2Cnso-ehuui%3D1%2Cewh%3D0%2Cnso-mplt%3D2%2Cnso-enksa%3D0%2Cnso-enfk%3D1%2Cnso-usnt%3D1%2Cnso-qnt-npqp%3D0-1701%2Cnso-qnt-npdq%3D0-54%2Cnso-qnt-npt%3D0-1%2Cnso-qnt-ndc%3D300%2Ccspa-dspm-nm-mnp%3D0-05%2Ccspa-dspm-nm-mxp%3D0-125%2Cnso-unt-npqp%3D0-17%2Cnso-unt-npdq%3D0-54%2Cnso-unt-npt%3D0-0602%2Cnso-unt-ndc%3D300%2Ccspa-uipm-nm-mnp%3D0-007525%2Ccspa-uipm-nm-mxp%3D0-052675...0...1.1.64.psy-ab..2.0.0._11Xc6SCPtA
# http://seminar.io/2013/09/27/testing-your-rest-client-in-python/
# class ClientAPI:
#
#     def request(self, user):
#         url = "https://api.github.com/users/%s" % user
#         response = urlopen(url)
#         raw_data = response.read().decode('utf-8')
#
#         return json.loads(raw_data)
