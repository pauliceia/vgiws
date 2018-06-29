#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


class TestAPINotification(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # notification - get

    def test_get_api_notification_return_all_notifications(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Notification',
                    'properties': {'notification_id': 1001, 'is_denunciation': False, 'keyword_id': None,
                                   'user_id_creator': 1001, 'notification_id_parent': None, 'layer_id': None,
                                   'description': 'Congresso X acontecerá em 2018/03/25',
                                   'created_at': '2017-01-01 00:00:00'}
                },
                {
                    'type': 'Notification',
                    'properties': {'notification_id': 1005, 'is_denunciation': False, 'keyword_id': None,
                                   'user_id_creator': 1002, 'notification_id_parent': None, 'layer_id': None,
                                   'description': 'Evento Y no dia 24/06/2018',
                                   'created_at': '2017-02-01 00:00:00'}
                },
                {
                    'type': 'Notification',
                    'properties': {'notification_id': 1006, 'is_denunciation': False, 'keyword_id': None,
                                   'user_id_creator': 1003, 'notification_id_parent': 1005, 'layer_id': None,
                                   'description': 'Muito bom', 'created_at': '2017-02-01 00:00:00'}
                },
                {
                    'type': 'Notification',
                    'properties': {'notification_id': 1010, 'is_denunciation': True, 'keyword_id': None,
                                   'user_id_creator': 1005, 'notification_id_parent': None, 'layer_id': 1004,
                                   'description': 'A camada contêm dados inapropriados.',
                                   'created_at': '2017-03-01 00:00:00'}
                },
                {
                    'type': 'Notification',
                    'properties': {'notification_id': 1011, 'is_denunciation': False, 'keyword_id': None,
                                   'user_id_creator': 1003, 'notification_id_parent': 1010, 'layer_id': None,
                                   'description': 'Obrigado pelo aviso.', 'created_at': '2017-03-01 00:00:00'}
                },
                {
                    'type': 'Notification',
                    'properties': {'notification_id': 1012, 'is_denunciation': False, 'keyword_id': None,
                                   'user_id_creator': 1001, 'notification_id_parent': 1010, 'layer_id': None,
                                   'description': 'Ações estão sendo tomadas.',
                                   'created_at': '2017-03-01 00:00:00'}
                },
                {
                    'type': 'Notification',
                    'properties': {'notification_id': 1015, 'is_denunciation': False, 'keyword_id': None,
                                   'user_id_creator': 1002, 'notification_id_parent': None, 'layer_id': 1002,
                                   'description': 'Muito boa camada. Parabéns.',
                                   'created_at': '2017-04-05 00:00:00'}
                },
                {
                    'type': 'Notification',
                    'properties': {'notification_id': 1020, 'is_denunciation': False, 'keyword_id': 1001,
                                   'user_id_creator': 1001, 'notification_id_parent': None, 'layer_id': None,
                                   'description': 'Uma keyword genérica', 'created_at': '2017-01-01 00:00:00'}
                }
            ]
        }

        self.tester.api_notification(expected)

    def test_get_api_notification_return_notification_by_notification_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Notification',
                    'properties': {'notification_id': 1005, 'is_denunciation': False, 'keyword_id': None,
                                   'user_id_creator': 1002, 'notification_id_parent': None, 'layer_id': None,
                                   'description': 'Evento Y no dia 24/06/2018',
                                   'created_at': '2017-02-01 00:00:00'}
                }
            ]
        }

        self.tester.api_notification(expected, notification_id="1005")

    def test_get_api_notification_return_notification_by_user_id_creator(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Notification',
                    'properties': {'notification_id': 1006, 'is_denunciation': False, 'keyword_id': None,
                                   'user_id_creator': 1003, 'notification_id_parent': 1005, 'layer_id': None,
                                   'description': 'Muito bom', 'created_at': '2017-02-01 00:00:00'}
                },
                {
                    'type': 'Notification',
                    'properties': {'notification_id': 1011, 'is_denunciation': False, 'keyword_id': None,
                                   'user_id_creator': 1003, 'notification_id_parent': 1010, 'layer_id': None,
                                   'description': 'Obrigado pelo aviso.', 'created_at': '2017-03-01 00:00:00'}
                }
            ]
        }

        self.tester.api_notification(expected, user_id_creator="1003")

    def test_get_api_notification_return_notification_by_layer_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Notification',
                    'properties': {'notification_id': 1010, 'is_denunciation': True, 'keyword_id': None,
                                   'user_id_creator': 1005, 'notification_id_parent': None, 'layer_id': 1004,
                                   'description': 'A camada contêm dados inapropriados.',
                                   'created_at': '2017-03-01 00:00:00'}
                }
            ]
        }

        self.tester.api_notification(expected, layer_id="1004")

    def test_get_api_notification_return_notification_by_keyword_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Notification',
                    'properties': {'notification_id': 1020, 'is_denunciation': False, 'keyword_id': 1001,
                                   'user_id_creator': 1001, 'notification_id_parent': None, 'layer_id': None,
                                   'description': 'Uma keyword genérica', 'created_at': '2017-01-01 00:00:00'}
                }
            ]
        }

        self.tester.api_notification(expected, keyword_id="1001")

    def test_get_api_notification_return_notification_by_notification_id_parent(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Notification',
                    'properties': {'notification_id': 1011, 'is_denunciation': False, 'keyword_id': None,
                                   'user_id_creator': 1003, 'notification_id_parent': 1010, 'layer_id': None,
                                   'description': 'Obrigado pelo aviso.', 'created_at': '2017-03-01 00:00:00'}
                },
                {
                    'type': 'Notification',
                    'properties': {'notification_id': 1012, 'is_denunciation': False, 'keyword_id': None,
                                   'user_id_creator': 1001, 'notification_id_parent': 1010, 'layer_id': None,
                                   'description': 'Ações estão sendo tomadas.',
                                   'created_at': '2017-03-01 00:00:00'}
                }
            ]
        }

        self.tester.api_notification(expected, notification_id_parent="1010")

    def test_get_api_notification_return_notification_that_are_general(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Notification',
                    'properties': {'notification_id': 1001, 'is_denunciation': False, 'keyword_id': None,
                                   'user_id_creator': 1001, 'notification_id_parent': None, 'layer_id': None,
                                   'description': 'Congresso X acontecerá em 2018/03/25',
                                   'created_at': '2017-01-01 00:00:00'}
                },
                {
                    'type': 'Notification',
                    'properties': {'notification_id': 1005, 'is_denunciation': False, 'keyword_id': None,
                                   'user_id_creator': 1002, 'notification_id_parent': None, 'layer_id': None,
                                   'description': 'Evento Y no dia 24/06/2018',
                                   'created_at': '2017-02-01 00:00:00'}
                }
            ]
        }

        self.tester.api_notification(expected, layer_id="NULL", keyword_id="NULL", notification_id_parent="NULL")

    # notification - create update and delete

    def test_api_notification_create_update_and_delete(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # create notification
        ##################################################
        resource = {
            'type': 'Notification',
            'properties': {'notification_id': -1, 'is_denunciation': False, 'keyword_id': None,
                           'notification_id_parent': 1005, 'layer_id': None, 'description': 'Muito bom'}
        }
        resource = self.tester.api_notification_create(resource)

        ##################################################
        # update notification
        ##################################################
        resource["properties"]["description"] = "Muito legal"
        self.tester.api_notification_update(resource)

        ##################################################
        # remove notification
        ##################################################
        # get the id of layer to REMOVE it
        notification_id = resource["properties"]["notification_id"]

        # remove the user in layer
        self.tester.api_notification_delete(notification_id=notification_id)

        # it is not possible to find the layer that just deleted
        self.tester.api_notification_error_404_not_found(notification_id=notification_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_api_notification_create_but_update_and_delete_with_admin(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # create notification
        ##################################################
        resource = {
            'type': 'Notification',
            'properties': {'notification_id': -1, 'is_denunciation': False, 'keyword_id': None,
                           'notification_id_parent': 1005, 'layer_id': None, 'description': 'Muito bom'}
        }
        resource = self.tester.api_notification_create(resource)

        # login with admin
        self.tester.auth_logout()
        self.tester.auth_login("admin@admin.com", "admin")

        ##################################################
        # update notification
        ##################################################
        resource["properties"]["description"] = "Muito legal"
        self.tester.api_notification_update(resource)

        ##################################################
        # remove notification
        ##################################################
        # get the id of layer to REMOVE it
        notification_id = resource["properties"]["notification_id"]

        # remove the user in layer
        self.tester.api_notification_delete(notification_id=notification_id)

        # it is not possible to find the layer that just deleted
        self.tester.api_notification_error_404_not_found(notification_id=notification_id)

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

        self.tester.api_notification_error_400_bad_request(user_id_creator="abc")
        self.tester.api_notification_error_400_bad_request(user_id_creator=0)
        self.tester.api_notification_error_400_bad_request(user_id_creator=-1)
        self.tester.api_notification_error_400_bad_request(user_id_creator="-1")
        self.tester.api_notification_error_400_bad_request(user_id_creator="0")

        self.tester.api_notification_error_400_bad_request(layer_id="abc")
        self.tester.api_notification_error_400_bad_request(layer_id=0)
        self.tester.api_notification_error_400_bad_request(layer_id=-1)
        self.tester.api_notification_error_400_bad_request(layer_id="-1")
        self.tester.api_notification_error_400_bad_request(layer_id="0")

        self.tester.api_notification_error_400_bad_request(keyword_id="abc")
        self.tester.api_notification_error_400_bad_request(keyword_id=0)
        self.tester.api_notification_error_400_bad_request(keyword_id=-1)
        self.tester.api_notification_error_400_bad_request(keyword_id="-1")
        self.tester.api_notification_error_400_bad_request(keyword_id="0")

        self.tester.api_notification_error_400_bad_request(notification_id_parent="abc")
        self.tester.api_notification_error_400_bad_request(notification_id_parent=0)
        self.tester.api_notification_error_400_bad_request(notification_id_parent=-1)
        self.tester.api_notification_error_400_bad_request(notification_id_parent="-1")
        self.tester.api_notification_error_400_bad_request(notification_id_parent="0")

    def test_get_api_notification_error_404_not_found(self):
        self.tester.api_notification_error_404_not_found(notification_id="999")
        self.tester.api_notification_error_404_not_found(user_id_creator="998")
        self.tester.api_notification_error_404_not_found(layer_id="999")
        self.tester.api_notification_error_404_not_found(keyword_id="998")
        self.tester.api_notification_error_404_not_found(notification_id_parent="999")

    # notification errors - create
    """
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
