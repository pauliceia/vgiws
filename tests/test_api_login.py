#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


class TestAPIAuthLogin(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_get_api_auth_login_admin(self):
        self.tester.auth_login("admin@admin.com", "admin")
        self.tester.auth_logout()

    def test_get_api_auth_login_rodrigo(self):
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")
        self.tester.auth_logout()

    def test_get_api_auth_login_miguel(self):
        self.tester.auth_login("miguel@admin.com", "miguel")
        self.tester.auth_logout()

    def test_get_api_auth_login_rafael(self):
        self.tester.auth_login("rafael@admin.com", "rafael")
        self.tester.auth_logout()

"""
class TestAPIAuthLoginError(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_get_api_auth_login_409_conflict(self):
        self.tester.auth_login_409_conflict("gabriel@admin.com", "gabriel")
"""

# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
