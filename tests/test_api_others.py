#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


class TestAPICapabilities(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_api_capabilities(self):
        expected = {
            "version": "0.0.2",
            "status": {"postgresql": "online", "neo4j": "online"}
        }

        self.tester.api_capabilities(expected)


class TestAPISessionUser(TestCase):
    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_api_session_user_with_login(self):
        expected = {
            'login': {
                'user': {'username': None, 'email': 'test@fake.login', 'id': 1},
                'type_login': 'fakelogin'
            }
        }

        # DO LOGIN BEFORE THE TEST
        self.tester.auth_login()

        self.tester.api_session_user(expected)

        # DO LOGOUT AFTER THE TEST
        self.tester.auth_logout()

    def test_api_session_user_without_login(self):
        self.tester.api_session_user_error_404_not_found()


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
