#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
from unittest import TestCase
from util.tester import UtilTester


class TestAPINotification(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # notification - get

    def test_get_api_notification_return_all_notifications(self):
        expected = {
            'features': [
                {
                    'properties': {'is_read': False, 'removed_at': None, 'visible': True, 'id': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'fk_user_id': 1001},
                    'type': 'Notification',
                    'tags': {'body': 'Happy Birthday', 'type': 'birthday', 'url': ''}
                },
                {
                    'properties': {'is_read': False, 'removed_at': None, 'visible': True, 'id': 1002,
                                   'created_at': '2017-03-25 00:00:00', 'fk_user_id': 1001},
                    'type': 'Notification',
                    'tags': {'body': 'You was added in a group called X', 'type': 'group', 'url': ''}
                },
                {
                    'properties': {'is_read': True, 'removed_at': None, 'visible': True, 'id': 1003,
                                   'created_at': '2017-12-25 00:00:00', 'fk_user_id': 1001},
                    'type': 'Notification',
                    'tags': {'body': 'Created a new project in group X', 'type': 'project', 'url': ''}
                },
                {
                    'properties': {'is_read': False, 'removed_at': None, 'visible': True, 'id': 1004,
                                   'created_at': '2017-05-13 00:00:00', 'fk_user_id': 1002},
                    'type': 'Notification',
                    'tags': {'body': 'Created a new layer in project Y', 'type': 'layer', 'url': ''}
                },
                {
                    'properties': {'is_read': False, 'removed_at': None, 'visible': True, 'id': 1005,
                                   'created_at': '2017-12-25 00:00:00', 'fk_user_id': 1002},
                    'type': 'Notification',
                    'tags': {'body': 'A new review was made in layer Z', 'type': 'review', 'url': ''}
                },
                {
                    'properties': {'is_read': False, 'removed_at': None, 'visible': True, 'id': 1006,
                                   'created_at': '2017-05-13 00:00:00', 'fk_user_id': 1003},
                    'type': 'Notification',
                    'tags': {'body': 'You gained a new trophy', 'type': 'award', 'url': ''}
                },
                {
                    'properties': {'is_read': False, 'removed_at': None, 'visible': True, 'id': 1008,
                                   'created_at': '2017-12-25 00:00:00', 'fk_user_id': 1004},
                    'type': 'Notification',
                    'tags': {'body': 'You gained more points', 'type': 'point', 'url': ''}
                },
                {
                    'properties': {'is_read': True, 'removed_at': None, 'visible': True, 'id': 1010,
                                   'created_at': '2017-05-13 00:00:00', 'fk_user_id': 1005},
                    'type': 'Notification',
                    'tags': {'body': 'You gained more points', 'type': 'point', 'url': ''}
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_notification(expected)

    def test_get_api_notification_return_notification_by_notification_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'is_read': False, 'removed_at': None, 'visible': True, 'id': 1002,
                                   'created_at': '2017-03-25 00:00:00', 'fk_user_id': 1001},
                    'type': 'Notification',
                    'tags': {'body': 'You was added in a group called X', 'type': 'group', 'url': ''}
                }
            ],
        }

        self.tester.api_notification(expected, notification_id="1002")

    def test_get_api_notification_return_notification_by_user_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'is_read': False, 'removed_at': None, 'visible': True, 'id': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'fk_user_id': 1001},
                    'type': 'Notification',
                    'tags': {'body': 'Happy Birthday', 'type': 'birthday', 'url': ''}
                },
                {
                    'properties': {'is_read': False, 'removed_at': None, 'visible': True, 'id': 1002,
                                   'created_at': '2017-03-25 00:00:00', 'fk_user_id': 1001},
                    'type': 'Notification',
                    'tags': {'body': 'You was added in a group called X', 'type': 'group', 'url': ''}
                },
                {
                    'properties': {'is_read': True, 'removed_at': None, 'visible': True, 'id': 1003,
                                   'created_at': '2017-12-25 00:00:00', 'fk_user_id': 1001},
                    'type': 'Notification',
                    'tags': {'body': 'Created a new project in group X', 'type': 'project', 'url': ''}
                }
            ],
        }

        self.tester.api_notification(expected, user_id="1001")

    def test_get_api_notification_return_notification_by_is_read_true(self):
        expected = {
            'features': [
                {
                    'properties': {'is_read': True, 'removed_at': None, 'visible': True, 'id': 1003,
                                   'created_at': '2017-12-25 00:00:00', 'fk_user_id': 1001},
                    'type': 'Notification',
                    'tags': {'body': 'Created a new project in group X', 'type': 'project', 'url': ''}
                },
                {
                    'properties': {'is_read': True, 'removed_at': None, 'visible': True, 'id': 1010,
                                   'created_at': '2017-05-13 00:00:00', 'fk_user_id': 1005},
                    'type': 'Notification',
                    'tags': {'body': 'You gained more points', 'type': 'point', 'url': ''}
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_notification(expected, is_read=True)

    def test_get_api_notification_return_notification_by_is_read_false(self):
        expected = {
            'features': [
                {
                    'properties': {'is_read': False, 'removed_at': None, 'visible': True, 'id': 1001,
                                   'created_at': '2017-01-01 00:00:00', 'fk_user_id': 1001},
                    'type': 'Notification',
                    'tags': {'body': 'Happy Birthday', 'type': 'birthday', 'url': ''}
                },
                {
                    'properties': {'is_read': False, 'removed_at': None, 'visible': True, 'id': 1002,
                                   'created_at': '2017-03-25 00:00:00', 'fk_user_id': 1001},
                    'type': 'Notification',
                    'tags': {'body': 'You was added in a group called X', 'type': 'group', 'url': ''}
                },
                {
                    'properties': {'is_read': False, 'removed_at': None, 'visible': True, 'id': 1004,
                                   'created_at': '2017-05-13 00:00:00', 'fk_user_id': 1002},
                    'type': 'Notification',
                    'tags': {'body': 'Created a new layer in project Y', 'type': 'layer', 'url': ''}
                },
                {
                    'properties': {'is_read': False, 'removed_at': None, 'visible': True, 'id': 1005,
                                   'created_at': '2017-12-25 00:00:00', 'fk_user_id': 1002},
                    'type': 'Notification',
                    'tags': {'body': 'A new review was made in layer Z', 'type': 'review', 'url': ''}
                },
                {
                    'properties': {'is_read': False, 'removed_at': None, 'visible': True, 'id': 1006,
                                   'created_at': '2017-05-13 00:00:00', 'fk_user_id': 1003},
                    'type': 'Notification',
                    'tags': {'body': 'You gained a new trophy', 'type': 'award', 'url': ''}
                },
                {
                    'properties': {'is_read': False, 'removed_at': None, 'visible': True, 'id': 1008,
                                   'created_at': '2017-12-25 00:00:00', 'fk_user_id': 1004},
                    'type': 'Notification',
                    'tags': {'body': 'You gained more points', 'type': 'point', 'url': ''}
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_notification(expected, is_read=False)

    def test_get_api_notification_return_notification_by_user_id_and_is_read_true(self):
        expected = {
            'features': [
                {
                    'properties': {'is_read': True, 'removed_at': None, 'visible': True, 'id': 1003,
                                   'created_at': '2017-12-25 00:00:00', 'fk_user_id': 1001},
                    'type': 'Notification',
                    'tags': {'body': 'Created a new project in group X', 'type': 'project', 'url': ''}
                },
            ],
            'type': 'FeatureCollection'
        }

        # e2 = {
        #     'features': [
        #         {
        #             'properties': {'removed_at': None, 'visible': True, 'created_at': '2017-01-01 00:00:00',
        #                            'id': 1001, 'is_read': False, 'fk_user_id': 1001},
        #             'tags': [{'body': 'Happy Birthday'},
        #                      {'type': 'birthday'},
        #                      {'url': ''}],
        #             'type': 'Notification'
        #         },
        #         {'properties': {'removed_at': None, 'visible': True, 'created_at': '2017-03-25 00:00:00',
        #                         'id': 1002, 'is_read': False, 'fk_user_id': 1001},
        #          'tags': [{'body': 'You was added in a group called X'},
        #                   {'type': 'group'},
        #                   {'url': ''}], 'type': 'Notification'
        #          },
        #         {'properties': {'removed_at': None, 'visible': True, 'created_at': '2017-12-25 00:00:00', 'id': 1003, 'is_read': True, 'fk_user_id': 1001}, 'tags': [{'body': 'Created a new project in group X'}, {'type': 'project'}, {'url': ''}], 'type': 'Notification'}], 'type': 'FeatureCollection'}

        self.tester.api_notification(expected, user_id="1001", is_read=True)

    def test_get_api_notification_return_notification_by_user_id_and_is_read_false(self):
        expected = {
            'features': [
                {
                    'properties': {'is_read': False, 'removed_at': None, 'visible': True, 'id': 1004,
                                   'created_at': '2017-05-13 00:00:00', 'fk_user_id': 1002},
                    'type': 'Notification',
                    'tags': {'body': 'Created a new layer in project Y', 'type': 'layer', 'url': ''}
                },
                {
                    'properties': {'is_read': False, 'removed_at': None, 'visible': True, 'id': 1005,
                                   'created_at': '2017-12-25 00:00:00', 'fk_user_id': 1002},
                    'type': 'Notification',
                    'tags': {'body': 'A new review was made in layer Z', 'type': 'review', 'url': ''}
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_notification(expected, user_id="1002", is_read=False)

    # notification - create and delete

    def test_get_api_notification_create_and_delete(self):
        # DO LOGIN
        self.tester.auth_login_fake()

        # create a notification
        feature = {
            'properties': {'id': -1, 'fk_user_id': 1002},
            'type': 'Notification',
            'tags': {'body': 'You gained more points', 'type': 'point', 'url': ''}
        }

        feature = self.tester.api_notification_create(feature)

        # get the id of feature to REMOVE it
        feature_id = feature["properties"]["id"]

        # REMOVE THE notification AFTER THE TESTS
        self.tester.api_notification_delete(feature_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPINotificationErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # notification errors - get

    def test_get_api_notification_error_400_bad_request(self):
        self.tester.api_notification_error_400_bad_request(notification_id="abc")
        self.tester.api_notification_error_400_bad_request(notification_id=0)
        self.tester.api_notification_error_400_bad_request(notification_id=-1)
        self.tester.api_notification_error_400_bad_request(notification_id="-1")
        self.tester.api_notification_error_400_bad_request(notification_id="0")

    def test_get_api_notification_error_404_not_found(self):
        self.tester.api_notification_error_404_not_found(notification_id="999")
        self.tester.api_notification_error_404_not_found(notification_id="998")

    # notification errors - create

    def test_put_api_notification_create_error_403_forbidden(self):
        feature = {
            'properties': {'id': -1, 'fk_user_id': 1003},
            'type': 'Notification',
            'tags': {'body': 'You gained more points', 'type': 'point', 'url': ''}
        }

        self.tester.api_notification_create_error_403_forbidden(feature)

    # notification errors - delete

    def test_delete_api_notification_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login_fake()

        self.tester.api_notification_delete_error_400_bad_request("abc")
        self.tester.api_notification_delete_error_400_bad_request(0)
        self.tester.api_notification_delete_error_400_bad_request(-1)
        self.tester.api_notification_delete_error_400_bad_request("-1")
        self.tester.api_notification_delete_error_400_bad_request("0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_notification_error_403_forbidden(self):
        self.tester.api_notification_delete_error_403_forbidden("abc")
        self.tester.api_notification_delete_error_403_forbidden(0)
        self.tester.api_notification_delete_error_403_forbidden(-1)
        self.tester.api_notification_delete_error_403_forbidden("-1")
        self.tester.api_notification_delete_error_403_forbidden("0")
        self.tester.api_notification_delete_error_403_forbidden("1001")

    def test_delete_api_notification_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login_fake()

        self.tester.api_notification_delete_error_404_not_found("5000")
        self.tester.api_notification_delete_error_404_not_found("5001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

"""
# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
