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


class TestAPIAuthLoginError(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_get_api_auth_login_409_conflict(self):
        self.tester.auth_login_409_conflict("gabriel@admin.com", "gabriel")


class TestAPIAuthChangePassword(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_post_change_the_password(self):
        self.tester.auth_login("ana@admin.com", "ana")

        resource = {
            'properties': {'current_password': 'ana', 'new_password': 'anabbb'},
            'type': 'ChangePassword'
        }
        self.tester.api_change_password(resource)

        self.tester.auth_logout()

        # try to login with the new password
        self.tester.auth_login("ana@admin.com", "anabbb")

        resource = {
            'properties': {'current_password': 'anabbb', 'new_password': 'ana'},
            'type': 'ChangePassword'
        }
        self.tester.api_change_password(resource)

        self.tester.auth_logout()


class TestAPIAuthChangePasswordErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_post_api_change_password_error_400_bad_request_attribute_in_JSON_is_missing(self):
        self.tester.auth_login("ana@admin.com", "ana")

        resource = {
            'properties': {'new_password': 'anabbb'},
            'type': 'ChangePassword'
        }
        self.tester.api_change_password_error_400_bad_request(resource)

        resource = {
            'properties': {'current_password': 'ana'},
            'type': 'ChangePassword'
        }
        self.tester.api_change_password_error_400_bad_request(resource)

        self.tester.auth_logout()

    def test_post_api_change_password_error_401_unauthorized(self):
        resource = {
            'properties': {'current_password': 'ana', 'new_password': 'anabbb'},
            'type': 'ChangePassword'
        }
        self.tester.api_change_password_error_401_unauthorized(resource)

    # def test_post_api_change_password_error_409_conflict_email_is_not_validated(self):
    #     # the 409 is raised when try to log in the system
    #     self.tester.auth_login("gabriel@admin.com", "gabriel")
    #
    #     resource = {
    #         'properties': {'current_password': 'gabriel', 'new_password': 'joao'},
    #         'type': 'ChangePassword'
    #     }
    #     self.tester.api_change_password_error_409_conflict(resource)
    #
    #     self.tester.auth_logout()

    def test_post_api_change_password_error_409_conflict_current_password_is_invalid(self):
        self.tester.auth_login("miguel@admin.com", "miguel")

        resource = {
            'properties': {'current_password': 'senha_errada', 'new_password': 'joao'},
            'type': 'ChangePassword'
        }
        self.tester.api_change_password_error_409_conflict(resource)

        self.tester.auth_logout()


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
