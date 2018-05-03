#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase, skip
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


class TestAPISessionUser(TestCase):
    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_api_session_user_with_login(self):
        # do not put the "id" and "created_at" attributes, because they are created dynamically
        expected_at_least = {
            'user': {
                'properties': {'username': 'test', 'terms_agreed': False, 'is_email_valid': False,
                               'email': 'test@fake.login'},
                # 'tags': {'type_login': 'fakelogin'},
                'type': 'User'
            }
        }

        # DO LOGIN BEFORE THE TEST
        self.tester.auth_login_fake()

        self.tester.api_session_user(expected_at_least)

        # DO LOGOUT AFTER THE TEST
        self.tester.auth_logout()

    def test_api_session_user_without_login(self):
        self.tester.api_session_user_error_404_not_found()
"""

# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
