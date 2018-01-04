#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase, skip
from util.tester import UtilTester


class TestAPIGroup(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # group - get

    def test_get_api_group_return_all_groups(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Group',
                    'properties': {'fk_user_id': 1001, 'created_at': '2017-01-01 00:00:00',
                                   'removed_at': None, 'id': 1001, 'visible': True},
                    'tags': [{'v': 'Just admins', 'k': 'description'},
                             {'v': 'Admins', 'k': 'name'},
                             {'v': 'private', 'k': 'type'}]
                },
                {
                    'type': 'Group',
                    'properties': {'fk_user_id': 1001, 'created_at': '2017-03-25 00:00:00',
                                   'removed_at': None, 'id': 1002, 'visible': True},
                    'tags': [{'v': '', 'k': 'description'},
                             {'v': 'INPE', 'k': 'name'},
                             {'v': 'private', 'k': 'type'}]
                },
                {
                    'type': 'Group',
                    'properties': {'fk_user_id': 1002, 'created_at': '2017-12-25 00:00:00',
                                   'removed_at': None, 'id': 1003, 'visible': True},
                    'tags': [{'v': '', 'k': 'description'},
                             {'v': 'UNIFESP SJC', 'k': 'name'},
                             {'v': 'public', 'k': 'type'}]
                },
                {
                    'type': 'Group',
                    'properties': {'fk_user_id': 1003, 'created_at': '2017-05-13 00:00:00',
                                   'removed_at': None, 'id': 1004, 'visible': True},
                    'tags': [{'v': '', 'k': 'description'},
                             {'v': 'UNIFESP Guarulhos', 'k': 'name'},
                             {'v': 'private', 'k': 'type'}]
                }
            ],
        }

        self.tester.api_group(expected)

    def test_get_api_group_return_group_by_group_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Group',
                    'properties': {'fk_user_id': 1002, 'created_at': '2017-12-25 00:00:00',
                                   'removed_at': None, 'id': 1003, 'visible': True},
                    'tags': [{'v': '', 'k': 'description'},
                             {'v': 'UNIFESP SJC', 'k': 'name'},
                             {'v': 'public', 'k': 'type'}]
                }
            ],
        }

        self.tester.api_group(expected, group_id="1003")

    def test_get_api_group_return_group_by_user_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Group',
                    'properties': {'fk_user_id': 1001, 'created_at': '2017-01-01 00:00:00',
                                   'removed_at': None, 'id': 1001, 'visible': True},
                    'tags': [{'v': 'Just admins', 'k': 'description'},
                             {'v': 'Admins', 'k': 'name'},
                             {'v': 'private', 'k': 'type'}]
                },
                {
                    'type': 'Group',
                    'properties': {'fk_user_id': 1001, 'created_at': '2017-03-25 00:00:00',
                                   'removed_at': None, 'id': 1002, 'visible': True},
                    'tags': [{'v': '', 'k': 'description'},
                             {'v': 'INPE', 'k': 'name'},
                             {'v': 'private', 'k': 'type'}]
                },
            ],
        }

        self.tester.api_group(expected, user_id="1001")

    # group - create and delete

    def test_get_api_group_create_and_delete(self):
        # DO LOGIN
        self.tester.auth_login()

        # create a group
        feature = {
            'type': 'Group',
            'properties': {'id': -1, 'fk_user_id': 1002},
            'tags': [{'k': 'description', 'v': 'group of my institution'},
                     {'k': 'name', 'v': 'VS'}]
        }

        feature = self.tester.api_group_create(feature)

        # get the id of feature to REMOVE it
        feature_id = feature["properties"]["id"]

        # REMOVE THE group AFTER THE TESTS
        self.tester.api_group_delete(feature_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPIGroupErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # group errors - get

    def test_get_api_group_error_400_bad_request(self):
        self.tester.api_group_error_400_bad_request(group_id="abc")
        self.tester.api_group_error_400_bad_request(group_id=0)
        self.tester.api_group_error_400_bad_request(group_id=-1)
        self.tester.api_group_error_400_bad_request(group_id="-1")
        self.tester.api_group_error_400_bad_request(group_id="0")

    def test_get_api_group_error_404_not_found(self):
        self.tester.api_group_error_404_not_found(group_id="999")
        self.tester.api_group_error_404_not_found(group_id="998")

    # group errors - create

    def test_put_api_group_create_error_403_forbidden(self):
        feature = {
            'type': 'group',
            'properties': {'id': -1, 'fk_group_id': 1001},
            'tags': [{'k': 'name', 'v': 'test group'},
                     {'k': 'url', 'v': 'http://somehost.com'}]
        }
        self.tester.api_group_create_error_403_forbidden(feature)

    # group errors - delete

    def test_delete_api_group_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login()

        self.tester.api_group_delete_error_400_bad_request("abc")
        self.tester.api_group_delete_error_400_bad_request(0)
        self.tester.api_group_delete_error_400_bad_request(-1)
        self.tester.api_group_delete_error_400_bad_request("-1")
        self.tester.api_group_delete_error_400_bad_request("0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_group_error_403_forbidden(self):
        self.tester.api_group_delete_error_403_forbidden("abc")
        self.tester.api_group_delete_error_403_forbidden(0)
        self.tester.api_group_delete_error_403_forbidden(-1)
        self.tester.api_group_delete_error_403_forbidden("-1")
        self.tester.api_group_delete_error_403_forbidden("0")
        self.tester.api_group_delete_error_403_forbidden("1001")

    def test_delete_api_group_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login()

        self.tester.api_group_delete_error_404_not_found("5000")
        self.tester.api_group_delete_error_404_not_found("5001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPIUserGroup(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # user group - get

    def test_get_api_user_group_return_all_users_in_groups(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-01-01 00:00:00', 'fk_user_id': 1001,
                                   'group_permission': 'admin', 'fk_group_id': 1001,
                                   'can_receive_notification': True, 'fk_user_id_added_by': 1001}
                },
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-03-25 00:00:00', 'fk_user_id': 1002,
                                   'group_permission': 'admin', 'fk_group_id': 1001,
                                   'can_receive_notification': True, 'fk_user_id_added_by': 1001}
                },
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-05-13 00:00:00', 'fk_user_id': 1001,
                                   'group_permission': 'admin', 'fk_group_id': 1002,
                                   'can_receive_notification': True, 'fk_user_id_added_by': 1001}
                },
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-06-13 00:00:00', 'fk_user_id': 1002,
                                   'group_permission': 'admin', 'fk_group_id': 1002,
                                   'can_receive_notification': True, 'fk_user_id_added_by': 1001}
                },
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-08-15 00:00:00', 'fk_user_id': 1003,
                                   'group_permission': 'member', 'fk_group_id': 1002,
                                   'can_receive_notification': False, 'fk_user_id_added_by': 1001}
                },
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-12-08 00:00:00', 'fk_user_id': 1004,
                                   'group_permission': 'member', 'fk_group_id': 1002,
                                   'can_receive_notification': True, 'fk_user_id_added_by': 1002}
                },
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-12-12 00:00:00', 'fk_user_id': 1002,
                                   'group_permission': 'admin', 'fk_group_id': 1003,
                                   'can_receive_notification': True, 'fk_user_id_added_by': 1002}
                },
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-12-15 00:00:00', 'fk_user_id': 1003,
                                   'group_permission': 'member', 'fk_group_id': 1003,
                                   'can_receive_notification': False, 'fk_user_id_added_by': 1002}
                },
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-06-15 00:00:00', 'fk_user_id': 1001,
                                   'group_permission': 'member', 'fk_group_id': 1004,
                                   'can_receive_notification': False, 'fk_user_id_added_by': 1004}
                },
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-12-19 00:00:00', 'fk_user_id': 1002,
                                   'group_permission': 'member', 'fk_group_id': 1004,
                                   'can_receive_notification': False, 'fk_user_id_added_by': 1004}
                },
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-01-11 00:00:00', 'fk_user_id': 1003,
                                   'group_permission': 'admin', 'fk_group_id': 1004,
                                   'can_receive_notification': True, 'fk_user_id_added_by': 1003}
                },
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-05-02 00:00:00', 'fk_user_id': 1004,
                                   'group_permission': 'admin', 'fk_group_id': 1004,
                                   'can_receive_notification': True, 'fk_user_id_added_by': 1003}
                },
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-12-20 00:00:00', 'fk_user_id': 1005,
                                   'group_permission': 'member', 'fk_group_id': 1004,
                                   'can_receive_notification': True, 'fk_user_id_added_by': 1004}
                },
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-01-10 00:00:00', 'fk_user_id': 1003,
                                   'group_permission': 'admin', 'fk_group_id': 1005,
                                   'can_receive_notification': True, 'fk_user_id_added_by': 1003}
                },
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-01-10 00:00:00', 'fk_user_id': 1004,
                                   'group_permission': 'admin', 'fk_group_id': 1006,
                                   'can_receive_notification': True, 'fk_user_id_added_by': 1004}
                }
            ]
        }

        self.tester.api_user_group(expected)

    def test_get_api_user_group_return_users_by_group_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-06-15 00:00:00', 'fk_user_id': 1001,
                                   'group_permission': 'member', 'fk_group_id': 1004,
                                   'can_receive_notification': False, 'fk_user_id_added_by': 1004}
                },
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-12-19 00:00:00', 'fk_user_id': 1002,
                                   'group_permission': 'member', 'fk_group_id': 1004,
                                   'can_receive_notification': False, 'fk_user_id_added_by': 1004}
                },
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-01-11 00:00:00', 'fk_user_id': 1003,
                                   'group_permission': 'admin', 'fk_group_id': 1004,
                                   'can_receive_notification': True, 'fk_user_id_added_by': 1003}
                },
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-05-02 00:00:00', 'fk_user_id': 1004,
                                   'group_permission': 'admin', 'fk_group_id': 1004,
                                   'can_receive_notification': True, 'fk_user_id_added_by': 1003}
                },
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-12-20 00:00:00', 'fk_user_id': 1005,
                                   'group_permission': 'member', 'fk_group_id': 1004,
                                   'can_receive_notification': True, 'fk_user_id_added_by': 1004}
                }
            ]
        }

        self.tester.api_user_group(expected, group_id="1004")

    def test_get_api_user_group_return_groups_by_user_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-01-01 00:00:00', 'fk_user_id': 1001,
                                   'group_permission': 'admin', 'fk_group_id': 1001,
                                   'can_receive_notification': True, 'fk_user_id_added_by': 1001}
                },
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-05-13 00:00:00', 'fk_user_id': 1001,
                                   'group_permission': 'admin', 'fk_group_id': 1002,
                                   'can_receive_notification': True, 'fk_user_id_added_by': 1001}
                },
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-06-15 00:00:00', 'fk_user_id': 1001,
                                   'group_permission': 'member', 'fk_group_id': 1004,
                                   'can_receive_notification': False, 'fk_user_id_added_by': 1004}
                }
            ]
        }

        self.tester.api_user_group(expected, user_id="1001")

    def test_get_api_user_group_return_information_by_user_id_and_group_id(self):
        """
        Return the information of that user in that group
        """

        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'UserGroup',
                    'properties': {'added_at': '2017-12-15 00:00:00', 'fk_user_id': 1003,
                                   'group_permission': 'member', 'fk_group_id': 1003,
                                   'can_receive_notification': False, 'fk_user_id_added_by': 1002}
                }
            ]
        }

        self.tester.api_user_group(expected, group_id="1003", user_id="1003")

    # user group - create and delete

    def test_get_api_user_group_create_and_delete(self):
        # DO LOGIN
        self.tester.auth_login()

        # create user in a group that can receive notification
        feature = {
            'type': 'UserGroup',
            'properties': {'fk_user_id': 1004, 'fk_group_id': 1003,
                           'can_receive_notification': True, 'fk_user_id_added_by': 1002}
        }

        self.tester.api_user_group_create(feature)

        # get the id of feature to REMOVE it
        user_id = feature["properties"]["fk_user_id"]
        group_id = feature["properties"]["fk_group_id"]

        # REMOVE THE group AFTER THE TESTS
        self.tester.api_user_group_delete(user_id=user_id, group_id=group_id)

        # create user in a group that cannot receive notification
        feature = {
            'type': 'UserGroup',
            'properties': {'fk_user_id': 1002, 'fk_group_id': 1005,
                           'can_receive_notification': False, 'fk_user_id_added_by': 1003}
        }

        self.tester.api_user_group_create(feature)

        # get the id of feature to REMOVE it
        user_id = feature["properties"]["fk_user_id"]
        group_id = feature["properties"]["fk_group_id"]

        # REMOVE THE group AFTER THE TESTS
        self.tester.api_user_group_delete(user_id=user_id, group_id=group_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPIUserGroupErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # group errors - get

    def test_get_api_user_group_error_400_bad_request(self):
        self.tester.api_user_group_error_400_bad_request(group_id="abc")
        self.tester.api_user_group_error_400_bad_request(group_id=0)
        self.tester.api_user_group_error_400_bad_request(group_id=-1)
        self.tester.api_user_group_error_400_bad_request(group_id="-1")
        self.tester.api_user_group_error_400_bad_request(group_id="0")

        self.tester.api_user_group_error_400_bad_request(user_id="abc")
        self.tester.api_user_group_error_400_bad_request(user_id=0)
        self.tester.api_user_group_error_400_bad_request(user_id=-1)
        self.tester.api_user_group_error_400_bad_request(user_id="-1")
        self.tester.api_user_group_error_400_bad_request(user_id="0")

        self.tester.api_user_group_error_400_bad_request(user_id="abc", group_id="0")
        self.tester.api_user_group_error_400_bad_request(user_id=0, group_id="abc")
        self.tester.api_user_group_error_400_bad_request(user_id=-1, group_id=0)
        self.tester.api_user_group_error_400_bad_request(user_id="-1", group_id=-11)
        self.tester.api_user_group_error_400_bad_request(user_id="0", group_id="1")

    def test_get_api_user_group_error_404_not_found(self):
        self.tester.api_user_group_error_404_not_found(group_id="999")
        self.tester.api_user_group_error_404_not_found(group_id="998")

        self.tester.api_user_group_error_404_not_found(user_id="999")
        self.tester.api_user_group_error_404_not_found(user_id="998")

        self.tester.api_user_group_error_404_not_found(group_id="998", user_id="999")
        self.tester.api_user_group_error_404_not_found(group_id="999", user_id="998")

    # group errors - create

    def test_put_api_user_group_create_error_403_forbidden(self):
        feature = {
            'type': 'group',
            'properties': {'id': -1, 'fk_group_id': 1001},
            'tags': [{'k': 'name', 'v': 'test group'},
                     {'k': 'url', 'v': 'http://somehost.com'}]
        }

        self.tester.api_user_group_create_error_403_forbidden(feature)

    def test_put_api_user_group_create_error_400_bad_request(self):
        """
        The user_id is already added in group_id
        """

        # DO LOGIN
        self.tester.auth_login()

        # create user in a group that can receive notification
        feature = {
            'type': 'UserGroup',
            'properties': {'fk_user_id': 1003, 'fk_group_id': 1003,
                           'can_receive_notification': True, 'fk_user_id_added_by': 1002}
        }

        feature = self.tester.api_user_group_create_error_400_bad_request(feature)

        # create user in a group that cannot receive notification
        feature = {
            'type': 'UserGroup',
            'properties': {'fk_user_id': 1002, 'fk_group_id': 1004,
                           'can_receive_notification': False, 'fk_user_id_added_by': 1002}
        }

        feature = self.tester.api_user_group_create_error_400_bad_request(feature)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    # group errors - delete

    def test_delete_api_user_group_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login()

        self.tester.api_user_group_delete_error_400_bad_request(user_id="abc", group_id="0")
        self.tester.api_user_group_delete_error_400_bad_request(user_id=0, group_id="abc")
        self.tester.api_user_group_delete_error_400_bad_request(user_id=-1, group_id=0)
        self.tester.api_user_group_delete_error_400_bad_request(user_id="-1", group_id=-1)
        self.tester.api_user_group_delete_error_400_bad_request(user_id="0", group_id="1")

        # one valid and other invalid
        self.tester.api_user_group_delete_error_400_bad_request(user_id="1003", group_id=-1)
        self.tester.api_user_group_delete_error_400_bad_request(user_id="0", group_id="1003")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_user_group_error_403_forbidden(self):
        self.tester.api_user_group_delete_error_403_forbidden(user_id="abc", group_id="0")
        self.tester.api_user_group_delete_error_403_forbidden(user_id=0, group_id="abc")
        self.tester.api_user_group_delete_error_403_forbidden(user_id=-1, group_id=0)
        self.tester.api_user_group_delete_error_403_forbidden(user_id="-1", group_id=-1)
        self.tester.api_user_group_delete_error_403_forbidden(user_id="0", group_id="1")

        self.tester.api_user_group_delete_error_403_forbidden(user_id="1003", group_id=-1)
        self.tester.api_user_group_delete_error_403_forbidden(user_id="0", group_id="1003")

        self.tester.api_user_group_delete_error_403_forbidden(user_id="1003", group_id="1003")

    def test_delete_api_user_group_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login()

        self.tester.api_user_group_delete_error_404_not_found(user_id="998", group_id="998")
        self.tester.api_user_group_delete_error_404_not_found(user_id="1001", group_id="998")
        self.tester.api_user_group_delete_error_404_not_found(user_id="998", group_id="1001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
