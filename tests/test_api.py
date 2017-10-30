#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from json import loads
from requests import get


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/

class TestAPI(TestCase):
    # def tests(self):
    #     print("\n")
    #     print("response: ", response)
    #     print("response.ok: ", response.ok)
    #     print("response.status_code: ", response.status_code)
    #     print("response.headers: ", response.headers)
    #     print("response.text: ", response.text)
    #     print("type(response.text): ", type(response.text))
    #     print("\n")

    def test_get_api_node_id_1_wkt(self):
        # do a GET call
        response = get('http://localhost:8888/api/node/?q=[id=1]&format=wkt')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = [
            {'visible': True, 'version': 1, 'fk_id_changeset': 1, 'id': 1, 'geom': 'MULTIPOINT(0 0)'}
        ]
        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_node_id_1_geojson(self):
        # do a GET call
        response = get('http://localhost:8888/api/node/?q=[id=1]&format=geojson')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = {
            'features': [
                {
                    'geometry': {'coordinates': [[0, 0]], 'type': 'MultiPoint'},
                    'properties': {'id': 1, 'fk_id_changeset': 1, 'version': 1},
                    'type': 'Feature',
                }
            ],
            'type': 'FeatureCollection'
        }

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_node_without_id_wkt(self):
        # do a GET call
        response = get('http://localhost:8888/api/node/?format=wkt')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = [
            {'fk_id_changeset': 1, 'version': 1, 'geom': 'MULTIPOINT(0 0)', 'visible': True, 'id': 1},
            {'fk_id_changeset': 2, 'version': 1, 'geom': 'MULTIPOINT(1 1)', 'visible': True, 'id': 2}
        ]
        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_node_without_id_geojson(self):
        # do a GET call
        response = get('http://localhost:8888/api/node/?format=geojson')

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        expected = {
            'features': [
                {
                    'geometry': {'type': 'MultiPoint', 'coordinates': [[0, 0]]},
                    'properties': {'version': 1, 'fk_id_changeset': 1, 'id': 1},
                    'type': 'Feature',
                },
                {
                    'geometry': {'type': 'MultiPoint', 'coordinates': [[1, 1]]},
                    'properties': {'version': 1, 'fk_id_changeset': 2, 'id': 2},
                    'type': 'Feature'
                }
            ],
            'type': 'FeatureCollection'
        }

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)



    # def test_get_api_node_create(self):
    #     # do a GET call
    #     response = get('http://localhost:8888/api/node/create/?q=[id=1]&format=geojson')
    #
    #     self.assertTrue(response.ok)
    #     self.assertEqual(response.status_code, 200)
    #
    #     expected = {'foo': 'bar', '1': 2, 'false': True}
    #     resulted = loads(response.text)  # convert string to dict/JSON
    #     self.assertEqual(expected, resulted)
    #
    # def test_get_api_node_history(self):
    #     # do a GET call
    #     response = get('http://localhost:8888/api/node/history/?q=[id=1]&format=geojson')
    #
    #     self.assertTrue(response.ok)
    #     self.assertEqual(response.status_code, 200)
    #
    #     expected = {'foo': 'bar', '1': 2, 'false': True}
    #     resulted = loads(response.text)  # convert string to dict/JSON
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
