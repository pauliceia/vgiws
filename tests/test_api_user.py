#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase, skip
from util.tester import UtilTester

from string import ascii_uppercase, digits
from random import choice


def generate_random_string(size=6, chars=ascii_uppercase + digits):
    """
    Source: https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
    """
    return ''.join(choice(chars) for _ in range(size))


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
                    'tags': {'institution': 'INPE', 'name': 'Administrator'},
                    'type': 'User'
                },
                {
                    'properties': {'removed_at': None, 'username': 'rodrigo', 'terms_agreed': True,
                                   'is_email_valid': True, 'email': 'rodrigo@admin.com', 'id': 1002,
                                   'created_at': '2017-03-03 00:00:00'},
                    'tags': {'institution': 'INPE', 'name': 'Rodrigo'},
                    'type': 'User'
                },
                {
                    'properties': {'removed_at': None, 'username': 'miguel', 'terms_agreed': True,
                                   'is_email_valid': False, 'email': 'miguel@admin.com', 'id': 1003,
                                   'created_at': '2017-05-08 00:00:00'},
                    'tags': {'name': 'Miguel'},
                    'type': 'User'
                },
                {
                    'properties': {'removed_at': None, 'username': 'rafael', 'terms_agreed': False,
                                   'is_email_valid': True, 'email': 'rafael@admin.com', 'id': 1004,
                                   'created_at': '2017-06-09 00:00:00'},
                    'tags': {'name': 'Rafael'},
                    'type': 'User'
                },
                {
                    'properties': {'removed_at': None, 'username': 'gabriel', 'terms_agreed': False,
                                   'is_email_valid': False, 'email': 'gabriel@admin.com', 'id': 1005,
                                   'created_at': '2017-09-20 00:00:00'},
                    'tags': {'name': 'Gabriel'},
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
                    'tags': {'name': 'Rodrigo', 'institution': 'INPE'},
                    'type': 'User'
                }
            ]
        }

        self.tester.api_user(expected, user_id="1002")

    # user - create and delete

    def test_get_api_user_create_and_delete(self):
        # create a fake email to avoid the error when exist the same email in DB
        email = generate_random_string() + "@roger.com"

        # create a feature
        feature = {
            'type': 'User',
            'tags': {},
            'properties': {'id': -1, 'email': email,
                           'password': 'roger', 'username': 'roger'}
        }

        feature = self.tester.api_user_create(feature)

        email = feature["properties"]["email"]
        password = feature["properties"]["password"]

        # login with the user created
        self.tester.auth_login(email, password)

        # get the id of feature to REMOVE it
        feature_id = feature["properties"]["id"]

        # remove the user created
        self.tester.api_user_delete(feature_id)

        # when the user delete itself, it is automatically logout, because of that, raise a 404
        self.tester.auth_logout_404_not_found()


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

    # user errors - delete

    def test_delete_api_user_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login_fake()

        self.tester.api_user_delete_error_400_bad_request("abc")
        self.tester.api_user_delete_error_400_bad_request(0)
        self.tester.api_user_delete_error_400_bad_request(-1)
        self.tester.api_user_delete_error_400_bad_request("-1")
        self.tester.api_user_delete_error_400_bad_request("0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_user_error_403_forbidden(self):
        self.tester.api_user_delete_error_403_forbidden("abc")
        self.tester.api_user_delete_error_403_forbidden(0)
        self.tester.api_user_delete_error_403_forbidden(-1)
        self.tester.api_user_delete_error_403_forbidden("-1")
        self.tester.api_user_delete_error_403_forbidden("0")
        self.tester.api_user_delete_error_403_forbidden("1001")

    def test_delete_api_user_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login_fake()

        self.tester.api_user_delete_error_404_not_found("5000")
        self.tester.api_user_delete_error_404_not_found("5001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
