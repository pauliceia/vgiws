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
                    'type': 'User',
                    'tags': [{'v': 'INPE', 'k': 'institution'}, {'v': 'Administrator', 'k': 'name'}],
                    'properties': {'id': 1001, 'is_email_valid': None, 'created_at': None, 'terms_agreed': None,
                                   'email': 'admin@admin.com', 'removed_at': None,
                                   'username': 'admin'}
                },
                {
                    'type': 'User',
                    'tags': [{'v': 'INPE', 'k': 'institution'}, {'v': 'Rodrigo', 'k': 'name'}],
                    'properties': {'id': 1002, 'is_email_valid': None, 'created_at': None, 'terms_agreed': None,
                                   'email': 'rodrigo@admin.com', 'removed_at': None,
                                   'username': 'rodrigo'}
                },
                {
                    'type': 'User',
                    'tags': [{'v': 'Miguel', 'k': 'name'}],
                    'properties': {'id': 1003, 'is_email_valid': None, 'created_at': None, 'terms_agreed': None,
                                   'email': 'miguel@admin.com', 'removed_at': None,
                                   'username': 'miguel'}
                },
                {
                    'type': 'User',
                    'tags': [{'v': 'Rafael', 'k': 'name'}],
                    'properties': {'id': 1004, 'is_email_valid': None, 'created_at': None, 'terms_agreed': None,
                                   'email': 'rafael@admin.com', 'removed_at': None,
                                   'username': 'rafael'}
                },
                {
                    'type': 'User',
                    'tags': [{'v': 'Gabriel', 'k': 'name'}],
                    'properties': {'id': 1005, 'is_email_valid': None, 'created_at': None, 'terms_agreed': None,
                                   'email': 'gabriel@admin.com', 'removed_at': None,
                                   'username': 'gabriel'}
                }
            ]
        }

        self.tester.api_user(expected_at_least=expected_at_least)

    def test_get_api_user_return_user_by_user_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'User',
                    'tags': [{'v': 'INPE', 'k': 'institution'}, {'v': 'Rodrigo', 'k': 'name'}],
                    'properties': {'id': 1002, 'is_email_valid': None, 'created_at': None, 'terms_agreed': None,
                                   'email': 'rodrigo@admin.com', 'removed_at': None,
                                   'username': 'rodrigo'}
                },
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
