#!/usr/bin/env python
# -*- coding: utf-8 -*-


# from unittest import TestCase
# from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/

"""
class TestAPIElement(TestCase):

    def setUp(self):
        self.maxDiff = None

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
                    'tags': {'address': 'R. São José', 'end_date': '1869', 'start_date': '1869'},
                    'properties': {'id': 1001, 'fk_changeset_id': 1001, 'version': 1, 'visible': True},
                    'geometry': {'type': 'MultiPoint', 'coordinates': [[-23.546421, -46.635722]]}
                },
                {
                    'type': 'Feature',
                    'tags': {'address': 'R. Marechal Deodoro', 'end_date': '1910', 'start_date': '1878'},
                    'properties': {'id': 1002, 'fk_changeset_id': 1002, 'version': 1, 'visible': True},
                    'geometry': {'type': 'MultiPoint', 'coordinates': [[-23.55045, -46.634272]]}
                },
                {
                    'type': 'Feature',
                    'tags': None,
                    'properties': {'id': 1006, 'fk_changeset_id': 1003, 'version': 1, 'visible': True},
                    'geometry': {'type': 'MultiPoint', 'coordinates': [[-54, 33]]}
                },
                {
                    'type': 'Feature',
                    'tags': None,
                    'properties': {'id': 1007, 'fk_changeset_id': 1002, 'version': 1, 'visible': True},
                    'geometry': {'type': 'MultiPoint', 'coordinates': [[-21, 42]]}
                }
            ]
        }

        self.tester.api_element("point", expected, element_id="")

        expected = {
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'type': 'FeatureCollection',
            'features': [
                {
                    'geometry': {'type': 'MultiLineString', 'coordinates': [
                        [[333188.261004703, 7395284.32488995], [333205.817689791, 7395247.71277836],
                         [333247.996555184, 7395172.56160195], [333261.133400433, 7395102.3470075],
                         [333270.981533908, 7395034.48052247], [333277.885095545, 7394986.25678192]]]},
                    'tags': {'end_date': '1930', 'name': 'rua boa vista', 'start_date': '1930'},
                    'type': 'Feature',
                    'properties': {'fk_changeset_id': 1001, 'id': 1001, 'version': 1, 'visible': True}
                },
                {
                    'geometry': {'type': 'MultiLineString', 'coordinates': [
                        [[333270.653184563, 7395036.74327773], [333244.47769325, 7395033.35326418],
                         [333204.141105934, 7395028.41654752], [333182.467715735, 7395026.2492085]]]},
                    'tags': {'name': 'rua tres de dezembro', 'end_date': '1930', 'start_date': '1930'},
                    'type': 'Feature',
                    'properties': {'fk_changeset_id': 1002, 'id': 1002, 'version': 1, 'visible': True}
                }
            ]
        }

        self.tester.api_element("line", expected, element_id="")

        expected = {
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'type': 'FeatureCollection',
            'features': [
                {
                    'tags': {'building': 'hotel', 'end_date': '1900', 'start_date': '1870'},
                    'type': 'Feature',
                    'geometry': {'type': 'MultiPolygon', 'coordinates': [[[[0, 0], [1, 1], [2, 2], [3, 3], [0, 0]]]]},
                    'properties': {'id': 1001, 'fk_changeset_id': 1001, 'version': 1, 'visible': True}
                },
                {
                    'tags': {'building': 'theater', 'end_date': '1930', 'start_date': '1920'},
                    'type': 'Feature',
                    'geometry': {'type': 'MultiPolygon', 'coordinates': [[[[2, 2], [3, 3], [4, 4], [5, 5], [2, 2]]]]},
                    'properties': {'id': 1002, 'fk_changeset_id': 1002, 'version': 1, 'visible': True}
                }
            ]
        }

        self.tester.api_element("polygon", expected, element_id="")

    def test_get_api_element_return_element_by_id(self):
        expected = {
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'type': 'FeatureCollection',
            'features': [
                {
                    'tags': {'address': 'R. São José', 'end_date': '1869', 'start_date': '1869'},
                    'type': 'Feature',
                    'properties': {'id': 1001, 'fk_changeset_id': 1001, 'version': 1, 'visible': True},
                    'geometry': {'type': 'MultiPoint', 'coordinates': [[-23.546421, -46.635722]]}
                }
            ]
        }

        self.tester.api_element("point", expected, element_id="1001")

        expected = {
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'coordinates': [[[333188.261004703, 7395284.32488995],
                                         [333205.817689791, 7395247.71277836],
                                         [333247.996555184, 7395172.56160195],
                                         [333261.133400433, 7395102.3470075],
                                         [333270.981533908, 7395034.48052247],
                                         [333277.885095545, 7394986.25678192]]],
                        'type': 'MultiLineString'
                    },
                    'tags': {'end_date': '1930', 'name': 'rua boa vista', 'start_date': '1930'},
                    'properties': {'id': 1001, 'fk_changeset_id': 1001, 'version': 1, 'visible': True}
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_element("line", expected, element_id="1001")

        expected = {
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'properties': {'id': 1001, 'fk_changeset_id': 1001, 'version': 1, 'visible': True},
                    'tags': {'building': 'hotel', 'end_date': '1900', 'start_date': '1870'},
                    'geometry': {'type': 'MultiPolygon', 'coordinates': [[[[0, 0], [1, 1], [2, 2], [3, 3], [0, 0]]]]},
                    'type': 'Feature'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_element("polygon", expected, element_id="1001")

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

    def test_get_api_element_return_all_elements_by_layer_id(self):
        expected = {
            'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'fk_changeset_id': 1001, 'id': 1001, 'version': 1, 'visible': True},
                    'type': 'Feature',
                    'geometry': {'coordinates': [[-23.546421, -46.635722]], 'type': 'MultiPoint'},
                    'tags': {'address': 'R. São José', 'end_date': '1869', 'start_date': '1869'}
                },
                {
                    'properties': {'fk_changeset_id': 1003, 'id': 1006, 'version': 1, 'visible': True},
                    'type': 'Feature',
                    'geometry': {'coordinates': [[-54, 33]], 'type': 'MultiPoint'},
                    'tags': None
                }
            ]
        }

        self.tester.api_element("point", expected, layer_id="1001")

        expected = {
            'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
            'type': 'FeatureCollection',
            'features': [
                {
                    'tags': {'end_date': '1930', 'name': 'rua boa vista', 'start_date': '1930'},
                    'type': 'Feature',
                    'geometry': {'type': 'MultiLineString', 'coordinates': [[[333188.261004703, 7395284.32488995], [333205.817689791, 7395247.71277836], [333247.996555184, 7395172.56160195], [333261.133400433, 7395102.3470075], [333270.981533908, 7395034.48052247], [333277.885095545, 7394986.25678192]]]},
                    'properties': {'fk_changeset_id': 1001, 'id': 1001, 'version': 1, 'visible': True}
                }
            ]
        }

        self.tester.api_element("line", expected, layer_id="1001")

        expected = {
            'crs': {'properties': {'name': 'EPSG:4326'}, 'type': 'name'},
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'id': 1001, 'fk_changeset_id': 1001, 'version': 1, 'visible': True},
                    'type': 'Feature',
                    'tags': {'building': 'hotel', 'end_date': '1900', 'start_date': '1870'},
                    'geometry': {'type': 'MultiPolygon', 'coordinates': [[[[0, 0], [1, 1], [2, 2], [3, 3], [0, 0]]]]}
                }
            ]
        }

        self.tester.api_element("polygon", expected, layer_id="1001")

    def test_get_api_element_return_all_elements_by_changeset_id(self):
        expected = {
            'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'fk_changeset_id': 1001, 'id': 1001, 'version': 1, 'visible': True},
                    'type': 'Feature',
                    'geometry': {'coordinates': [[-23.546421, -46.635722]], 'type': 'MultiPoint'},
                    'tags': {'address': 'R. São José', 'end_date': '1869', 'start_date': '1869'}
                }
            ]
        }

        self.tester.api_element("point", expected, changeset_id="1001")

        expected = {
            'type': 'FeatureCollection',
            'crs': {'properties': {'name': 'EPSG:4326'}, 'type': 'name'},
            'features': [
                {
                    'properties': {'id': 1001, 'fk_changeset_id': 1001, 'version': 1, 'visible': True},
                    'tags': {'end_date': '1930', 'name': 'rua boa vista', 'start_date': '1930'},
                    'geometry': {'type': 'MultiLineString', 'coordinates': [[[333188.261004703, 7395284.32488995], [333205.817689791, 7395247.71277836], [333247.996555184, 7395172.56160195], [333261.133400433, 7395102.3470075], [333270.981533908, 7395034.48052247], [333277.885095545, 7394986.25678192]]]},
                    'type': 'Feature'
                }
            ]
        }

        self.tester.api_element("line", expected, changeset_id="1001")

        expected = {
            'features': [
                {
                    'geometry': {'coordinates': [[[[0, 0], [1, 1], [2, 2], [3, 3], [0, 0]]]], 'type': 'MultiPolygon'},
                    'tags': {'building': 'hotel', 'end_date': '1900', 'start_date': '1870'},
                    'type': 'Feature',
                    'properties': {'fk_changeset_id': 1001, 'id': 1001, 'version': 1, 'visible': True}
                }
            ],
            'type': 'FeatureCollection',
            'crs': {'properties': {'name': 'EPSG:4326'}, 'type': 'name'}
        }

        self.tester.api_element("polygon", expected, changeset_id="1001")

    def test_get_api_element_return_all_elements_by_user_id(self):
        expected = {
            'crs': {'properties': {'name': 'EPSG:4326'}, 'type': 'name'},
            'type': 'FeatureCollection',
            'features': [
                {
                    'tags': {'address': 'R. São José', 'end_date': '1869', 'start_date': '1869'},
                    'geometry': {'coordinates': [[-23.546421, -46.635722]], 'type': 'MultiPoint'},
                    'properties': {'fk_changeset_id': 1001, 'id': 1001, 'version': 1, 'visible': True},
                    'type': 'Feature'
                },
                {
                    'tags': None,
                    'geometry': {'coordinates': [[-54, 33]], 'type': 'MultiPoint'},
                    'properties': {'fk_changeset_id': 1003, 'id': 1006, 'version': 1, 'visible': True},
                    'type': 'Feature'
                }
            ]
        }

        self.tester.api_element("point", expected, user_id="1001")

        expected = {
            'type': 'FeatureCollection',
            'crs': {'properties': {'name': 'EPSG:4326'}, 'type': 'name'},
            'features': [
                {
                    'properties': {'fk_changeset_id': 1001, 'id': 1001, 'version': 1, 'visible': True},
                    'type': 'Feature',
                    'tags': {'end_date': '1930', 'name': 'rua boa vista', 'start_date': '1930'},
                    'geometry': {'type': 'MultiLineString', 'coordinates': [[[333188.261004703, 7395284.32488995], [333205.817689791, 7395247.71277836], [333247.996555184, 7395172.56160195], [333261.133400433, 7395102.3470075], [333270.981533908, 7395034.48052247], [333277.885095545, 7394986.25678192]]]}
                }
            ]
        }

        self.tester.api_element("line", expected, user_id="1001")

        expected = {
            'features': [
                {
                    'properties': {'fk_changeset_id': 1001, 'id': 1001, 'version': 1, 'visible': True},
                    'type': 'Feature',
                    'geometry': {'coordinates': [[[[0, 0], [1, 1], [2, 2], [3, 3], [0, 0]]]], 'type': 'MultiPolygon'},
                    'tags': {'building': 'hotel', 'end_date': '1900', 'start_date': '1870'}
                }
            ],
            'type': 'FeatureCollection',
            'crs': {'properties': {'name': 'EPSG:4326'}, 'type': 'name'}
        }

        self.tester.api_element("polygon", expected, user_id="1001")

    # element - create and delete

    def test_get_api_element_create_and_delete(self):
        # DO LOGIN
        self.tester.auth_login_fake()

        # CREATE A CHANGESET
        changeset = {
            'tags': {'comment': 'testing create changeset', 'created_by': 'test_api'},
            'properties': {'id': -1, "fk_layer_id": 1004},
            'type': 'Changeset'
        }
        changeset_id = self.tester.api_changeset_create(changeset)

        # ADD ELEMENTS
        point = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': {'date': '1910', 'event': 'robbery'},
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': changeset_id},
                    'geometry': {
                        'type': 'MultiPoint',
                        'coordinates': [[-23.546421, -46.635722]]
                    },
                }
            ]
        }
        point = self.tester.api_element_create(point)  # return the same element with the id generated
        line = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': {'end_date': '1930-03-25', 'highway': 'residential', 'start_date': '1910-12-08'},
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': changeset_id},
                    'geometry': {
                        'type': 'MultiLineString',
                        'coordinates': [[[-54, 33], [-32, 31], [-36, 89]]]
                    },
                }
            ]
        }
        line = self.tester.api_element_create(line)
        polygon = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': {'building': 'cathedral', 'end_date': '1915-12-25', 'start_date': '1900-11-12'},
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': changeset_id},
                    'geometry': {
                        'type': 'MultiPolygon',
                        'coordinates': [[[[-12, 32], [-23, 74], [-12, 32]]]]
                    },
                }
            ]
        }
        polygon = self.tester.api_element_create(polygon)

        # REMOVE THE ELEMENTS CREATED
        self.tester.api_element_delete(point)
        self.tester.api_element_delete(line)
        self.tester.api_element_delete(polygon)

        # CLOSE THE CHANGESET
        self.tester.api_changeset_close(changeset_id)

        # DELETE THE CHANGESET
        self.tester.api_changeset_delete(changeset_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPIElementErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # element errors - get

    def test_get_api_element_error_400_bad_request(self):
        self.tester.api_element_error_400_bad_request("point", element_id="abc")
        self.tester.api_element_error_400_bad_request("line", element_id=0)
        self.tester.api_element_error_400_bad_request("polygon", element_id=-1)
        self.tester.api_element_error_400_bad_request("point", element_id="-1")
        self.tester.api_element_error_400_bad_request("line", element_id="0")

    def test_get_api_element_error_404_not_found(self):
        self.tester.api_element_error_404_not_found("point", element_id="999")
        self.tester.api_element_error_404_not_found("line", element_id="998")
        self.tester.api_element_error_404_not_found("polygon", element_id="997")

    # element errors - create

    def test_get_api_element_create_400_bad_request(self):
        # DO LOGIN
        self.tester.auth_login_fake()

        # ADD ELEMENTS
        point = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': {'date': '1910', 'event': 'robbery'},
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': 1001, 'version': 1, 'visible': True},
                    'geometry': {
                        'type': 'MultiPoint',
                        'coordinates': [[-23.546421, -46.635722]]
                    },
                }
            ]
        }
        self.tester.api_element_create_error_409_conflict(point)  # return the same element with the id generated

        line = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': {'end_date': '1930-03-25', 'highway': 'residential', 'start_date': '1910-12-08'},
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': 1001, 'version': 1, 'visible': True},
                    'geometry': {
                        'type': 'MultiLineString',
                        'coordinates': [[[-54, 33], [-32, 31], [-36, 89]]]
                    },
                }
            ]
        }
        self.tester.api_element_create_error_409_conflict(line)

        polygon = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': {'building': 'cathedral', 'end_date': '1915-12-25', 'start_date': '1900-11-12'},
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': 1001, 'version': 1, 'visible': True},
                    'geometry': {
                        'type': 'MultiPolygon',
                        'coordinates': [[[[-12, 32], [-23, 74], [-12, 32]]]]
                    },
                }
            ]
        }
        self.tester.api_element_create_error_409_conflict(polygon)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_element_create_error_403_forbidden(self):
        # ADD ELEMENTS
        point = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': {'date': '1910', 'event': 'robbery'},
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': 1001, 'version': 1, 'visible': True},
                    'geometry': {
                        'type': 'MultiPoint',
                        'coordinates': [[-23.546421, -46.635722]]
                    },
                }
            ]
        }
        self.tester.api_element_create_error_403_forbidden(point)  # return the same element with the id generated

        line = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': {'end_date': '1930-03-25', 'highway': 'residential', 'start_date': '1910-12-08'},
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': 1001, 'version': 1, 'visible': True},
                    'geometry': {
                        'type': 'MultiLineString',
                        'coordinates': [[[-54, 33], [-32, 31], [-36, 89]]]
                    },
                }
            ]
        }
        self.tester.api_element_create_error_403_forbidden(line)

        polygon = {
            'type': 'FeatureCollection',
            'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
            'features': [
                {
                    'tags': {'building': 'cathedral', 'end_date': '1915-12-25', 'start_date': '1900-11-12'},
                    'type': 'Feature',
                    'properties': {'id': -1, 'fk_changeset_id': 1001, 'version': 1, 'visible': True},
                    'geometry': {
                        'type': 'MultiPolygon',
                        'coordinates': [[[[-12, 32], [-23, 74], [-12, 32]]]]
                    },
                }
            ]
        }
        self.tester.api_element_create_error_403_forbidden(polygon)

    # element errors - delete

    def test_delete_api_element_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login_fake()

        self.tester.api_element_delete_error_400_bad_request("point", element_id="abc")
        self.tester.api_element_delete_error_400_bad_request("line", element_id=0)
        self.tester.api_element_delete_error_400_bad_request("polygon", element_id=-1)
        self.tester.api_element_delete_error_400_bad_request("point", element_id="-1")
        self.tester.api_element_delete_error_400_bad_request("line", element_id="0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_element_error_403_forbidden(self):
        self.tester.api_element_delete_error_403_forbidden("point", element_id="abc")
        self.tester.api_element_delete_error_403_forbidden("line", element_id=0)
        self.tester.api_element_delete_error_403_forbidden("point", element_id=-1)
        self.tester.api_element_delete_error_403_forbidden("polygon", element_id="-1")
        self.tester.api_element_delete_error_403_forbidden("line", element_id="0")
        self.tester.api_element_delete_error_403_forbidden("point", element_id="1001")

    def test_delete_api_element_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login_fake()

        self.tester.api_element_delete_error_404_not_found("point", element_id="5000")
        self.tester.api_element_delete_error_404_not_found("line", element_id="5001")
        self.tester.api_element_delete_error_404_not_found("polygon", element_id="5002")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()
"""

# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
