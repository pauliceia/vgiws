#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/


class TestAPIElement(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # element - get

    def test_get_api_element_return_all_elements(self):
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

        expected = {
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'type': 'FeatureCollection',
            'features': [
                {
                    'geometry': {'type': 'MultiLineString', 'coordinates': [
                        [[333188.261004703, 7395284.32488995], [333205.817689791, 7395247.71277836],
                         [333247.996555184, 7395172.56160195], [333261.133400433, 7395102.3470075],
                         [333270.981533908, 7395034.48052247], [333277.885095545, 7394986.25678192]]]},
                    'tags': [{'k': 'name', 'v': 'rua boa vista'},
                             {'k': 'start_date', 'v': '1930'},
                             {'k': 'end_date', 'v': '1930'}],
                    'type': 'Feature',
                    'properties': {'fk_changeset_id': 1001, 'id': 1001}
                },
                {
                    'geometry': {'type': 'MultiLineString', 'coordinates': [
                        [[333270.653184563, 7395036.74327773], [333244.47769325, 7395033.35326418],
                         [333204.141105934, 7395028.41654752], [333182.467715735, 7395026.2492085]]]},
                    'tags': [{'k': 'address', 'v': 'rua tres de dezembro'},
                             {'k': 'start_date', 'v': '1930'},
                             {'k': 'end_date', 'v': '1930'}],
                    'type': 'Feature',
                    'properties': {'fk_changeset_id': 1002, 'id': 1002}
                }
            ]
        }

        self.tester.api_element("way", expected, element_id="")

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

    def test_get_api_element_return_element_by_id(self):
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

    def test_get_api_element_return_all_elements_by_user_id(self):
        expected = {
            'crs': {'properties': {'name': 'EPSG:4326'}, 'type': 'name'},
            'type': 'FeatureCollection',
            'features': [
                {
                    'tags': [{'k': 'address', 'v': 'R. São José'},
                             {'k': 'start_date', 'v': '1869'},
                             {'k': 'end_date', 'v': '1869'}],
                    'geometry': {'coordinates': [[-23.546421, -46.635722]], 'type': 'MultiPoint'},
                    'properties': {'fk_changeset_id': 1001, 'id': 1001}, 'type': 'Feature'
                },
                {
                    'tags': None,
                    'geometry': {'coordinates': [[-54, 33]], 'type': 'MultiPoint'},
                    'properties': {'fk_changeset_id': 1003, 'id': 1006},
                    'type': 'Feature'}
            ]
        }

        self.tester.api_element("node", expected, user_id="1001")

        expected = {
            'type': 'FeatureCollection',
            'crs': {'properties': {'name': 'EPSG:4326'}, 'type': 'name'},
            'features': [
                {
                    'properties': {'fk_changeset_id': 1001, 'id': 1001},
                    'type': 'Feature',
                    'tags': [{'k': 'name', 'v': 'rua boa vista'},
                             {'k': 'start_date', 'v': '1930'},
                             {'k': 'end_date', 'v': '1930'}],
                    'geometry': {'type': 'MultiLineString', 'coordinates': [[[333188.261004703, 7395284.32488995], [333205.817689791, 7395247.71277836], [333247.996555184, 7395172.56160195], [333261.133400433, 7395102.3470075], [333270.981533908, 7395034.48052247], [333277.885095545, 7394986.25678192]]]}
                }
            ]
        }

        self.tester.api_element("way", expected, user_id="1001")

        expected = {
            'features': [
                {
                    'properties': {'fk_changeset_id': 1001, 'id': 1001},
                    'type': 'Feature',
                    'geometry': {'coordinates': [[[[0, 0], [1, 1], [2, 2], [3, 3], [0, 0]]]], 'type': 'MultiPolygon'},
                    'tags': [{'v': 'hotel', 'k': 'building'},
                             {'v': '1870', 'k': 'start_date'},
                             {'v': '1900', 'k': 'end_date'}]
                }
            ],
            'type': 'FeatureCollection',
            'crs': {'properties': {'name': 'EPSG:4326'}, 'type': 'name'}
        }

        self.tester.api_element("area", expected, user_id="1001")

    # element - create and delete

    def test_get_api_element_create_and_delete(self):
        # DO LOGIN
        self.tester.auth_login()

        # CREATE A CHANGESET
        changeset = {
            'changeset': {
                'tags': [{'k': 'created_by', 'v': 'test_api'},
                         {'k': 'comment', 'v': 'testing create changeset'}],
                'properties': {'id': -1, "fk_project_id": 1004}
            }
        }
        changeset = self.tester.api_changeset_create(changeset)

        # get the id of changeset to use in ADD element and CLOSE changeset
        changeset_id = changeset["changeset"]["properties"]["id"]

        # ADD ELEMENTS
        node = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'event', 'v': 'robbery'},
                             {'k': 'date', 'v': '1910'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': changeset_id},
                    'geometry': {
                        'type': 'MultiPoint',
                        'coordinates': [[-23.546421, -46.635722]]
                    },
                }
            ]
        }
        node = self.tester.api_element_create(node)  # return the same element with the id generated
        way = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'highway', 'v': 'residential'},
                             {'k': 'start_date', 'v': '1910-12-08'},
                             {'k': 'end_date', 'v': '1930-03-25'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': changeset_id},
                    'geometry': {
                        'type': 'MultiLineString',
                        'coordinates': [[[-54, 33], [-32, 31], [-36, 89]]]
                    },
                }
            ]
        }
        way = self.tester.api_element_create(way)
        area = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'building', 'v': 'cathedral'},
                             {'k': 'start_date', 'v': '1900-11-12'},
                             {'k': 'end_date', 'v': '1915-12-25'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': changeset_id},
                    'geometry': {
                        'type': 'MultiPolygon',
                        'coordinates': [[[[-12, 32], [-23, 74], [-12, 32]]]]
                    },
                }
            ]
        }
        area = self.tester.api_element_create(area)

        # REMOVE THE ELEMENTS CREATED
        element_id = node["features"][0]["properties"]["id"]  # get the id of element
        self.tester.api_element_delete("node", element_id=element_id)
        element_id = way["features"][0]["properties"]["id"]  # get the id of element
        self.tester.api_element_delete("way", element_id=element_id)
        element_id = area["features"][0]["properties"]["id"]  # get the id of element
        self.tester.api_element_delete("area", element_id=element_id)

        # CLOSE THE CHANGESET
        self.tester.api_changeset_close(changeset_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPIElementErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # element errors - get

    def test_get_api_element_error_400_bad_request(self):
        self.tester.api_element_error_400_bad_request("node", element_id="abc")
        self.tester.api_element_error_400_bad_request("way", element_id=0)
        self.tester.api_element_error_400_bad_request("area", element_id=-1)
        self.tester.api_element_error_400_bad_request("node", element_id="-1")
        self.tester.api_element_error_400_bad_request("way", element_id="0")

    def test_get_api_element_error_404_not_found(self):
        self.tester.api_element_error_404_not_found("node", element_id="999")
        self.tester.api_element_error_404_not_found("way", element_id="998")
        self.tester.api_element_error_404_not_found("area", element_id="997")

    # element errors - create

    def test_get_api_element_create_400_bad_request(self):
        # DO LOGIN
        self.tester.auth_login()

        # ADD ELEMENTS
        node = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'event', 'v': 'robbery'},
                             {'k': 'date', 'v': '1910'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': 1001},
                    'geometry': {
                        'type': 'MultiPoint',
                        'coordinates': [[-23.546421, -46.635722]]
                    },
                }
            ]
        }
        self.tester.api_element_create_error_400_bad_request(node)  # return the same element with the id generated

        way = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'highway', 'v': 'residential'},
                             {'k': 'start_date', 'v': '1910-12-08'},
                             {'k': 'end_date', 'v': '1930-03-25'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': 1001},
                    'geometry': {
                        'type': 'MultiLineString',
                        'coordinates': [[[-54, 33], [-32, 31], [-36, 89]]]
                    },
                }
            ]
        }
        self.tester.api_element_create_error_400_bad_request(way)

        area = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'building', 'v': 'cathedral'},
                             {'k': 'start_date', 'v': '1900-11-12'},
                             {'k': 'end_date', 'v': '1915-12-25'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': 1001},
                    'geometry': {
                        'type': 'MultiPolygon',
                        'coordinates': [[[[-12, 32], [-23, 74], [-12, 32]]]]
                    },
                }
            ]
        }
        self.tester.api_element_create_error_400_bad_request(area)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_element_create_error_403_forbidden(self):
        # ADD ELEMENTS
        node = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'event', 'v': 'robbery'},
                             {'k': 'date', 'v': '1910'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': 1001},
                    'geometry': {
                        'type': 'MultiPoint',
                        'coordinates': [[-23.546421, -46.635722]]
                    },
                }
            ]
        }
        self.tester.api_element_create_error_403_forbidden(node)  # return the same element with the id generated

        way = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'highway', 'v': 'residential'},
                             {'k': 'start_date', 'v': '1910-12-08'},
                             {'k': 'end_date', 'v': '1930-03-25'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': 1001},
                    'geometry': {
                        'type': 'MultiLineString',
                        'coordinates': [[[-54, 33], [-32, 31], [-36, 89]]]
                    },
                }
            ]
        }
        self.tester.api_element_create_error_403_forbidden(way)

        area = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': [{'k': 'building', 'v': 'cathedral'},
                             {'k': 'start_date', 'v': '1900-11-12'},
                             {'k': 'end_date', 'v': '1915-12-25'}],
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': 1001},
                    'geometry': {
                        'type': 'MultiPolygon',
                        'coordinates': [[[[-12, 32], [-23, 74], [-12, 32]]]]
                    },
                }
            ]
        }
        self.tester.api_element_create_error_403_forbidden(area)

    # element errors - delete

    def test_delete_api_element_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login()

        self.tester.api_element_delete_error_400_bad_request("node", element_id="abc")
        self.tester.api_element_delete_error_400_bad_request("way", element_id=0)
        self.tester.api_element_delete_error_400_bad_request("area", element_id=-1)
        self.tester.api_element_delete_error_400_bad_request("node", element_id="-1")
        self.tester.api_element_delete_error_400_bad_request("way", element_id="0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_element_error_403_forbidden(self):
        self.tester.api_element_delete_error_403_forbidden("node", element_id="abc")
        self.tester.api_element_delete_error_403_forbidden("way", element_id=0)
        self.tester.api_element_delete_error_403_forbidden("node", element_id=-1)
        self.tester.api_element_delete_error_403_forbidden("area", element_id="-1")
        self.tester.api_element_delete_error_403_forbidden("way", element_id="0")
        self.tester.api_element_delete_error_403_forbidden("node", element_id="1001")

    def test_delete_api_element_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login()

        self.tester.api_element_delete_error_404_not_found("node", element_id="5000")
        self.tester.api_element_delete_error_404_not_found("way", element_id="5001")
        self.tester.api_element_delete_error_404_not_found("area", element_id="5002")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
