#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


class TestAPIProject(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # project - get

    def test_get_api_project_return_all_projects(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Project',
                    'properties': {'fk_user_id': 1001, 'created_at': '2017-11-20 00:00:00',
                                   'id': 1001, 'removed_at': None, 'fk_group_id': 1001},
                    'tags': {'description': 'default project', 'name': 'admin'}
                },
                {
                    'type': 'Project',
                    'properties': {'fk_user_id': 1002, 'created_at': '2017-10-12 00:00:00',
                                   'id': 1002, 'removed_at': None, 'fk_group_id': 1001},
                    'tags': {'name': 'test project', 'url': 'http://somehost.com'}
                },
                {
                    'type': 'Project',
                    'properties': {'fk_user_id': 1002, 'created_at': '2017-12-23 00:00:00',
                                   'id': 1003, 'removed_at': None, 'fk_group_id': 1002},
                    'tags': {'name': 'hello world'}
                },
                {
                    'type': 'Project',
                    'properties': {'fk_user_id': 1004, 'created_at': '2017-09-11 00:00:00',
                                   'id': 1004, 'removed_at': None, 'fk_group_id': 1002},
                    'tags': None
                }
            ]
        }

        self.tester.api_project(expected)

    def test_get_api_project_return_project_by_project_id(self):
        expected = {
            'features': [
                {
                    'type': 'Project',
                    'properties': {'fk_user_id': 1001, 'created_at': '2017-11-20 00:00:00',
                                   'id': 1001, 'removed_at': None, 'fk_group_id': 1001},
                    'tags': {'description': 'default project', 'name': 'admin'}
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_project(expected, project_id="1001")

    def test_get_api_project_return_project_by_group_id(self):
        expected = {
            'features': [
                {
                    'type': 'Project',
                    'properties': {'fk_user_id': 1002, 'created_at': '2017-12-23 00:00:00',
                                   'id': 1003, 'removed_at': None, 'fk_group_id': 1002},
                    'tags': {'name': 'hello world'}
                },
                {
                    'type': 'Project',
                    'properties': {'fk_user_id': 1004, 'created_at': '2017-09-11 00:00:00',
                                   'id': 1004, 'removed_at': None, 'fk_group_id': 1002},
                    'tags': None
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_project(expected, group_id="1002")

    def test_get_api_project_return_project_by_user_id(self):
        expected = {
            'features': [
                {
                    'type': 'Project',
                    'properties': {'fk_user_id': 1002, 'created_at': '2017-10-12 00:00:00',
                                   'id': 1002, 'removed_at': None, 'fk_group_id': 1001},
                    'tags': {'name': 'test project', 'url': 'http://somehost.com'}
                },
                {
                    'type': 'Project',
                    'properties': {'fk_user_id': 1002, 'created_at': '2017-12-23 00:00:00',
                                   'id': 1003, 'removed_at': None, 'fk_group_id': 1002},
                    'tags': {'name': 'hello world'}
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_project(expected, user_id="1002")

    # project - create and delete

    def test_get_api_project_create_and_delete(self):
        # DO LOGIN
        self.tester.auth_login_fake()

        # create a project
        feature = {
            'type': 'Project',
            'properties': {'id': -1, 'fk_group_id': 1001},
            'tags': {'name': 'test project', 'url': 'http://somehost.com'}
        }

        feature = self.tester.api_project_create(feature)

        # get the id of feature to REMOVE it
        feature_id = feature["properties"]["id"]

        # REMOVE THE project AFTER THE TESTS
        self.tester.api_project_delete(feature_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPIProjectErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # project errors - get

    def test_get_api_project_error_400_bad_request(self):
        self.tester.api_project_error_400_bad_request(project_id="abc")
        self.tester.api_project_error_400_bad_request(project_id=0)
        self.tester.api_project_error_400_bad_request(project_id=-1)
        self.tester.api_project_error_400_bad_request(project_id="-1")
        self.tester.api_project_error_400_bad_request(project_id="0")

    def test_get_api_project_error_404_not_found(self):
        self.tester.api_project_error_404_not_found(project_id="999")
        self.tester.api_project_error_404_not_found(project_id="998")

    # project errors - create

    def test_put_api_project_create_error_403_forbidden(self):
        feature = {
            'type': 'Project',
            'properties': {'id': -1, 'fk_group_id': 1001},
            'tags': [{'name': 'test project'},
                     {'url': 'http://somehost.com'}]
        }
        self.tester.api_project_create_error_403_forbidden(feature)

    # project errors - delete

    def test_delete_api_project_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login_fake()

        self.tester.api_project_delete_error_400_bad_request("abc")
        self.tester.api_project_delete_error_400_bad_request(0)
        self.tester.api_project_delete_error_400_bad_request(-1)
        self.tester.api_project_delete_error_400_bad_request("-1")
        self.tester.api_project_delete_error_400_bad_request("0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_project_error_403_forbidden(self):
        self.tester.api_project_delete_error_403_forbidden("abc")
        self.tester.api_project_delete_error_403_forbidden(0)
        self.tester.api_project_delete_error_403_forbidden(-1)
        self.tester.api_project_delete_error_403_forbidden("-1")
        self.tester.api_project_delete_error_403_forbidden("0")
        self.tester.api_project_delete_error_403_forbidden("1001")

    def test_delete_api_project_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login_fake()

        self.tester.api_project_delete_error_404_not_found("5000")
        self.tester.api_project_delete_error_404_not_found("5001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
