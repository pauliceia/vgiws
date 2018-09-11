#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
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
                    'properties': {'created_at': '2017-01-05 00:00:00', 'user_id_creator': 1001, 'changeset_id': 1001,
                                   'closed_at': '2017-01-05 00:00:00', 'layer_id': 1001,
                                   'description': 'Creating layer_1001'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-03-05 00:00:00', 'user_id_creator': 1004, 'changeset_id': 1002,
                                   'closed_at': '2017-03-05 00:00:00', 'layer_id': 1002,
                                   'description': 'Creating layer_1002'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-04-12 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1003,
                                   'closed_at': '2017-04-12 00:00:00', 'layer_id': 1003,
                                   'description': 'Creating layer_1003'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-06-28 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1004,
                                   'closed_at': '2017-06-28 00:00:00', 'layer_id': 1004,
                                   'description': 'Creating layer_1004'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-08-05 00:00:00', 'user_id_creator': 1007, 'changeset_id': 1005,
                                   'closed_at': '2017-08-05 00:00:00', 'layer_id': 1005,
                                   'description': 'Creating layer_1005'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-09-04 00:00:00', 'user_id_creator': 1007, 'changeset_id': 1006,
                                   'closed_at': '2017-09-04 00:00:00', 'layer_id': 1006,
                                   'description': 'Creating layer_1006'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-01-08 00:00:00', 'user_id_creator': 1001, 'changeset_id': 1011,
                                   'closed_at': None, 'layer_id': 1001, 'description': 'An open changeset'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-04-13 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1013,
                                   'closed_at': None, 'layer_id': 1003, 'description': 'Creating an open changeset'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-01-08 00:00:00', 'user_id_creator': 1004, 'changeset_id': 1014,
                                   'closed_at': None, 'layer_id': 1002, 'description': 'An open changeset'},
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
                    'properties': {'created_at': '2017-04-12 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1003,
                                   'closed_at': '2017-04-12 00:00:00', 'layer_id': 1003,
                                   'description': 'Creating layer_1003'},
                    'type': 'Changeset'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_changeset(expected, changeset_id="1003")

    def test_get_api_changeset_return_changeset_by_layer_id(self):
        expected = {
            'features': [
                {
                    'properties': {'created_at': '2017-06-28 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1004,
                                   'closed_at': '2017-06-28 00:00:00', 'layer_id': 1004,
                                   'description': 'Creating layer_1004'},
                    'type': 'Changeset'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_changeset(expected, layer_id="1004")

    def test_get_api_changeset_return_changeset_by_user_id(self):
        expected = {
            'features': [
                {
                    'properties': {'created_at': '2017-04-12 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1003,
                                   'closed_at': '2017-04-12 00:00:00', 'layer_id': 1003,
                                   'description': 'Creating layer_1003'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-06-28 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1004,
                                   'closed_at': '2017-06-28 00:00:00', 'layer_id': 1004,
                                   'description': 'Creating layer_1004'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-04-13 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1013,
                                   'closed_at': None, 'layer_id': 1003, 'description': 'Creating an open changeset'},
                    'type': 'Changeset'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_changeset(expected, user_id_creator="1005")

    def test_get_api_changeset_return_all_open_changesets(self):
        expected = {
            'features': [
                {
                    'properties': {'created_at': '2017-01-08 00:00:00', 'user_id_creator': 1001, 'changeset_id': 1011,
                                   'closed_at': None, 'layer_id': 1001, 'description': 'An open changeset'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-04-13 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1013,
                                   'closed_at': None, 'layer_id': 1003, 'description': 'Creating an open changeset'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-01-08 00:00:00', 'user_id_creator': 1004, 'changeset_id': 1014,
                                   'closed_at': None, 'layer_id': 1002, 'description': 'An open changeset'},
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
                    'properties': {'created_at': '2017-01-05 00:00:00', 'user_id_creator': 1001, 'changeset_id': 1001,
                                   'closed_at': '2017-01-05 00:00:00', 'layer_id': 1001,
                                   'description': 'Creating layer_1001'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-03-05 00:00:00', 'user_id_creator': 1004, 'changeset_id': 1002,
                                   'closed_at': '2017-03-05 00:00:00', 'layer_id': 1002,
                                   'description': 'Creating layer_1002'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-04-12 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1003,
                                   'closed_at': '2017-04-12 00:00:00', 'layer_id': 1003,
                                   'description': 'Creating layer_1003'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-06-28 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1004,
                                   'closed_at': '2017-06-28 00:00:00', 'layer_id': 1004,
                                   'description': 'Creating layer_1004'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-08-05 00:00:00', 'user_id_creator': 1007, 'changeset_id': 1005,
                                   'closed_at': '2017-08-05 00:00:00', 'layer_id': 1005,
                                   'description': 'Creating layer_1005'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-09-04 00:00:00', 'user_id_creator': 1007, 'changeset_id': 1006,
                                   'closed_at': '2017-09-04 00:00:00', 'layer_id': 1006,
                                   'description': 'Creating layer_1006'},
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
                    'properties': {'created_at': '2017-04-13 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1013,
                                   'closed_at': None, 'layer_id': 1003, 'description': 'Creating an open changeset'},
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
                    'properties': {'created_at': '2017-06-28 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1004,
                                   'closed_at': '2017-06-28 00:00:00', 'layer_id': 1004,
                                   'description': 'Creating layer_1004'},
                    'type': 'Changeset'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_changeset(expected, closed=True, layer_id="1004")

    def test_get_api_changeset_return_all_open_changesets_by_user_id(self):
        expected = {
            'features': [
                {
                    'properties': {'created_at': '2017-01-08 00:00:00', 'user_id_creator': 1001, 'changeset_id': 1011,
                                   'closed_at': None, 'layer_id': 1001, 'description': 'An open changeset'},
                    'type': 'Changeset'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_changeset(expected, open=True, user_id_creator="1001")

    def test_get_api_changeset_return_all_closed_changesets_by_user_id(self):
        expected = {
            'features': [
                {
                    'properties': {'created_at': '2017-04-12 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1003,
                                   'closed_at': '2017-04-12 00:00:00', 'layer_id': 1003,
                                   'description': 'Creating layer_1003'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-06-28 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1004,
                                   'closed_at': '2017-06-28 00:00:00', 'layer_id': 1004,
                                   'description': 'Creating layer_1004'},
                    'type': 'Changeset'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_changeset(expected, closed=True, user_id_creator="1005")

    # changeset - create, close and delete

    def test_get_api_changeset_create_and_close_but_delete_with_admin(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': 1003},
            'type': 'Changeset'
        }
        changeset = self.tester.api_changeset_create(changeset)

        # get the id of changeset to CLOSE the changeset
        changeset_id = changeset["properties"]["changeset_id"]

        # CLOSE THE CHANGESET
        close_changeset = {
            'properties': {'changeset_id': changeset_id, 'description': 'Creating layer_1003'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        # login with admin to delete the changeset
        self.tester.auth_logout()
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # DELETE THE CHANGESET
        self.tester.api_changeset_delete(changeset_id=changeset_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_get_api_changeset_create_close_and_delete_with_admin(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': 1003},
            'type': 'Changeset'
        }
        changeset = self.tester.api_changeset_create(changeset)

        # get the id of changeset to CLOSE the changeset
        changeset_id = changeset["properties"]["changeset_id"]

        # CLOSE THE CHANGESET
        close_changeset = {
            'properties': {'changeset_id': changeset_id, 'description': 'Creating layer_1003'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        # DELETE THE CHANGESET
        self.tester.api_changeset_delete(changeset_id=changeset_id)

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

    def test_put_api_changeset_create_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        # try to create a changeset (without layer_id)
        resource = {
            'properties': {'description': 'Creating layer_1003'},
            'type': 'Changeset'
        }
        self.tester.api_changeset_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_changeset_create_error_401_unauthorized(self):
        resource = {
            'properties': {'changeset_id': -1, 'layer_id': 1003, 'description': 'Creating layer_1003'},
            'type': 'Changeset'
        }
        self.tester.api_changeset_create_error_401_unauthorized(resource)
    
    # changeset errors - close

    def test_put_api_changeset_close_error_400_bad_request(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        list_invalid_changeset_id = ["abc", 0, -1, "-1", "0"]
        
        for invalid_changeset_id in list_invalid_changeset_id:
            close_changeset = {
                'properties': {'changeset_id': invalid_changeset_id, 'description': 'Creating layer_1003'},
                'type': 'ChangesetClose'
            }
            self.tester.api_changeset_close_error_400_bad_request(close_changeset)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_changeset_close_error_401_unauthorized(self):
        list_invalid_changeset_id = ["abc", 0, -1, "-1", "0", "1001", 1001]

        for invalid_changeset_id in list_invalid_changeset_id:
            close_changeset = {
                'properties': {'changeset_id': invalid_changeset_id, 'description': 'Creating layer_1003'},
                'type': 'ChangesetClose'
            }
            self.tester.api_changeset_close_error_401_unauthorized(close_changeset)

    def test_put_api_changeset_close_error_404_not_found(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        list_invalid_changeset_id = ["5000", "5001"]

        for invalid_changeset_id in list_invalid_changeset_id:
            close_changeset = {
                'properties': {'changeset_id': invalid_changeset_id, 'description': 'Creating layer_1003'},
                'type': 'ChangesetClose'
            }
            self.tester.api_changeset_close_error_404_not_found(close_changeset)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()
    
    def test_put_api_changeset_close_error_409_conflict_changeset_is_closed(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        close_changeset = {
            'properties': {'changeset_id': 1002, 'description': 'Creating layer_1003'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close_error_409_conflict(close_changeset)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_changeset_close_error_409_conflict_user_didnt_create_the_changeset(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        close_changeset = {
            'properties': {'changeset_id': 1011, 'description': 'Creating layer_1003'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close_error_409_conflict(close_changeset)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    # changeset errors - delete

    def test_delete_api_changeset_error_400_bad_request(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_changeset_delete_error_400_bad_request(changeset_id="abc")
        self.tester.api_changeset_delete_error_400_bad_request(changeset_id=0)
        self.tester.api_changeset_delete_error_400_bad_request(changeset_id=-1)
        self.tester.api_changeset_delete_error_400_bad_request(changeset_id="-1")
        self.tester.api_changeset_delete_error_400_bad_request(changeset_id="0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_changeset_error_401_unauthorized(self):
        self.tester.api_changeset_delete_error_401_unauthorized(changeset_id="abc")
        self.tester.api_changeset_delete_error_401_unauthorized(changeset_id=0)
        self.tester.api_changeset_delete_error_401_unauthorized(changeset_id=-1)
        self.tester.api_changeset_delete_error_401_unauthorized(changeset_id="-1")
        self.tester.api_changeset_delete_error_401_unauthorized(changeset_id="0")
        self.tester.api_changeset_delete_error_401_unauthorized(changeset_id="1001")

    def test_delete_api_changeset_error_403_forbidden_non_admin_user_tries_to_delete(self):
        self.tester.auth_login("miguel@admin.com", "miguel")

        self.tester.api_changeset_delete_error_403_forbidden(changeset_id="abc")
        self.tester.api_changeset_delete_error_403_forbidden(changeset_id=0)
        self.tester.api_changeset_delete_error_403_forbidden(changeset_id=-1)
        self.tester.api_changeset_delete_error_403_forbidden(changeset_id="-1")
        self.tester.api_changeset_delete_error_403_forbidden(changeset_id="0")
        self.tester.api_changeset_delete_error_403_forbidden(changeset_id="1001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_changeset_error_404_not_found(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_changeset_delete_error_404_not_found(changeset_id="5000")
        self.tester.api_changeset_delete_error_404_not_found(changeset_id="5001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
