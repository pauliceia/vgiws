#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase, skip
from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/

class TestAPIChangeset(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # changeset - create and delete

    def test_get_api_changeset_create_and_delete(self):
        # DO LOGIN
        self.tester.auth_login()

        changeset = {
            'changeset': {
                'tags': [{'k': 'created_by', 'v': 'test_api'},
                         {'k': 'comment', 'v': 'testing create changeset'}],
                'properties': {'id': -1, "fk_project_id": 1001}
            }
        }
        changeset = self.tester.api_changeset_create(changeset)

        # get the id of changeset to CLOSE the changeset
        changeset_id = changeset["changeset"]["properties"]["id"]

        # CLOSE THE CHANGESET
        self.tester.api_changeset_close(changeset_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPIChangesetErrors(TestCase):
    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # changeset errors - create

    def test_put_api_changeset_create_error_403_forbidden(self):
        changeset = {
            'changeset': {
                'tags': [{'k': 'created_by', 'v': 'test_api'},
                         {'k': 'comment', 'v': 'testing create changeset'}],
                'properties': {'id': -1, "fk_project_id": 1001}
            }
        }
        self.tester.api_changeset_create_error_403_forbidden(changeset)

    # changeset errors - close

    def test_put_api_changeset_close_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login()

        self.tester.api_changeset_close_error_400_bad_request(changeset_id="abc")
        self.tester.api_changeset_close_error_400_bad_request(changeset_id=0)
        self.tester.api_changeset_close_error_400_bad_request(changeset_id=-1)
        self.tester.api_changeset_close_error_400_bad_request(changeset_id="-1")
        self.tester.api_changeset_close_error_400_bad_request(changeset_id="0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_changeset_close_error_403_forbidden(self):
        self.tester.api_changeset_close_error_403_forbidden(changeset_id="abc")
        self.tester.api_changeset_close_error_403_forbidden(changeset_id=0)
        self.tester.api_changeset_close_error_403_forbidden(changeset_id=-1)
        self.tester.api_changeset_close_error_403_forbidden(changeset_id="-1")
        self.tester.api_changeset_close_error_403_forbidden(changeset_id="0")
        self.tester.api_changeset_close_error_403_forbidden(changeset_id="1001")

    def test_put_api_changeset_close_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login()

        self.tester.api_changeset_close_error_404_not_found(changeset_id="5000")
        self.tester.api_changeset_close_error_404_not_found(changeset_id="5001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
