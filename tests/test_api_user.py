#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase, skip
from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/

@skip("demonstrating skipping")
class TestAPIUser(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # project - get

    def test_get_api_user_return_all_users(self):
        expected = {
            'features': [
                {
                    'properties': {'removed_at': None, 'create_at': '2017-11-20 00:00:00', 'fk_user_id_owner': 1001, 'id': 1001},
                    'tags': [{'k': 'name', 'v': 'default'}, {'k': 'description', 'v': 'default project'}],
                    'type': 'Project'
                },
                {
                    'properties': {'removed_at': None, 'create_at': '2017-10-12 00:00:00', 'fk_user_id_owner': 1002, 'id': 1002},
                    'tags': [{'k': 'name', 'v': 'test_project'}, {'k': 'description', 'v': 'test_project'}],
                    'type': 'Project'
                },
                {
                    'properties': {'removed_at': None, 'create_at': '2017-12-23 00:00:00', 'fk_user_id_owner': 1002, 'id': 1003},
                    'tags': [{'k': 'name', 'v': 'project 3'}, {'k': 'description', 'v': 'test_project'}],
                    'type': 'Project'
                },
                {
                    'properties': {'removed_at': None, 'create_at': '2017-09-11 00:00:00', 'fk_user_id_owner': 1003, 'id': 1004},
                    'tags': [{'k': 'name', 'v': 'project 4'}, {'k': 'description', 'v': 'test_project'}],
                    'type': 'Project'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_user(expected)

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
