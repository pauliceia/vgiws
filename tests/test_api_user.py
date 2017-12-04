#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase, skip
from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/

class TestAPIUser(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # project - get

    def test_get_api_user_return_all_users(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'User',
                    'tags': None,
                    'properties': {'id': 1, 'is_email_valid': None, 'create_at': None, 'terms_agreed': None,
                                   'description': None, 'email': 'test@fake.login', 'name': None,
                                   'terms_seen': None, 'removed_at': None, 'username': None}
                },
                {
                    'type': 'User',
                    'tags': [{'v': 'INPE', 'k': 'institution'}],
                    'properties': {'id': 1001, 'is_email_valid': None, 'create_at': None, 'terms_agreed': None,
                                   'description': None, 'email': 'admin@admin.com', 'name': 'Administrator',
                                   'terms_seen': None, 'removed_at': None, 'username': 'admin'}
                },
                {
                    'type': 'User',
                    'tags': [{'v': 'INPE', 'k': 'institution'}],
                    'properties': {'id': 1002, 'is_email_valid': None, 'create_at': None, 'terms_agreed': None,
                                   'description': None, 'email': 'rodrigo@admin.com', 'name': 'Rodrigo',
                                   'terms_seen': None, 'removed_at': None, 'username': 'rodrigo'}
                },
                {
                    'type': 'User',
                    'tags': None,
                    'properties': {'id': 1003, 'is_email_valid': None, 'create_at': None, 'terms_agreed': None,
                                   'description': None, 'email': 'miguel@admin.com', 'name': 'Miguel',
                                   'terms_seen': None, 'removed_at': None, 'username': 'miguel'}
                },
                {
                    'type': 'User',
                    'tags': None,
                    'properties': {'id': 1004, 'is_email_valid': None, 'create_at': None, 'terms_agreed': None,
                                   'description': None, 'email': 'rafael@admin.com', 'name': 'Rafael',
                                   'terms_seen': None, 'removed_at': None, 'username': 'rafael'}
                },
                {
                    'type': 'User',
                    'tags': None,
                    'properties': {'id': 1005, 'is_email_valid': None, 'create_at': None, 'terms_agreed': None,
                                   'description': None, 'email': 'gabriel@admin.com', 'name': 'Gabriel',
                                   'terms_seen': None, 'removed_at': None, 'username': 'gabriel'}
                }
            ]
        }

        self.tester.api_user(expected)

    @skip("demonstrating skipping")
    def test_get_api_user_return_user_by_user_id(self):
        expected = {
            'features': [
                {
                    'properties': {'removed_at': None, 'create_at': '2017-10-12 00:00:00',
                                   'fk_user_id_owner': 1002,'id': 1002},
                    'tags': [{'k': 'name', 'v': 'test_project'},
                             {'k': 'description', 'v': 'test_project'}],
                    'type': 'Project'
                },
                {
                    'properties': {'removed_at': None, 'create_at': '2017-12-23 00:00:00',
                                   'fk_user_id_owner': 1002, 'id': 1003},
                    'tags': [{'k': 'name', 'v': 'project 3'},
                             {'k': 'description', 'v': 'test_project'}],
                    'type': 'Project'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_user(expected, user_id="1002")


@skip("demonstrating skipping")
class TestAPIUserErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # project errors - get

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
