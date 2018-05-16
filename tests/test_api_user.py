#!/usr/bin/env python
# -*- coding: utf-8 -*-



from unittest import TestCase, skip
from util.tester import UtilTester

from string import ascii_uppercase, digits
from random import choice


def generate_random_string(size=6, chars=ascii_uppercase + digits):
    """
    #Source: https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
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
                    'type': 'User',
                    'properties': {'receive_notification_by_email': False, 'terms_agreed': True,
                                   'username': 'admin', 'user_id': 1001, 'email': 'admin@admin.com',
                                   'name': 'Administrator', 'is_the_admin': True, 'can_add_layer': True,
                                   'created_at': '2017-01-01 00:00:00', 'login_date': '2017-01-01T00:00:00',
                                   'is_email_valid': True}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': False, 'terms_agreed': True,
                                   'username': 'rodrigo', 'user_id': 1002, 'email': 'rodrigo@admin.com',
                                   'name': 'Rodrigo', 'is_the_admin': True, 'can_add_layer': True,
                                   'created_at': '2017-03-03 00:00:00', 'login_date': '2017-03-03T00:00:00',
                                   'is_email_valid': True}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': False, 'terms_agreed': True,
                                   'username': 'miguel', 'user_id': 1003, 'email': 'miguel@admin.com',
                                   'name': 'Miguel', 'is_the_admin': True, 'can_add_layer': True,
                                   'created_at': '2017-05-08 00:00:00', 'login_date': '2017-05-08T00:00:00',
                                   'is_email_valid': False}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': False,
                                   'username': 'rafael', 'user_id': 1004, 'email': 'rafael@admin.com',
                                   'name': 'Rafael', 'is_the_admin': False, 'can_add_layer': True,
                                   'created_at': '2017-06-09 00:00:00', 'login_date': '2017-06-09T00:00:00',
                                   'is_email_valid': True}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': False,
                                   'username': 'gabriel', 'user_id': 1005, 'email': 'gabriel@admin.com',
                                   'name': 'Gabriel', 'is_the_admin': False, 'can_add_layer': True,
                                   'created_at': '2017-09-20 00:00:00', 'login_date': '2017-09-20T00:00:00',
                                   'is_email_valid': False}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': False,
                                   'username': 'fernanda', 'user_id': 1006, 'email': 'fernanda@gmail.com',
                                   'name': None, 'is_the_admin': False, 'can_add_layer': False,
                                   'created_at': '2017-01-19 00:00:00', 'login_date': '2017-01-19T00:00:00',
                                   'is_email_valid': True}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': False, 'terms_agreed': True,
                                   'username': 'ana', 'user_id': 1007, 'email': 'ana@gmail.com',
                                   'name': None, 'is_the_admin': False, 'can_add_layer': False,
                                   'created_at': '2017-01-18 00:00:00', 'login_date': '2017-01-18T00:00:00',
                                   'is_email_valid': False}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': False, 'terms_agreed': False,
                                   'username': 'bea', 'user_id': 1008, 'email': 'bea@gmail.com',
                                   'name': None, 'is_the_admin': False, 'can_add_layer': False,
                                   'created_at': '2017-01-30 00:00:00', 'login_date': '2017-01-30T00:00:00',
                                   'is_email_valid': False}
                }
            ]
        }

        self.tester.api_user(expected_at_least=expected_at_least)

    def test_get_api_user_return_user_by_user_id(self):
        expected = {
            'features': [
                {'properties': {'name': 'Rodrigo', 'login_date': '2017-03-03T00:00:00', 'terms_agreed': True,
                                'receive_notification_by_email': False, 'user_id': 1002, 'username': 'rodrigo',
                                'is_email_valid': True, 'is_the_admin': True, 'email': 'rodrigo@admin.com',
                                'can_add_layer': True, 'created_at': '2017-03-03 00:00:00'},
                 'type': 'User'}
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_user(expected, user_id="1002")

    # user - create and delete

    def test_get_api_user_create_and_delete(self):
        # create a fake email to avoid the error when exist the same email in DB
        email = generate_random_string() + "@roger.com"

        # create a feature
        feature = {
            'type': 'User',
            'properties': {'user_id': -1, 'email': email, 'password': 'roger', 'username': 'roger'}
        }

        feature = self.tester.api_user_create(feature)

        email = feature["properties"]["email"]
        password = feature["properties"]["password"]

        # login with the user created
        self.tester.auth_login(email, password)

        # get the id of feature to REMOVE it
        feature_id = feature["properties"]["user_id"]

        # logout
        self.tester.auth_logout()

        ##################################################
        # log in with a admin user (who can delete an user)
        ##################################################
        self.tester.auth_login("admin@admin.com", "admin")

        # remove the user created
        self.tester.api_user_delete(feature_id)

        # logout
        self.tester.auth_logout()


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
        # DO LOGIN
        self.tester.auth_login("admin@admin.com", "admin")

        self.tester.api_user_delete_error_400_bad_request("abc")
        self.tester.api_user_delete_error_400_bad_request(0)
        self.tester.api_user_delete_error_400_bad_request(-1)
        self.tester.api_user_delete_error_400_bad_request("-1")
        self.tester.api_user_delete_error_400_bad_request("0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_user_error_403_forbidden_user_without_login(self):
        self.tester.api_user_delete_error_403_forbidden("abc")
        self.tester.api_user_delete_error_403_forbidden(0)
        self.tester.api_user_delete_error_403_forbidden(-1)
        self.tester.api_user_delete_error_403_forbidden("-1")
        self.tester.api_user_delete_error_403_forbidden("0")
        self.tester.api_user_delete_error_403_forbidden("1001")

    def test_delete_api_user_error_403_forbidden_user_cannot_delete_other_user(self):
        # create a fake email to avoid the error when exist the same email in DB
        email = generate_random_string() + "@roger.com"

        # create a feature
        feature = {
            'type': 'User',
            'properties': {'user_id': -1, 'email': email, 'password': 'roger', 'username': 'roger'}
        }

        feature = self.tester.api_user_create(feature)

        email = feature["properties"]["email"]
        password = feature["properties"]["password"]

        # login with the user created
        self.tester.auth_login(email, password)

        # get the id of feature to REMOVE it
        feature_id = feature["properties"]["user_id"]

        # try to remove the user created, but get a 403, because just admin can delete users
        self.tester.api_user_delete_error_403_forbidden(feature_id)

        # logout
        self.tester.auth_logout()

        ##################################################
        # log in with a admin user (who can delete an user)
        ##################################################
        self.tester.auth_login("admin@admin.com", "admin")

        # remove the user created
        self.tester.api_user_delete(feature_id)

        # logout
        self.tester.auth_logout()

    def test_delete_api_user_error_404_not_found(self):
        # DO LOGIN
        self.tester.auth_login("admin@admin.com", "admin")

        self.tester.api_user_delete_error_404_not_found("5000")
        self.tester.api_user_delete_error_404_not_found("5001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
