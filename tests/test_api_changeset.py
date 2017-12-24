#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase, skip
from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/

class TestAPIChangeset(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # changeset - get

    def test_get_api_changeset_return_all_changesets(self):
        expected = {
            'features': [
                {
                    'tags': [{'v': 'pauliceia_portal', 'k': 'created_by'},
                             {'v': 'a changeset created', 'k': 'comment'}],
                    'properties': {'id': 1001, 'create_at': '2017-10-20 00:00:00', 'fk_layer_id': 1001,
                                   'closed_at': '2017-12-01 00:00:00', 'fk_user_id': 1001},
                    'type': 'Changeset'
                },
                {
                    'tags': [{'v': 'test_postgresql', 'k': 'created_by'},
                             {'v': 'changeset test', 'k': 'comment'}],
                    'properties': {'id': 1002, 'create_at': '2017-11-10 00:00:00', 'fk_layer_id': 1002,
                                   'closed_at': '2017-12-01 00:00:00', 'fk_user_id': 1002},
                    'type': 'Changeset'
                },
                {
                    'tags': [{'v': 'pauliceia_portal', 'k': 'created_by'},
                             {'v': 'a changeset created', 'k': 'comment'}],
                    'properties': {'id': 1003, 'create_at': '2017-11-15 00:00:00', 'fk_layer_id': 1001,
                                   'closed_at': '2017-12-01 00:00:00', 'fk_user_id': 1001},
                    'type': 'Changeset'
                },
                {
                    'tags': [{'v': 'test_postgresql', 'k': 'created_by'},
                             {'v': 'changeset test', 'k': 'comment'}],
                    'properties': {'id': 1004, 'create_at': '2017-01-20 00:00:00', 'fk_layer_id': 1002,
                                   'closed_at': '2017-12-01 00:00:00', 'fk_user_id': 1002},
                    'type': 'Changeset'
                },
                {
                    'tags': None,
                    'properties': {'create_at': '2017-03-25 00:00:00', 'closed_at': None, 'fk_layer_id': 1003,
                                   'fk_user_id': 1003, 'id': 1005},
                    'type': 'Changeset'
                },
                {
                    'tags': None,
                    'properties': {'create_at': '2017-05-13 00:00:00', 'closed_at': None, 'fk_layer_id': 1004,
                                   'fk_user_id': 1004, 'id': 1006},
                    'type': 'Changeset'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_changeset(expected)

    def test_get_api_changeset_return_changeset_by_changeset_id(self):
        expected = {
            'features': [
                {
                    'type': 'Changeset',
                    'properties': {'closed_at': '2017-12-01 00:00:00', 'fk_user_id': 1001,
                                   'create_at': '2017-10-20 00:00:00', 'id': 1001, 'fk_layer_id': 1001},
                    'tags': [{'k': 'created_by', 'v': 'pauliceia_portal'},
                             {'k': 'comment', 'v': 'a changeset created'}]
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_changeset(expected, changeset_id="1001")

    def test_get_api_changeset_return_changeset_by_layer_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'id': 1001, 'fk_user_id': 1001, 'create_at': '2017-10-20 00:00:00',
                                   'closed_at': '2017-12-01 00:00:00', 'fk_layer_id': 1001},
                    'tags': [{'v': 'pauliceia_portal', 'k': 'created_by'},
                             {'v': 'a changeset created', 'k': 'comment'}],
                    'type': 'Changeset'
                },
                {
                    'properties': {'id': 1003, 'fk_user_id': 1001, 'create_at': '2017-11-15 00:00:00',
                                   'closed_at': '2017-12-01 00:00:00', 'fk_layer_id': 1001},
                    'tags': [{'v': 'pauliceia_portal', 'k': 'created_by'},
                             {'v': 'a changeset created', 'k': 'comment'}],
                    'type': 'Changeset'
                }
            ]
        }

        self.tester.api_changeset(expected, layer_id="1001")

    def test_get_api_changeset_return_changeset_by_user_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Changeset',
                    'properties': {'id': 1002, 'closed_at': '2017-12-01 00:00:00', 'fk_layer_id': 1002,
                                   'create_at': '2017-11-10 00:00:00', 'fk_user_id': 1002},
                    'tags': [{'k': 'created_by', 'v': 'test_postgresql'},
                             {'k': 'comment', 'v': 'changeset test'}]},
                {
                    'type': 'Changeset',
                    'properties': {'id': 1004, 'closed_at': '2017-12-01 00:00:00', 'fk_layer_id': 1002,
                                   'create_at': '2017-01-20 00:00:00', 'fk_user_id': 1002},
                    'tags': [{'k': 'created_by', 'v': 'test_postgresql'},
                             {'k': 'comment', 'v': 'changeset test'}]
                }
            ]
        }

        self.tester.api_changeset(expected, user_id="1002")

    def test_get_api_changeset_return_all_open_changesets(self):
        expected = {
            'features': [
                {
                    'tags': None,
                    'properties': {'create_at': '2017-03-25 00:00:00', 'closed_at': None,
                                   'fk_user_id': 1003, 'id': 1005, 'fk_layer_id': 1003},
                    'type': 'Changeset'
                },
                {
                    'tags': None,
                    'properties': {'create_at': '2017-05-13 00:00:00', 'closed_at': None,
                                   'fk_user_id': 1004, 'id': 1006, 'fk_layer_id': 1004},
                    'type': 'Changeset'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_changeset(expected, open=True)

    def test_get_api_changeset_return_all_closed_changesets(self):
        expected = {
            'features': [
                {
                    'tags': [{'v': 'pauliceia_portal', 'k': 'created_by'},
                             {'v': 'a changeset created', 'k': 'comment'}],
                    'properties': {'id': 1001, 'create_at': '2017-10-20 00:00:00', 'fk_layer_id': 1001,
                                   'closed_at': '2017-12-01 00:00:00', 'fk_user_id': 1001},
                    'type': 'Changeset'
                },
                {
                    'tags': [{'v': 'test_postgresql', 'k': 'created_by'},
                             {'v': 'changeset test', 'k': 'comment'}],
                    'properties': {'id': 1002, 'create_at': '2017-11-10 00:00:00', 'fk_layer_id': 1002,
                                   'closed_at': '2017-12-01 00:00:00', 'fk_user_id': 1002},
                    'type': 'Changeset'
                },
                {
                    'tags': [{'v': 'pauliceia_portal', 'k': 'created_by'},
                             {'v': 'a changeset created', 'k': 'comment'}],
                    'properties': {'id': 1003, 'create_at': '2017-11-15 00:00:00', 'fk_layer_id': 1001,
                                   'closed_at': '2017-12-01 00:00:00', 'fk_user_id': 1001},
                    'type': 'Changeset'
                },
                {
                    'tags': [{'v': 'test_postgresql', 'k': 'created_by'},
                             {'v': 'changeset test', 'k': 'comment'}],
                    'properties': {'id': 1004, 'create_at': '2017-01-20 00:00:00', 'fk_layer_id': 1002,
                                   'closed_at': '2017-12-01 00:00:00', 'fk_user_id': 1002},
                    'type': 'Changeset'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_changeset(expected, closed=True)

    def test_get_api_changeset_return_all_open_changesets_by_layer_id(self):
        expected = {
            'features': [
                {
                    'tags': None,
                    'properties': {'create_at': '2017-03-25 00:00:00', 'closed_at': None,
                                   'fk_user_id': 1003, 'id': 1005, 'fk_layer_id': 1003},
                    'type': 'Changeset'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_changeset(expected, open=True, layer_id="1003")

    def test_get_api_changeset_return_all_closed_changesets_by_layer_id(self):
        expected = {
            'features': [
                {
                    'tags': [{'v': 'pauliceia_portal', 'k': 'created_by'},
                             {'v': 'a changeset created', 'k': 'comment'}],
                    'properties': {'id': 1001, 'create_at': '2017-10-20 00:00:00', 'fk_layer_id': 1001,
                                   'closed_at': '2017-12-01 00:00:00', 'fk_user_id': 1001},
                    'type': 'Changeset'
                },
                {
                    'tags': [{'v': 'pauliceia_portal', 'k': 'created_by'},
                             {'v': 'a changeset created', 'k': 'comment'}],
                    'properties': {'id': 1003, 'create_at': '2017-11-15 00:00:00', 'fk_layer_id': 1001,
                                   'closed_at': '2017-12-01 00:00:00', 'fk_user_id': 1001},
                    'type': 'Changeset'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_changeset(expected, closed=True, layer_id="1001")

    def test_get_api_changeset_return_all_open_changesets_by_user_id(self):
        expected = {
            'features': [
                {
                    'tags': None,
                    'properties': {'create_at': '2017-03-25 00:00:00', 'closed_at': None,
                                   'fk_user_id': 1003, 'id': 1005, 'fk_layer_id': 1003},
                    'type': 'Changeset'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_changeset(expected, open=True, user_id="1003")

    def test_get_api_changeset_return_all_closed_changesets_by_user_id(self):
        expected = {
            'features': [
                {
                    'tags': [{'v': 'pauliceia_portal', 'k': 'created_by'},
                             {'v': 'a changeset created', 'k': 'comment'}],
                    'properties': {'id': 1001, 'create_at': '2017-10-20 00:00:00', 'fk_layer_id': 1001,
                                   'closed_at': '2017-12-01 00:00:00', 'fk_user_id': 1001},
                    'type': 'Changeset'
                },
                {
                    'tags': [{'v': 'pauliceia_portal', 'k': 'created_by'},
                             {'v': 'a changeset created', 'k': 'comment'}],
                    'properties': {'id': 1003, 'create_at': '2017-11-15 00:00:00', 'fk_layer_id': 1001,
                                   'closed_at': '2017-12-01 00:00:00', 'fk_user_id': 1001},
                    'type': 'Changeset'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_changeset(expected, closed=True, user_id="1001")

    # changeset - create and delete

    def test_get_api_changeset_create_close_and_delete(self):
        # DO LOGIN
        self.tester.auth_login()

        feature = {
            'tags': [{'k': 'created_by', 'v': 'test_api'},
                     {'k': 'comment', 'v': 'testing create changeset'}],
            'properties': {'id': -1, "fk_layer_id": 1004},
            'type': 'Changeset'

        }
        feature = self.tester.api_changeset_create(feature)

        # get the id of changeset to CLOSE the changeset
        feature_id = feature["properties"]["id"]

        # CLOSE THE CHANGESET
        self.tester.api_changeset_close(feature_id)

        # DELETE THE CHANGESET
        self.tester.api_changeset_delete(feature_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPIChangesetErrors(TestCase):
    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # changeset errors - get

    def test_get_api_changeset_error_400_bad_request(self):
        self.tester.api_changeset_error_400_bad_request(changeset_id="abc")
        self.tester.api_changeset_error_400_bad_request(changeset_id=0)
        self.tester.api_changeset_error_400_bad_request(changeset_id=-1)
        self.tester.api_changeset_error_400_bad_request(changeset_id="-1")
        self.tester.api_changeset_error_400_bad_request(changeset_id="0")

    def test_get_api_changeset_error_404_not_found(self):
        self.tester.api_changeset_error_404_not_found(changeset_id="999")
        self.tester.api_changeset_error_404_not_found(changeset_id="998")

    # changeset errors - create

    def test_put_api_changeset_create_error_403_forbidden(self):
        feature = {
            'tags': [{'k': 'created_by', 'v': 'test_api'},
                     {'k': 'comment', 'v': 'testing create changeset'}],
            'properties': {'id': -1, "fk_layer_id": 1004},
            'type': 'Changeset'
        }
        self.tester.api_changeset_create_error_403_forbidden(feature)

    # changeset errors - close

    def test_put_api_changeset_close_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login()

        self.tester.api_changeset_close_error_400_bad_request("abc")
        self.tester.api_changeset_close_error_400_bad_request(0)
        self.tester.api_changeset_close_error_400_bad_request(-1)
        self.tester.api_changeset_close_error_400_bad_request("-1")
        self.tester.api_changeset_close_error_400_bad_request("0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_changeset_close_error_403_forbidden(self):
        self.tester.api_changeset_close_error_403_forbidden("abc")
        self.tester.api_changeset_close_error_403_forbidden(0)
        self.tester.api_changeset_close_error_403_forbidden(-1)
        self.tester.api_changeset_close_error_403_forbidden("-1")
        self.tester.api_changeset_close_error_403_forbidden("0")
        self.tester.api_changeset_close_error_403_forbidden("1001")

    def test_put_api_changeset_close_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login()

        self.tester.api_changeset_close_error_404_not_found("5000")
        self.tester.api_changeset_close_error_404_not_found("5001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    # layer errors - delete

    def test_delete_api_changeset_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login()

        self.tester.api_changeset_delete_error_400_bad_request("abc")
        self.tester.api_changeset_delete_error_400_bad_request(0)
        self.tester.api_changeset_delete_error_400_bad_request(-1)
        self.tester.api_changeset_delete_error_400_bad_request("-1")
        self.tester.api_changeset_delete_error_400_bad_request("0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_layer_error_403_forbidden(self):
        self.tester.api_changeset_delete_error_403_forbidden("abc")
        self.tester.api_changeset_delete_error_403_forbidden(0)
        self.tester.api_changeset_delete_error_403_forbidden(-1)
        self.tester.api_changeset_delete_error_403_forbidden("-1")
        self.tester.api_changeset_delete_error_403_forbidden("0")
        self.tester.api_changeset_delete_error_403_forbidden("1001")

    def test_delete_api_layer_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login()

        self.tester.api_changeset_delete_error_404_not_found("5000")
        self.tester.api_changeset_delete_error_404_not_found("5001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
