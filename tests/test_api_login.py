#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase, skip
from util.tester import UtilTester

"""

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

    def test_get_api_auth_login_gabriel(self):
        self.tester.auth_login("gabriel@admin.com", "gabriel")
        self.tester.auth_logout()


@skip(">>>")
class TestAPIAuthLoginErrors(TestCase):

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

"""

# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
