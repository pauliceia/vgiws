#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase, skip
from util.tester import UtilTester


class TestAPIUser(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # user - get

    def test_get_api_user_return_all_users(self):
        expected_at_least = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'removed_at': None, 'username': 'admin', 'terms_agreed': True,
                                   'is_email_valid': True, 'email': 'admin@admin.com', 'id': 1001,
                                   'created_at': '2017-01-01 00:00:00'},
                    'tags': [{'k': 'institution', 'v': 'INPE'}, {'k': 'name', 'v': 'Administrator'}],
                    'type': 'User'
                },
                {
                    'properties': {'removed_at': None, 'username': 'rodrigo', 'terms_agreed': True,
                                   'is_email_valid': True, 'email': 'rodrigo@admin.com', 'id': 1002,
                                   'created_at': '2017-03-03 00:00:00'},
                    'tags': [{'k': 'institution', 'v': 'INPE'}, {'k': 'name', 'v': 'Rodrigo'}],
                    'type': 'User'
                },
                {
                    'properties': {'removed_at': None, 'username': 'miguel', 'terms_agreed': True,
                                   'is_email_valid': False, 'email': 'miguel@admin.com', 'id': 1003,
                                   'created_at': '2017-05-08 00:00:00'},
                    'tags': [{'k': 'name', 'v': 'Miguel'}],
                    'type': 'User'
                },
                {
                    'properties': {'removed_at': None, 'username': 'rafael', 'terms_agreed': False,
                                   'is_email_valid': True, 'email': 'rafael@admin.com', 'id': 1004,
                                   'created_at': '2017-06-09 00:00:00'},
                    'tags': [{'k': 'name', 'v': 'Rafael'}],
                    'type': 'User'
                },
                {
                    'properties': {'removed_at': None, 'username': 'gabriel', 'terms_agreed': False,
                                   'is_email_valid': False, 'email': 'gabriel@admin.com', 'id': 1005,
                                   'created_at': '2017-09-20 00:00:00'},
                    'tags': [{'k': 'name', 'v': 'Gabriel'}],
                    'type': 'User'
                }
            ]
        }

        self.tester.api_user(expected_at_least=expected_at_least)

    def test_get_api_user_return_user_by_user_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'removed_at': None, 'username': 'rodrigo', 'terms_agreed': True,
                                   'is_email_valid': True, 'email': 'rodrigo@admin.com', 'id': 1002,
                                   'created_at': '2017-03-03 00:00:00'},
                    'tags': [{'k': 'institution', 'v': 'INPE'}, {'k': 'name', 'v': 'Rodrigo'}],
                    'type': 'User'
                }
            ]
        }

        self.tester.api_user(expected, user_id="1002")


class TestAPIUserErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # user errors - get

    def test_get_api_user_error_400_bad_request(self):
        self.tester.api_user_error_400_bad_request(user_id="abc")
        self.tester.api_user_error_400_bad_request(user_id=0)
        self.tester.api_user_error_400_bad_request(user_id=-1)
        self.tester.api_user_error_400_bad_request(user_id="-1")
        self.tester.api_user_error_400_bad_request(user_id="0")

    def test_get_api_user_error_404_not_found(self):
        self.tester.api_user_error_404_not_found(user_id="999")
        self.tester.api_user_error_404_not_found(user_id="998")


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
