#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util.tester import RequestTester, get_string_in_hash_sha512


class TestAPIAuthLogin(RequestTester):

    def test__get_api_auth_login__user_admin(self):
        self.auth_login("admin@admin.com", "admin")
        self.auth_logout()

    def test__get_api_auth_login__user_rodrigo(self):
        self.auth_login("rodrigo@admin.com", "rodrigo")
        self.auth_logout()

    def test__get_api_auth_login__user_miguel(self):
        self.auth_login("miguel@admin.com", "miguel")
        self.auth_logout()

    def test__get_api_auth_login__user_rafael(self):
        self.auth_login("rafael@admin.com", "rafael")
        self.auth_logout()


class TestAPIAuthLoginError(RequestTester):

    def test__get_api_auth_login__409_conflict__the_email_was_not_validated(self):
        self.auth_login("gabriel@admin.com", "gabriel",
                   status_code=409, text_message="The email has not been validated.")


class TestAPIAuthChangePassword(RequestTester):

    def setUp(self):
        self.set_urn('/api/auth/change_password')

    def test__post_api_auth_change_password(self):
        self.auth_login("ana@admin.com", "ana")

        # update the passaword
        resource = {
            'properties': {
                'current_password': get_string_in_hash_sha512('ana'),
                'new_password': get_string_in_hash_sha512('anabbb')
            },
            'type': 'ChangePassword'
        }
        self.put(resource)

        self.auth_logout()

        # try to login with the new password
        self.auth_login("ana@admin.com", "anabbb")

        # update the password again with the previous version
        resource = {
            'properties': {
                'current_password': get_string_in_hash_sha512('anabbb'),
                'new_password': get_string_in_hash_sha512('ana')
            },
            'type': 'ChangePassword'
        }
        self.put(resource)

        self.auth_logout()


class TestAPIAuthChangePasswordErrors(RequestTester):

    def setUp(self):
        self.set_urn('/api/auth/change_password')

    def test__post_api_auth_change_password__400_bad_request__attribute_in_JSON_is_missing(self):
        self.auth_login("ana@admin.com", "ana")

        resource = {
            'properties': {'new_password': 'anabbb'},
            'type': 'ChangePassword'
        }
        self.put(resource, status_code=400,
                 text_message="It is needed to pass the encrypted current_password and new_password.")

        resource = {
            'properties': {'current_password': 'ana'},
            'type': 'ChangePassword'
        }
        self.put(resource, status_code=400,
                 text_message="It is needed to pass the encrypted current_password and new_password.")

        self.auth_logout()

    def test__post_api_auth_change_password__401_unauthorized(self):
        resource = {
            'properties': {'current_password': 'ana', 'new_password': 'anabbb'},
            'type': 'ChangePassword'
        }

        self.put(resource, status_code=401,
                 text_message="A valid `Authorization` header is necessary!")

    # def test_post_api_change_password_error_409_conflict_email_is_not_validated(self):
    #     # the 409 is raised when try to log in the system
    #     self.auth_login("gabriel@admin.com", "gabriel")
    #
    #     resource = {
    #         'properties': {'current_password': 'gabriel', 'new_password': 'joao'},
    #         'type': 'ChangePassword'
    #     }
    #     self.api_change_password_error_409_conflict(resource)
    #
    #     self.auth_logout()

    def test__post_api_auth_change_password__409_conflict__current_password_is_invalid(self):
        self.auth_login("miguel@admin.com", "miguel")

        resource = {
            'properties': {'current_password': 'senha_errada', 'new_password': 'joao'},
            'type': 'ChangePassword'
        }

        self.put(resource, status_code=409, text_message="Current password is invalid.")

        self.auth_logout()


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
