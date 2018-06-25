#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


class TestAPICurrentUser(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_api_user_by_token_with_login(self):
        # DO LOGIN BEFORE THE TEST
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # do not put the "login_date" and "created_at" attributes, because they are created dynamically
        expected_at_least = {
            'properties': {
                'username': 'rodrigo', 'is_the_admin': True, 'user_id': 1002,
                'email': 'rodrigo@admin.com', 'terms_agreed': True, 'name': 'Rodrigo',
                'is_email_valid': True, 'receive_notification_by_email': False
            },
            'type': 'User'
        }

        self.tester.api_user_by_token(expected_at_least)

        # DO LOGOUT AFTER THE TEST
        self.tester.auth_logout()


class TestAPIValidateEmail(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_api_validate_email(self):
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMDA1fQ.XbibygDhgaF0x3w50wI8UWfK8u1I2vrMlfPBa5y-Z4o'
        user_id = 1005

        # a user is with a invalidated email
        user = self.tester.api_user_get(user_id=user_id)
        self.assertEqual(user["features"][0]["properties"]["is_email_valid"], False)

        # so the user validate his/her email
        self.tester.api_validate_email(token)

        # now the user is with the validated email
        user = self.tester.api_user_get(user_id=user_id)
        self.assertEqual(user["features"][0]["properties"]["is_email_valid"], True)

        # change the is_email_valid to False again, for not break the tests
        self.tester.api_is_email_valid(user_id=user_id, is_email_valid=False)

        user = self.tester.api_user_get(user_id=user_id)
        self.assertEqual(user["features"][0]["properties"]["is_email_valid"], False)

    def test_api_validate_email_400_bad_request(self):
        # try to validate the email
        self.tester.api_validate_email_400_bad_request('eyJhbGciOiJIVCJ9.eyJ1c2VyMDAzfQ.IsLw6ZQh-UoPWEKc8Cj5q8')

        # try to validate the email
        self.tester.api_validate_email_400_bad_request('eyJhbGciOiJIVCJ91c2VyMDAzfQ.IsLw6ZQh-UoPWEKc8Cj5q8')

        # try to validate the email
        self.tester.api_validate_email_400_bad_request('eyJhbGciOiJIc2VyMDAzw6ZQh-UoPWEKc8Cj5q8')


"""
class TestAPICapabilities(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_api_capabilities(self):
        expected = {
            "version": "0.0.4",
            "status": {"postgresql": "online"}
        }

        self.tester.api_capabilities(expected)


class TestAPICurrentUserError(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_api_user_by_token_invalid_token(self):
        # do not put the "login_date" and "created_at" attributes, because they are created dynamically
        invalid_authorization = "29uj29uç0suk2"

        self.tester.api_user_by_token_400_bad_request(invalid_authorization)

    def test_api_user_by_token_without_login(self):
        self.tester.api_user_by_token_401_unauthorized()
"""

# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
