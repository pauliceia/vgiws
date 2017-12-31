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

    @unittest.skip(">>> skipping...")
    def test_get_api_group_return_all_layers(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'group',
                    'properties': {'fk_user_id': 1001, 'create_at': '2017-11-20 00:00:00',
                                   'id': 1001, 'removed_at': None, 'fk_group_id': 1001},
                    'tags': [{'k': 'description', 'v': 'default group'}, {'k': 'name', 'v': 'admin'}]
                },
                {
                    'type': 'group',
                    'properties': {'fk_user_id': 1002, 'create_at': '2017-10-12 00:00:00',
                                   'id': 1002, 'removed_at': None, 'fk_group_id': 1001},
                    'tags': [{'k': 'name', 'v': 'test group'}, {'k': 'url', 'v': 'http://somehost.com'}]
                },
                {
                    'type': 'group',
                    'properties': {'fk_user_id': 1002, 'create_at': '2017-12-23 00:00:00',
                                   'id': 1003, 'removed_at': None, 'fk_group_id': 1002},
                    'tags': [{'k': 'name', 'v': 'hello world'}]
                },
                {
                    'type': 'group',
                    'properties': {'fk_user_id': 1004, 'create_at': '2017-09-11 00:00:00',
                                   'id': 1004, 'removed_at': None, 'fk_group_id': 1002},
                    'tags': None
                }
            ]
        }

        self.tester.api_group(expected)

    @unittest.skip(">>> skipping...")
    def test_get_api_layer_return_group_by_group_id(self):
        expected = {
            'features': [
                {
                    'type': 'group',
                    'properties': {'fk_user_id': 1001, 'create_at': '2017-11-20 00:00:00',
                                   'id': 1001, 'removed_at': None, 'fk_group_id': 1001},
                    'tags': [{'k': 'description', 'v': 'default group'}, {'k': 'name', 'v': 'admin'}]
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_group(expected, group_id="1001")

    @unittest.skip(">>> skipping...")
    def test_get_api_group_return_group_by_group_id(self):
        expected = {
            'features': [
                {
                    'type': 'group',
                    'properties': {'fk_user_id': 1002, 'create_at': '2017-12-23 00:00:00',
                                   'id': 1003, 'removed_at': None, 'fk_group_id': 1002},
                    'tags': [{'k': 'name', 'v': 'hello world'}]
                },
                {
                    'type': 'group',
                    'properties': {'fk_user_id': 1004, 'create_at': '2017-09-11 00:00:00',
                                   'id': 1004, 'removed_at': None, 'fk_group_id': 1002},
                    'tags': None
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_group(expected, group_id="1002")

    @unittest.skip(">>> skipping...")
    def test_get_api_group_return_group_by_user_id(self):
        expected = {
            'features': [
                {
                    'type': 'group',
                    'properties': {'fk_user_id': 1002, 'create_at': '2017-10-12 00:00:00',
                                   'id': 1002, 'removed_at': None, 'fk_group_id': 1001},
                    'tags': [{'k': 'name', 'v': 'test group'}, {'k': 'url', 'v': 'http://somehost.com'}]
                },
                {
                    'type': 'group',
                    'properties': {'fk_user_id': 1002, 'create_at': '2017-12-23 00:00:00',
                                   'id': 1003, 'removed_at': None, 'fk_group_id': 1002},
                    'tags': [{'k': 'name', 'v': 'hello world'}]
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_group(expected, user_id="1002")

    # group - create and delete
    @unittest.skip(">>> skipping...")
    def test_get_api_group_create_and_delete(self):
        # DO LOGIN
        self.tester.auth_login()

        # create a group
        feature = {
            'type': 'group',
            'properties': {'id': -1, 'fk_group_id': 1001},
            'tags': [{'k': 'name', 'v': 'test group'},
                     {'k': 'url', 'v': 'http://somehost.com'}]
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
