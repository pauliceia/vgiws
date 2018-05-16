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

    # def test_get_api_user_return_all_users(self):
    #     expected_at_least = {
    #         'features': [
    #             {
    #                 'properties': {'username': 'admin', 'name': 'Administrator', 'id': 1001,
    #                                'created_at': '2017-01-01 00:00:00', 'email': 'admin@admin.com', 'terms_agreed': True,
    #                                'is_email_valid': True},
    #                 'type': 'User',
    #                 'auth': {'is_curator': True, 'id': 1001, 'is_manager': True, 'is_admin': True}
    #             },
    #             {
    #                 'properties': {'username': 'rodrigo', 'name': 'Rodrigo', 'id': 1002,
    #                                'created_at': '2017-03-03 00:00:00', 'email': 'rodrigo@admin.com', 'terms_agreed': True,
    #                                'is_email_valid': True},
    #                 'type': 'User',
    #                 'auth': {'is_curator': True, 'id': 1002, 'is_manager': True, 'is_admin': True}
    #             },
    #             {
    #                 'properties': {'username': 'miguel', 'name': 'Miguel', 'id': 1003, 'created_at': '2017-05-08 00:00:00',
    #                                'email': 'miguel@admin.com', 'terms_agreed': True, 'is_email_valid': False},
    #                 'type': 'User',
    #                 'auth': {'is_curator': True, 'id': 1003, 'is_manager': True, 'is_admin': False}
    #             },
    #             {
    #                 'properties': {'username': 'rafael', 'name': 'Rafael', 'id': 1004, 'created_at': '2017-06-09 00:00:00',
    #                                'email': 'rafael@admin.com', 'terms_agreed': False, 'is_email_valid': True},
    #                 'type': 'User',
    #                 'auth': {'is_curator': True, 'id': 1004, 'is_manager': False, 'is_admin': False}
    #             },
    #             {
    #                 'properties': {'username': 'gabriel', 'name': 'Gabriel', 'id': 1005, 'created_at': '2017-09-20 00:00:00',
    #                                'email': 'gabriel@admin.com', 'terms_agreed': False, 'is_email_valid': False},
    #                 'type': 'User',
    #                 'auth': {'is_curator': True, 'id': 1005, 'is_manager': False, 'is_admin': False}
    #             },
    #             {
    #                 'properties': {'username': 'fernanda', 'name': None, 'id': 1006, 'created_at': '2017-01-19 00:00:00',
    #                                'email': 'fernanda@gmail.com', 'terms_agreed': False, 'is_email_valid': True},
    #                 'type': 'User',
    #                 'auth': {'is_curator': True, 'id': 1006, 'is_manager': False, 'is_admin': False}
    #             },
    #             {
    #                 'properties': {'username': 'ana', 'name': None, 'id': 1007, 'created_at': '2017-01-18 00:00:00',
    #                                'email': 'ana@gmail.com', 'terms_agreed': True, 'is_email_valid': False},
    #                 'type': 'User', 'auth': {'is_curator': False, 'id': 1007, 'is_manager': False, 'is_admin': False}
    #             },
    #             {
    #                 'properties': {'username': 'bea', 'name': None, 'id': 1008, 'created_at': '2017-01-30 00:00:00',
    #                                'email': 'bea@gmail.com', 'terms_agreed': False, 'is_email_valid': False},
    #                 'type': 'User',
    #                 'auth': {'is_curator': False, 'id': 1008, 'is_manager': False, 'is_admin': False}
    #             }
    #         ],
    #         'type': 'FeatureCollection',
    #     }
    #
    #     self.tester.api_user(expected_at_least=expected_at_least)

    # def test_get_api_user_return_user_by_user_id(self):
    #     expected = {
    #         'type': 'FeatureCollection',
    #         'features': [
    #             {
    #                 'properties': {'username': 'rodrigo', 'name': 'Rodrigo', 'id': 1002,
    #                                'created_at': '2017-03-03 00:00:00', 'email': 'rodrigo@admin.com',
    #                                'terms_agreed': True, 'is_email_valid': True},
    #                 'type': 'User',
    #                 'auth': {'is_curator': True, 'id': 1002, 'is_manager': True, 'is_admin': True}
    #             }
    #         ]
    #     }
    #
    #     self.tester.api_user(expected, user_id="1002")

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


"""
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

"""

# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
