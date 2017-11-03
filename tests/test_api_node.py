#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from json import loads
from requests import get


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
