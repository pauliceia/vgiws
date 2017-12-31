#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from unittest import TestCase
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
                    'tags': [{'v': 'Just admins', 'k': 'description'}, {'v': 'Admins', 'k': 'name'}]
                },
                {
                    'type': 'Group',
                    'properties': {'fk_user_id': 1001, 'created_at': '2017-03-25 00:00:00',
                                   'removed_at': None, 'id': 1002, 'visible': True},
                    'tags': [{'v': '', 'k': 'description'}, {'v': 'INPE', 'k': 'name'}]
                },
                {
                    'type': 'Group',
                    'properties': {'fk_user_id': 1002, 'created_at': '2017-12-25 00:00:00',
                                   'removed_at': None, 'id': 1003, 'visible': True},
                    'tags': [{'v': '', 'k': 'description'}, {'v': 'UNIFESP SJC', 'k': 'name'}]
                },
                {
                    'type': 'Group',
                    'properties': {'fk_user_id': 1003, 'created_at': '2017-05-13 00:00:00',
                                   'removed_at': None, 'id': 1004, 'visible': True},
                    'tags': [{'v': '', 'k': 'description'}, {'v': 'UNIFESP Guarulhos', 'k': 'name'}]
                }
            ],
        }

        self.tester.api_group(expected)

    def test_get_api_layer_return_group_by_group_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Group',
                    'properties': {'fk_user_id': 1002, 'created_at': '2017-12-25 00:00:00',
                                   'removed_at': None, 'id': 1003, 'visible': True},
                    'tags': [{'v': '', 'k': 'description'}, {'v': 'UNIFESP SJC', 'k': 'name'}]
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
                    'tags': [{'v': 'Just admins', 'k': 'description'}, {'v': 'Admins', 'k': 'name'}]
                },
                {
                    'type': 'Group',
                    'properties': {'fk_user_id': 1001, 'created_at': '2017-03-25 00:00:00',
                                   'removed_at': None, 'id': 1002, 'visible': True},
                    'tags': [{'v': '', 'k': 'description'}, {'v': 'INPE', 'k': 'name'}]
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


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
