#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester

from modules import generate_random_string
from modules.common import generate_encoded_jwt_token


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
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': True,
                                   'username': 'admin', 'user_id': 1001, 'email': 'admin@admin.com',
                                   'name': 'Administrator', 'is_the_admin': True,
                                   'created_at': '2017-01-01 00:00:00', 'login_date': '2017-01-01T00:00:00',
                                   'is_email_valid': True, 'picture': '', 'social_id': '', 'social_account': ''}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': True,
                                   'username': 'rodrigo', 'user_id': 1002, 'email': 'rodrigo@admin.com',
                                   'name': 'Rodrigo', 'is_the_admin': True,
                                   'created_at': '2017-03-03 00:00:00', 'login_date': '2017-03-03T00:00:00',
                                   'is_email_valid': True, 'picture': '', 'social_id': '', 'social_account': ''}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': True,
                                   'username': 'miguel', 'user_id': 1003, 'email': 'miguel@admin.com',
                                   'name': 'Miguel', 'is_the_admin': False,
                                   'created_at': '2017-05-08 00:00:00', 'login_date': '2017-05-08T00:00:00',
                                   'is_email_valid': True, 'picture': '', 'social_id': '', 'social_account': ''}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': False,
                                   'username': 'rafael', 'user_id': 1004, 'email': 'rafael@admin.com',
                                   'name': 'Rafael', 'is_the_admin': False,
                                   'created_at': '2017-06-09 00:00:00', 'login_date': '2017-06-09T00:00:00',
                                   'is_email_valid': True, 'picture': '', 'social_id': '', 'social_account': ''}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': False,
                                   'username': 'gabriel', 'user_id': 1005, 'email': 'gabriel@admin.com',
                                   'name': 'Gabriel', 'is_the_admin': False,
                                   'created_at': '2017-09-20 00:00:00', 'login_date': '2017-09-20T00:00:00',
                                   'is_email_valid': False, 'picture': '', 'social_id': '', 'social_account': ''}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': False,
                                   'username': 'fernanda', 'user_id': 1006, 'email': 'fernanda@admin.com',
                                   'name': None, 'is_the_admin': False,
                                   'created_at': '2017-01-19 00:00:00', 'login_date': '2017-01-19T00:00:00',
                                   'is_email_valid': True, 'picture': '', 'social_id': '', 'social_account': ''}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': False, 'terms_agreed': True,
                                   'username': 'ana', 'user_id': 1007, 'email': 'ana@admin.com',
                                   'name': None, 'is_the_admin': False,
                                   'created_at': '2017-01-18 00:00:00', 'login_date': '2017-01-18T00:00:00',
                                   'is_email_valid': True, 'picture': '', 'social_id': '', 'social_account': ''}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': False, 'terms_agreed': False,
                                   'username': 'bea', 'user_id': 1008, 'email': 'bea@admin.com',
                                   'name': None, 'is_the_admin': False,
                                   'created_at': '2017-01-30 00:00:00', 'login_date': '2017-01-30T00:00:00',
                                   'is_email_valid': False, 'picture': '', 'social_id': '', 'social_account': ''}
                }
            ]
        }

        self.tester.api_user(expected_at_least=expected_at_least)

    def test_get_api_user_return_user_by_user_id(self):
        expected = {
            'features': [
                {'properties': {'name': 'Rodrigo', 'login_date': '2017-03-03T00:00:00', 'terms_agreed': True,
                                'receive_notification_by_email': True, 'user_id': 1002, 'username': 'rodrigo',
                                'is_email_valid': True, 'is_the_admin': True, 'email': 'rodrigo@admin.com',
                                'created_at': '2017-03-03 00:00:00', 'picture': '', 'social_id': '', 'social_account': ''},
                 'type': 'User'}
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_user(expected, user_id="1002")

    def test_get_api_user_return_users_by_name(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': True,
                                   'username': 'miguel', 'user_id': 1003, 'email': 'miguel@admin.com',
                                   'name': 'Miguel', 'is_the_admin': False,
                                   'created_at': '2017-05-08 00:00:00', 'login_date': '2017-05-08T00:00:00',
                                   'is_email_valid': True, 'picture': '', 'social_id': '', 'social_account': ''}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': False,
                                   'username': 'rafael', 'user_id': 1004, 'email': 'rafael@admin.com',
                                   'name': 'Rafael', 'is_the_admin': False,
                                   'created_at': '2017-06-09 00:00:00', 'login_date': '2017-06-09T00:00:00',
                                   'is_email_valid': True, 'picture': '', 'social_id': '', 'social_account': ''}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': False,
                                   'username': 'gabriel', 'user_id': 1005, 'email': 'gabriel@admin.com',
                                   'name': 'Gabriel', 'is_the_admin': False,
                                   'created_at': '2017-09-20 00:00:00', 'login_date': '2017-09-20T00:00:00',
                                   'is_email_valid': False, 'picture': '', 'social_id': '', 'social_account': ''}
                },
            ]
        }

        self.tester.api_user(expected, name="êL")

    def test_get_api_user_return_users_by_email(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': False,
                                   'username': 'rafael', 'user_id': 1004, 'email': 'rafael@admin.com',
                                   'name': 'Rafael', 'is_the_admin': False,
                                   'created_at': '2017-06-09 00:00:00', 'login_date': '2017-06-09T00:00:00',
                                   'is_email_valid': True, 'picture': '', 'social_id': '', 'social_account': ''}
                }
            ]
        }

        self.tester.api_user(expected, email="rafael@admin.com")

    def test_get_api_user_return_users_by_username(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': True,
                                   'username': 'miguel', 'user_id': 1003, 'email': 'miguel@admin.com',
                                   'name': 'Miguel', 'is_the_admin': False,
                                   'created_at': '2017-05-08 00:00:00', 'login_date': '2017-05-08T00:00:00',
                                   'is_email_valid': True, 'picture': '', 'social_id': '', 'social_account': ''}
                }
            ]
        }

        self.tester.api_user(expected, username="miguel")

    def test_get_api_user_return_zero_resources(self):
        expected = {'type': 'FeatureCollection', 'features': []}

        self.tester.api_user(expected, user_id="999")
        self.tester.api_user(expected, user_id="998")

    # user - create, update and delete

    def test_get_api_user_create_update_and_delete(self):
        # create a fake email to avoid the error when exist the same email in DB
        email = generate_random_string() + "@roger.com"

        ##################################################
        # create a user
        ##################################################
        resource = {
            'type': 'User',
            'properties': {'user_id': -1, 'email': email, 'password': 'roger', 'username': 'roger', 'name': 'Roger',
                           'terms_agreed': True, 'receive_notification_by_email': False}
        }
        resource = self.tester.api_user_create(resource)

        ####################################################################################################
        # validate the email
        ####################################################################################################

        user_id = resource["properties"]["user_id"]
        token = generate_encoded_jwt_token({'user_id': user_id})

        # a user is with an invalidated email
        # TODO: temporarily all users will be registered with is_email_valid=True.
        #       after it returns to normal, undo the changes
        # user = self.tester.api_user(user_id=user_id)
        # self.assertEqual(user["features"][0]["properties"]["is_email_valid"], False)

        # so the user validate his/her email
        self.tester.api_validate_email(token)

        # now the user is with the validated email
        user = self.tester.api_user(user_id=user_id)
        self.assertEqual(user["features"][0]["properties"]["is_email_valid"], True)

        ####################################################################################################

        ##################################################
        # login with the created user
        ##################################################
        email = resource["properties"]["email"]
        password = resource["properties"]["password"]
        self.tester.auth_login(email, password)

        ##################################################
        # update the user with himself/herself
        ##################################################
        resource["properties"]["name"] = "Roger Jose"
        resource["properties"]["receive_notification_by_email"] = True
        self.tester.api_user_update(resource)

        ##################################################
        # check if the resource was modified
        ##################################################
        del resource["properties"]["password"]  # remove the password, because it is not needed to compare

        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.tester.api_user(expected_at_least=expected_resource, user_id=resource["properties"]["user_id"])

        # logout with the created user
        self.tester.auth_logout()

        ##################################################
        # log in with a admin user (who can update/delete a user)
        ##################################################
        self.tester.auth_login("admin@admin.com", "admin")

        ##################################################
        # update the user with a admin
        ##################################################
        resource["properties"]["name"] = "Roger"
        resource["properties"]["receive_notification_by_email"] = False
        self.tester.api_user_update(resource)

        ##################################################
        # delete the user with an administrator
        ##################################################
        # get the id of feature to REMOVE it
        resource_id = resource["properties"]["user_id"]

        # remove the created user
        self.tester.api_user_delete(resource_id)

        # check if the user was deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_user(expected, user_id=resource_id)

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

    # user errors - create

    def test_post_api_user_create_error_400_bad_request_attribute_already_exist(self):
        # try to create a resource with email that already exist
        resource = {
            'type': 'User',
            'properties': {'email': "rodrigo@admin.com", 'password': 'roger', 'username': 'roger', 'name': 'Roger',
                           'terms_agreed': True,  'receive_notification_by_email': False}
        }

        self.tester.api_user_error_create_400_bad_request(resource)

        # try to create a resource with username that already exist
        resource = {
            'type': 'User',
            'properties': {'username': 'rodrigo', 'email': "new@email.com", 'password': 'roger', 'name': 'Roger',
                           'terms_agreed': True,  'receive_notification_by_email': False}
        }

        self.tester.api_user_error_create_400_bad_request(resource)

    def test_post_api_user_create_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # try to create a user without username
        resource = {
            'type': 'User',
            'properties': {'email': "new@email.com", 'password': 'roger', 'name': 'Roger',
                           'receive_notification_by_email': False}
        }

        self.tester.api_user_error_create_400_bad_request(resource)

        # try to create a user without username
        resource = {
            'type': 'User',
            'properties': {'username': 'new', 'password': 'roger', 'name': 'Roger',
                           'receive_notification_by_email': False}
        }

        self.tester.api_user_error_create_400_bad_request(resource)

    # user errors - update

    def test_put_api_user_error_400_bad_request_attribute_already_exist(self):
        # login with gabriel
        self.tester.auth_login("admin@admin.com", "admin")

        # try to create a resource with email that already exists
        resource = {
            'type': 'User',
            'properties': {'user_id': 1005, 'email': "admin@admin.com", 'username': 'gabriel', 'name': 'Gabriel',
                           'terms_agreed': True, 'receive_notification_by_email': False}
        }

        self.tester.api_user_update_error_400_bad_request(resource)

        # try to create a resource with username that already exists
        resource = {
            'type': 'User',
            'properties': {'user_id': 1005, 'username': 'admin', 'email': "gabriel@admin.com", 'name': 'Gabriel',
                           'terms_agreed': True, 'receive_notification_by_email': False}
        }

        self.tester.api_user_update_error_400_bad_request(resource)

        # logout
        self.tester.auth_logout()

    def test_put_api_user_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # login with gabriel
        self.tester.auth_login("admin@admin.com", "admin")

        # try to update a user without user_id
        resource = {
            'type': 'User',
            'properties': {'email': "gabriel@admin.com", 'name': 'Gabriel',
                           'receive_notification_by_email': False}
        }

        self.tester.api_user_update_error_400_bad_request(resource)

        # try to update a user without username
        resource = {
            'type': 'User',
            'properties': {'user_id': 1005, 'email': "gabriel@admin.com", 'name': 'Gabriel',
                           'receive_notification_by_email': False}
        }

        self.tester.api_user_update_error_400_bad_request(resource)

        # try to update a user without email
        resource = {
            'type': 'User',
            'properties': {'user_id': 1005, 'username': 'gabriel', 'name': 'Gabriel',
                           'receive_notification_by_email': False}
        }

        self.tester.api_user_update_error_400_bad_request(resource)

        # logout
        self.tester.auth_logout()

    def test_put_api_user_error_401_unauthorized(self):
        # update a user
        resource = {
            'type': 'User',
            'properties': {'email': "gabriel@admin.com", 'name': 'Gabriel', 'receive_notification_by_email': False}
        }

        self.tester.api_user_update_error_401_unauthorized(resource)

    def test_put_api_user_error_403_forbidden(self):
        # login with gabriel
        self.tester.auth_login("rafael@admin.com", "rafael")

        # try to create a resource with email that already exist
        resource = {
            'type': 'User',
            'properties': {'user_id': 1005, 'email': "admin@admin.com", 'username': 'gabriel', 'name': 'Gabriel',
                           'terms_agreed': True, 'receive_notification_by_email': False}
        }

        self.tester.api_user_update_error_403_forbidden(resource)

        # logout
        self.tester.auth_logout()

    def test_put_api_user_error_404_not_found(self):
        # login with gabriel
        self.tester.auth_login("admin@admin.com", "admin")

        # try to create a resource with email that already exist
        resource = {
            'type': 'User',
            'properties': {'user_id': 999, 'email': "admin@admin.com", 'username': 'gabriel', 'name': 'Gabriel',
                           'terms_agreed': True, 'receive_notification_by_email': False}
        }

        self.tester.api_user_update_error_404_not_found(resource)

        # logout
        self.tester.auth_logout()

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

    def test_delete_api_user_error_401_unauthorized_user_without_login(self):
        self.tester.api_user_delete_error_401_unauthorized("abc")
        self.tester.api_user_delete_error_401_unauthorized(0)
        self.tester.api_user_delete_error_401_unauthorized(-1)
        self.tester.api_user_delete_error_401_unauthorized("-1")
        self.tester.api_user_delete_error_401_unauthorized("0")
        self.tester.api_user_delete_error_401_unauthorized("1001")

    def test_delete_api_user_error_403_forbidden_user_cannot_delete_other_user(self):
        self.tester.auth_login("miguel@admin.com", "miguel")

        # try to remove the user created, but get a 403, because just admin can delete users
        self.tester.api_user_delete_error_403_forbidden(1001)

        # logout
        self.tester.auth_logout()

    def test_delete_api_user_error_404_not_found(self):
        # DO LOGIN
        self.tester.auth_login("admin@admin.com", "admin")

        self.tester.api_user_delete_error_404_not_found("5000")
        self.tester.api_user_delete_error_404_not_found("5001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
