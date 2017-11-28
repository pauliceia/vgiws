#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/

class TestAPIProject(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # project - get

    def test_get_api_project_return_all_projects(self):
        expected = {
            'features': [
                {
                    'properties': {'removed_at': None, 'create_at': '2017-11-20 00:00:00', 'fk_user_id_owner': 1001, 'id': 1001},
                    'tags': [{'k': 'name', 'v': 'default'}, {'k': 'description', 'v': 'default project'}],
                    'type': 'Project'
                },
                {
                    'properties': {'removed_at': None, 'create_at': '2017-10-12 00:00:00', 'fk_user_id_owner': 1002, 'id': 1002},
                    'tags': [{'k': 'name', 'v': 'test_project'}, {'k': 'description', 'v': 'test_project'}],
                    'type': 'Project'
                },
                {
                    'properties': {'removed_at': None, 'create_at': '2017-12-23 00:00:00', 'fk_user_id_owner': 1002, 'id': 1003},
                    'tags': [{'k': 'name', 'v': 'project 3'}, {'k': 'description', 'v': 'test_project'}],
                    'type': 'Project'
                },
                {
                    'properties': {'removed_at': None, 'create_at': '2017-09-11 00:00:00', 'fk_user_id_owner': 1003, 'id': 1004},
                    'tags': [{'k': 'name', 'v': 'project 4'}, {'k': 'description', 'v': 'test_project'}],
                    'type': 'Project'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_project(expected)

    def test_get_api_project_return_project_by_project_id(self):
        expected = {
            'features': [
                {
                    'type': 'Project',
                    'tags': [{'k': 'name', 'v': 'default'},
                             {'k': 'description', 'v': 'default project'}],
                    'properties': {'removed_at': None, 'fk_user_id_owner': 1001,
                                   'id': 1001, 'create_at': '2017-11-20 00:00:00'}
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_project(expected, project_id="1001")

    def test_get_api_project_return_project_by_user_id(self):
        expected = {
            'features': [
                {
                    'properties': {'removed_at': None, 'create_at': '2017-10-12 00:00:00',
                                   'fk_user_id_owner': 1002,'id': 1002},
                    'tags': [{'k': 'name', 'v': 'test_project'},
                             {'k': 'description', 'v': 'test_project'}],
                    'type': 'Project'
                },
                {
                    'properties': {'removed_at': None, 'create_at': '2017-12-23 00:00:00',
                                   'fk_user_id_owner': 1002, 'id': 1003},
                    'tags': [{'k': 'name', 'v': 'project 3'},
                             {'k': 'description', 'v': 'test_project'}],
                    'type': 'Project'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_project(expected, user_id="1002")

    # project - create and delete

    def test_get_api_project_create_and_delete(self):
        # DO LOGIN
        self.tester.auth_login()

        # create a project
        project = {
            'project': {
                'tags': [{'k': 'created_by', 'v': 'test_api'},
                         {'k': 'name', 'v': 'project of data'},
                         {'k': 'description', 'v': 'description of the project'}],
                'properties': {'id': -1}
            }
        }
        self.project = self.tester.api_project_create(project)

        # get the id of project to REMOVE it
        project_id = self.project["project"]["properties"]["id"]

        # REMOVE THE PROJECT AFTER THE TESTS
        self.tester.api_project_delete(project_id)

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
        project = {
            'project': {
                'tags': [{'k': 'created_by', 'v': 'test_api'},
                         {'k': 'name', 'v': 'project of data'},
                         {'k': 'description', 'v': 'description of the project'}],
                'properties': {'id': -1}
            }
        }
        self.tester.api_project_create_error_403_forbidden(project)

    # project errors - delete

    def test_delete_api_project_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login()

        self.tester.api_project_delete_error_400_bad_request(project_id="abc")
        self.tester.api_project_delete_error_400_bad_request(project_id=0)
        self.tester.api_project_delete_error_400_bad_request(project_id=-1)
        self.tester.api_project_delete_error_400_bad_request(project_id="-1")
        self.tester.api_project_delete_error_400_bad_request(project_id="0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_project_error_403_forbidden(self):
        self.tester.api_project_delete_error_403_forbidden(project_id="abc")
        self.tester.api_project_delete_error_403_forbidden(project_id=0)
        self.tester.api_project_delete_error_403_forbidden(project_id=-1)
        self.tester.api_project_delete_error_403_forbidden(project_id="-1")
        self.tester.api_project_delete_error_403_forbidden(project_id="0")
        self.tester.api_project_delete_error_403_forbidden(project_id="1001")

    def test_delete_api_project_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login()

        self.tester.api_project_delete_error_404_not_found(project_id="5000")
        self.tester.api_project_delete_error_404_not_found(project_id="5001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
