#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester

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
"""


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


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
