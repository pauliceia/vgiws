
from unittest import TestCase

from util.tester import UtilTester


class TestAPINotification(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # notification - get

    def test_get_api_notification_return_all_notifications(self):
        expected = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1015,
                        "layer_id": 1002,
                        "username": "rodrigo",
                        "user_name": "Rodrigo",
                        "created_at": "2017-04-05 00:00:00",
                        "keyword_id": None,
                        "layer_name": "Robberies between 1880 to 1900",
                        "description": "Muito boa camada. Parabéns.",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1002,
                        "notification_id_parent": None
                    }
                },
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1012,
                        "layer_id": None,
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-03-01 00:00:00",
                        "keyword_id": None,
                        "layer_name": None,
                        "description": "Ações estão sendo tomadas.",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1001,
                        "notification_id_parent": 1010
                    }
                },
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1011,
                        "layer_id": None,
                        "username": "miguel",
                        "user_name": "Miguel",
                        "created_at": "2017-03-01 00:00:00",
                        "keyword_id": None,
                        "layer_name": None,
                        "description": "Obrigado pelo aviso.",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1003,
                        "notification_id_parent": 1010
                    }
                },
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1010,
                        "layer_id": 1004,
                        "username": "gabriel",
                        "user_name": "Gabriel",
                        "created_at": "2017-03-01 00:00:00",
                        "keyword_id": None,
                        "layer_name": "Streets in 1920",
                        "description": "A camada contêm dados inapropriados.",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": True,
                        "user_id_creator": 1005,
                        "notification_id_parent": None
                    }
                },
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1006,
                        "layer_id": None,
                        "username": "miguel",
                        "user_name": "Miguel",
                        "created_at": "2017-02-01 00:00:00",
                        "keyword_id": None,
                        "layer_name": None,
                        "description": "Muito bom",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1003,
                        "notification_id_parent": 1005
                    }
                },
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1005,
                        "layer_id": None,
                        "username": "rodrigo",
                        "user_name": "Rodrigo",
                        "created_at": "2017-02-01 00:00:00",
                        "keyword_id": None,
                        "layer_name": None,
                        "description": "Evento Y no dia 24/06/2018",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1002,
                        "notification_id_parent": None
                    }
                },
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1020,
                        "layer_id": None,
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "keyword_id": 1001,
                        "layer_name": None,
                        "description": "Uma keyword genérica",
                        "keyword_name": "generic",
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1001,
                        "notification_id_parent": None
                    }
                },
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1001,
                        "layer_id": None,
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "keyword_id": None,
                        "layer_name": None,
                        "description": "Congresso X acontecerá em 2018/03/25",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1001,
                        "notification_id_parent": None
                    }
                }
            ]
        }

        self.tester.api_notification(expected)

    def test_get_api_notification_return_notification_by_notification_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1005,
                        "layer_id": None,
                        "username": "rodrigo",
                        "user_name": "Rodrigo",
                        "created_at": "2017-02-01 00:00:00",
                        "keyword_id": None,
                        "layer_name": None,
                        "description": "Evento Y no dia 24/06/2018",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1002,
                        "notification_id_parent": None
                    }
                }
            ]
        }

        self.tester.api_notification(expected, id="1005")

    def test_get_api_notification_return_notification_by_user_id_creator(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1011,
                        "layer_id": None,
                        "username": "miguel",
                        "user_name": "Miguel",
                        "created_at": "2017-03-01 00:00:00",
                        "keyword_id": None,
                        "layer_name": None,
                        "description": "Obrigado pelo aviso.",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1003,
                        "notification_id_parent": 1010
                    }
                },
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1006,
                        "layer_id": None,
                        "username": "miguel",
                        "user_name": "Miguel",
                        "created_at": "2017-02-01 00:00:00",
                        "keyword_id": None,
                        "layer_name": None,
                        "description": "Muito bom",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1003,
                        "notification_id_parent": 1005
                    }
                }
            ]
        }

        self.tester.api_notification(expected, user_id_creator="1003")

    def test_get_api_notification_return_notification_by_layer_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1010,
                        "layer_id": 1004,
                        "username": "gabriel",
                        "user_name": "Gabriel",
                        "created_at": "2017-03-01 00:00:00",
                        "keyword_id": None,
                        "layer_name": "Streets in 1920",
                        "description": "A camada contêm dados inapropriados.",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": True,
                        "user_id_creator": 1005,
                        "notification_id_parent": None
                    }
                }
            ]
        }

        self.tester.api_notification(expected, layer_id="1004")

    def test_get_api_notification_return_notification_by_keyword_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1020,
                        "layer_id": None,
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "keyword_id": 1001,
                        "layer_name": None,
                        "description": "Uma keyword genérica",
                        "keyword_name": "generic",
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1001,
                        "notification_id_parent": None
                    }
                }
            ]
        }

        self.tester.api_notification(expected, keyword_id="1001")

    def test_get_api_notification_return_notification_by_notification_id_parent(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1012,
                        "layer_id": None,
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-03-01 00:00:00",
                        "keyword_id": None,
                        "layer_name": None,
                        "description": "Ações estão sendo tomadas.",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1001,
                        "notification_id_parent": 1010
                    }
                },
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1011,
                        "layer_id": None,
                        "username": "miguel",
                        "user_name": "Miguel",
                        "created_at": "2017-03-01 00:00:00",
                        "keyword_id": None,
                        "layer_name": None,
                        "description": "Obrigado pelo aviso.",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1003,
                        "notification_id_parent": 1010
                    }
                }
            ]
        }

        self.tester.api_notification(expected, notification_id_parent="1010")

    def test_get_api_notification_return_notification_that_are_general(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1005,
                        "layer_id": None,
                        "username": "rodrigo",
                        "user_name": "Rodrigo",
                        "created_at": "2017-02-01 00:00:00",
                        "keyword_id": None,
                        "layer_name": None,
                        "description": "Evento Y no dia 24/06/2018",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1002,
                        "notification_id_parent": None
                    }
                },
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1001,
                        "layer_id": None,
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "keyword_id": None,
                        "layer_name": None,
                        "description": "Congresso X acontecerá em 2018/03/25",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1001,
                        "notification_id_parent": None
                    }
                }
            ]
        }

        self.tester.api_notification(expected, layer_id="NULL", keyword_id="NULL", notification_id_parent="NULL")

    def test_get_api_notification_return_denunciations(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1010,
                        "layer_id": 1004,
                        "username": "gabriel",
                        "user_name": "Gabriel",
                        "created_at": "2017-03-01 00:00:00",
                        "keyword_id": None,
                        "layer_name": "Streets in 1920",
                        "description": "A camada contêm dados inapropriados.",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": True,
                        "user_id_creator": 1005,
                        "notification_id_parent": None
                    }
                }
            ]
        }

        self.tester.api_notification(expected, is_denunciation=True)

        expected = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1015,
                        "layer_id": 1002,
                        "username": "rodrigo",
                        "user_name": "Rodrigo",
                        "created_at": "2017-04-05 00:00:00",
                        "keyword_id": None,
                        "layer_name": "Robberies between 1880 to 1900",
                        "description": "Muito boa camada. Parabéns.",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1002,
                        "notification_id_parent": None
                    }
                },
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1012,
                        "layer_id": None,
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-03-01 00:00:00",
                        "keyword_id": None,
                        "layer_name": None,
                        "description": "Ações estão sendo tomadas.",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1001,
                        "notification_id_parent": 1010
                    }
                },
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1011,
                        "layer_id": None,
                        "username": "miguel",
                        "user_name": "Miguel",
                        "created_at": "2017-03-01 00:00:00",
                        "keyword_id": None,
                        "layer_name": None,
                        "description": "Obrigado pelo aviso.",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1003,
                        "notification_id_parent": 1010
                    }
                },
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1006,
                        "layer_id": None,
                        "username": "miguel",
                        "user_name": "Miguel",
                        "created_at": "2017-02-01 00:00:00",
                        "keyword_id": None,
                        "layer_name": None,
                        "description": "Muito bom",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1003,
                        "notification_id_parent": 1005
                    }
                },
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1005,
                        "layer_id": None,
                        "username": "rodrigo",
                        "user_name": "Rodrigo",
                        "created_at": "2017-02-01 00:00:00",
                        "keyword_id": None,
                        "layer_name": None,
                        "description": "Evento Y no dia 24/06/2018",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1002,
                        "notification_id_parent": None
                    }
                },
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1020,
                        "layer_id": None,
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "keyword_id": 1001,
                        "layer_name": None,
                        "description": "Uma keyword genérica",
                        "keyword_name": "generic",
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1001,
                        "notification_id_parent": None
                    }
                },
                {
                    "type": "Notification",
                    "properties": {
                        "id": 1001,
                        "layer_id": None,
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "keyword_id": None,
                        "layer_name": None,
                        "description": "Congresso X acontecerá em 2018/03/25",
                        "keyword_name": None,
                        "user_picture": "",
                        "is_denunciation": False,
                        "user_id_creator": 1001,
                        "notification_id_parent": None
                    }
                }
            ]
        }

        self.tester.api_notification(expected, is_denunciation=False)

    def test_get_api_notification_error_404_not_found(self):
        expected = {'type': 'FeatureCollection', 'features': []}

        self.tester.api_notification(expected, id="999")
        self.tester.api_notification(expected, user_id_creator="998")
        self.tester.api_notification(expected, layer_id="999")
        self.tester.api_notification(expected, keyword_id="998")
        self.tester.api_notification(expected, notification_id_parent="999")

    # notification - create update and delete

    def test_api_notification_create_update_and_delete_general(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # create notification
        ##################################################
        resource = {
            'type': 'Notification',
            'properties': {'id': -1, 'is_denunciation': False, 'keyword_id': None,
                           'notification_id_parent': None, 'layer_id': None, 'description': 'Congresso de HD no RJ'}
        }
        notification_id = self.tester.api_notification_create(resource)
        resource["properties"]["id"] = notification_id

        ##################################################
        # update notification
        ##################################################
        resource["properties"]["description"] = "Muito legal"
        self.tester.api_notification_update(resource)

        ##################################################
        # check if the resource was modified
        ##################################################
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.tester.api_notification(expected_at_least=expected_resource,
                                     id=notification_id)

        ##################################################
        # remove notification
        ##################################################
        # remove the user in layer
        self.tester.api_notification_delete(id=notification_id)

        # it is not possible to find the notification that was just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_notification(expected, id=notification_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_api_notification_create_update_and_delete_layer(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # create notification
        ##################################################
        resource = {
            'type': 'Notification',
            'properties': {'id': -1, 'is_denunciation': False, 'keyword_id': None,
                           'notification_id_parent': None, 'layer_id': 1001, 'description': 'Ótimos dados'}
        }
        notification_id = self.tester.api_notification_create(resource)
        resource["properties"]["id"] = notification_id

        ##################################################
        # update notification
        ##################################################
        resource["properties"]["description"] = "Dados bons"
        self.tester.api_notification_update(resource)

        ##################################################
        # check if the resource was modified
        ##################################################
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.tester.api_notification(expected_at_least=expected_resource,
                                     id=notification_id)

        ##################################################
        # remove notification
        ##################################################
        # remove the user in layer
        self.tester.api_notification_delete(id=notification_id)

        # it is not possible to find the layer that was just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_notification(expected, id=notification_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_api_notification_create_update_and_delete_keyword(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # create notification
        ##################################################
        resource = {
            'type': 'Notification',
            'properties': {'id': -1, 'is_denunciation': False, 'keyword_id': 1001,
                           'notification_id_parent': None, 'layer_id': None, 'description': 'Ótima keyword'}
        }
        notification_id = self.tester.api_notification_create(resource)
        resource["properties"]["id"] = notification_id

        ##################################################
        # update notification
        ##################################################
        resource["properties"]["description"] = "Dados bons"
        self.tester.api_notification_update(resource)

        ##################################################
        # check if the resource was modified
        ##################################################
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.tester.api_notification(expected_at_least=expected_resource,
                                     id=notification_id)

        ##################################################
        # remove notification
        ##################################################
        # remove the user in layer
        self.tester.api_notification_delete(id=notification_id)

        # it is not possible to find the layer that was just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_notification(expected, id=notification_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_api_notification_create_update_and_delete_denunciation(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # create notification
        ##################################################
        resource = {
            'type': 'Notification',
            'properties': {'id': -1, 'is_denunciation': True, 'keyword_id': None,
                           'notification_id_parent': None, 'layer_id': 1001, 'description': 'Problema com dados'}
        }
        notification_id = self.tester.api_notification_create(resource)
        resource["properties"]["id"] = notification_id

        ##################################################
        # update notification
        ##################################################
        resource["properties"]["description"] = "Dados bons"
        self.tester.api_notification_update(resource)

        ##################################################
        # check if the resource was modified
        ##################################################
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.tester.api_notification(expected_at_least=expected_resource,
                                     id=notification_id)

        ##################################################
        # remove notification
        ##################################################
        # remove the user in layer
        self.tester.api_notification_delete(id=notification_id)

        # it is not possible to find the layer that was just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_notification(expected, id=notification_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_api_notification_create_update_and_delete_comment(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # create notification
        ##################################################
        resource = {
            'type': 'Notification',
            'properties': {'id': -1, 'is_denunciation': False, 'keyword_id': None,
                           'notification_id_parent': 1005, 'layer_id': None, 'description': 'Muito bom'}
        }
        notification_id = self.tester.api_notification_create(resource)
        resource["properties"]["id"] = notification_id

        ##################################################
        # update notification
        ##################################################
        resource["properties"]["description"] = "Muito legal"
        self.tester.api_notification_update(resource)

        ##################################################
        # check if the resource was modified
        ##################################################
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.tester.api_notification(expected_at_least=expected_resource,
                                     id=notification_id)

        ##################################################
        # remove notification
        ##################################################
        # remove the user in layer
        self.tester.api_notification_delete(id=notification_id)

        # it is not possible to find the layer that just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_notification(expected, id=notification_id)

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
            'properties': {'id': -1, 'is_denunciation': False, 'keyword_id': None,
                           'notification_id_parent': 1005, 'layer_id': None, 'description': 'Muito bom'}
        }
        notification_id = self.tester.api_notification_create(resource)
        resource["properties"]["id"] = notification_id

        # login with admin
        self.tester.auth_logout()
        self.tester.auth_login("admin@admin.com", "admin")

        ##################################################
        # update notification
        ##################################################
        resource["properties"]["description"] = "Muito legal"
        self.tester.api_notification_update(resource)

        ##################################################
        # check if the resource was modified
        ##################################################
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.tester.api_notification(expected_at_least=expected_resource,
                                     id=notification_id)

        ##################################################
        # remove notification
        ##################################################
        # remove the user in layer
        self.tester.api_notification_delete(id=notification_id)

        # it is not possible to find the layer that just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_notification(expected, id=notification_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_api_notification_create_update_and_delete_notification_with_reply(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # create notification
        ##################################################
        notification = {
            'type': 'Notification',
            'properties': {'id': -1, 'is_denunciation': False, 'keyword_id': None,
                           'notification_id_parent': None, 'layer_id': None, 'description': 'Congresso de HD no RJ'}
        }
        notification_id = self.tester.api_notification_create(notification)
        notification["properties"]["id"] = notification_id

        ##################################################
        # create reply
        ##################################################
        reply = {
            'type': 'Notification',
            'properties': {'id': -1, 'is_denunciation': False, 'keyword_id': None,
                           'notification_id_parent': notification_id, 'layer_id': None, 'description': 'Legal!'}
        }
        reply_id = self.tester.api_notification_create(reply)
        reply["properties"]["id"] = reply_id

        ##################################################
        # check if the notification was added
        ##################################################
        expected_resource = {'type': 'FeatureCollection', 'features': [notification]}
        self.tester.api_notification(expected_at_least=expected_resource,
                                     id=notification_id)

        ##################################################
        # check if the reply was added
        ##################################################
        expected_resource = {'type': 'FeatureCollection', 'features': [reply]}
        self.tester.api_notification(expected_at_least=expected_resource,
                                     id=reply_id)

        ##################################################
        # remove notification
        ##################################################
        # remove the notification (and together the reply)
        self.tester.api_notification_delete(id=notification_id)

        # it is not possible to find the notification that just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_notification(expected, id=notification_id)

        # it is not possible to find the reply that just deleted
        self.tester.api_notification(expected, id=reply_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPINotificationErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # notification errors - get

    def test_get_api_notification_error_400_bad_request(self):
        self.tester.api_notification_error_400_bad_request(id="abc")
        self.tester.api_notification_error_400_bad_request(id=0)
        self.tester.api_notification_error_400_bad_request(id=-1)
        self.tester.api_notification_error_400_bad_request(id="-1")
        self.tester.api_notification_error_400_bad_request(id="0")

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

    # notification errors - create

    def test_post_api_notification_create_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        # try to create a notification (without description)
        resource = {
            'type': 'Notification',
            'properties': {'is_denunciation': False, 'keyword_id': None,
                           'notification_id_parent': 1005, 'layer_id': None}
        }
        self.tester.api_notification_create_error_400_bad_request(resource)

        # try to create a notification (without is_denunciation)
        resource = {
            'type': 'Notification',
            'properties': {'description': 'Muito bom', 'keyword_id': None,
                           'notification_id_parent': 1005, 'layer_id': None}
        }
        self.tester.api_notification_create_error_400_bad_request(resource)

        # try to create a notification (without keyword_id)
        resource = {
            'type': 'Notification',
            'properties': {'description': 'Muito bom', 'is_denunciation': False,
                           'notification_id_parent': 1005, 'layer_id': None}
        }
        self.tester.api_notification_create_error_400_bad_request(resource)

        # try to create a notification (without notification_id_parent)
        resource = {
            'type': 'Notification',
            'properties': {'description': 'Muito bom', 'is_denunciation': False, 'keyword_id': None,
                           'layer_id': None}
        }
        self.tester.api_notification_create_error_400_bad_request(resource)

        # try to create a notification (without layer_id)
        resource = {
            'type': 'Notification',
            'properties': {'description': 'Muito bom', 'is_denunciation': False, 'keyword_id': None,
                           'notification_id_parent': 1005}
        }
        self.tester.api_notification_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_notification_create_error_401_unauthorized_user_is_not_logged(self):
        resource = {
            'type': 'Notification',
            'properties': {'id': -1, 'is_denunciation': False, 'keyword_id': None,
                           'notification_id_parent': 1005, 'layer_id': None, 'description': 'Muito bom'}
        }
        self.tester.api_notification_create_error_401_unauthorized(resource)

    # notification errors - update

    def test_put_api_notification_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        # try to update a notification (without notification_id)
        resource = {
            'type': 'Notification',
            'properties': {'is_denunciation': False, 'keyword_id': None, 'description': 'Muito bom',
                           'user_id_creator': 1003, 'notification_id_parent': 1005, 'layer_id': None}
        }
        self.tester.api_notification_update_error_400_bad_request(resource)

        # try to update a notification (without description)
        resource = {
            'type': 'Notification',
            'properties': {'id': 1006, 'is_denunciation': False, 'keyword_id': None,
                           'user_id_creator': 1003, 'notification_id_parent': 1005, 'layer_id': None}
        }
        self.tester.api_notification_update_error_400_bad_request(resource)

        # try to update a notification (without keyword_id)
        resource = {
            'type': 'Notification',
            'properties': {'id': 1006, 'is_denunciation': False, 'description': 'Muito bom',
                           'user_id_creator': 1003, 'notification_id_parent': 1005, 'layer_id': None}
        }
        self.tester.api_notification_update_error_400_bad_request(resource)

        # try to update a notification (without notification_id_parent)
        resource = {
            'type': 'Notification',
            'properties': {'id': 1006, 'is_denunciation': False, 'keyword_id': None,
                           'user_id_creator': 1003, 'layer_id': None, 'description': 'Muito bom'}
        }
        self.tester.api_notification_update_error_400_bad_request(resource)

        # try to update a notification (without layer_id)
        resource = {
            'type': 'Notification',
            'properties': {'id': 1006, 'is_denunciation': False, 'keyword_id': None,
                           'user_id_creator': 1003, 'notification_id_parent': 1005, 'description': 'Muito bom'}
        }
        self.tester.api_notification_update_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_notification_error_401_unauthorized_user_is_not_logged(self):
        resource = {
            'type': 'Notification',
            'properties': {'is_denunciation': False, 'keyword_id': None,
                           'notification_id_parent': 1005, 'layer_id': None, 'description': 'Muito bom'}
        }
        self.tester.api_notification_update_error_401_unauthorized(resource)

    def test_put_api_notification_error_403_forbidden_invalid_user_tries_to_manage(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # miguel tries to update one notification that doesn't belong to him
        ##################################################
        resource = {
            'type': 'Notification',
            'properties': {'id': 1001, 'is_denunciation': False, 'keyword_id': None,
                           'user_id_creator': 1001, 'notification_id_parent': None, 'layer_id': None,
                           'description': 'Congresso Z 2018/03/25'}
        }
        self.tester.api_notification_update_error_403_forbidden(resource)

        # DO LOGOUT
        self.tester.auth_logout()

    def test_put_api_notification_error_404_not_found(self):
        # DO LOGIN
        self.tester.auth_login("admin@admin.com", "admin")

        resource = {
            'type': 'Notification',
            'properties': {'id': 999, 'is_denunciation': False, 'keyword_id': None,
                           'user_id_creator': 1001, 'notification_id_parent': None, 'layer_id': None,
                           'description': 'Congresso Z 2018/03/25'}
        }
        self.tester.api_notification_update_error_404_not_found(resource)

        # DO LOGOUT
        self.tester.auth_logout()

    # notification errors - delete

    def test_delete_api_notification_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        self.tester.api_notification_delete_error_400_bad_request(id="abc")
        self.tester.api_notification_delete_error_400_bad_request(id=0)
        self.tester.api_notification_delete_error_400_bad_request(id=-1)
        self.tester.api_notification_delete_error_400_bad_request(id="-1")
        self.tester.api_notification_delete_error_400_bad_request(id="0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_notification_error_401_unauthorized_user_is_not_logged(self):
        self.tester.api_notification_delete_error_401_unauthorized(id="abc")
        self.tester.api_notification_delete_error_401_unauthorized(id=0)
        self.tester.api_notification_delete_error_401_unauthorized(id=-1)
        self.tester.api_notification_delete_error_401_unauthorized(id="-1")
        self.tester.api_notification_delete_error_401_unauthorized(id="0")
        self.tester.api_notification_delete_error_401_unauthorized(id="1001")

    def test_delete_api_notification_error_403_forbidden_invalid_user_tries_to_manage(self):
        self.tester.auth_login("miguel@admin.com", "miguel")

        ########################################
        # try to delete the notification with user gabriel
        ########################################
        self.tester.api_notification_delete_error_403_forbidden(id="1001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_notification_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_notification_delete_error_404_not_found(id="5000")
        self.tester.api_notification_delete_error_404_not_found(id="5001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


# NOTIFICATIONS (GENERAL + FOLLOWERS) RELATED TO A SPECIFIC USER

class TestAPINotificationRelatedToUser(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # notification - get

    def test_get_api_notification_related_to_user_return_notification_by_user_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Notification',
                    'properties': {
                        'id': 1015, 'notification_id_parent': None, 'created_at': '2017-04-05 00:00:00',
                        'layer_id': 1002, 'description': 'Muito boa camada. Parabéns.', 'user_id_creator': 1002,
                        'keyword_id': None, 'is_denunciation': False
                    }
                },
                {
                    'type': 'Notification',
                    'properties': {
                        'id': 1005, 'notification_id_parent': None, 'created_at': '2017-02-01 00:00:00',
                        'layer_id': None, 'description': 'Evento Y no dia 24/06/2018', 'user_id_creator': 1002,
                        'keyword_id': None, 'is_denunciation': False
                    }
                },
                {
                    'type': 'Notification',
                    'properties': {
                        'id': 1001, 'notification_id_parent': None, 'created_at': '2017-01-01 00:00:00',
                        'layer_id': None, 'description': 'Congresso X acontecerá em 2018/03/25', 'user_id_creator': 1001,
                        'keyword_id': None, 'is_denunciation': False
                    }
                }
            ]
        }

        self.tester.api_notification_related_to_user(expected, user_id="1001")
        self.tester.api_notification_related_to_user(expected, user_id="1003")

        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Notification',
                    'properties': {
                        'id': 1005, 'notification_id_parent': None, 'created_at': '2017-02-01 00:00:00',
                        'layer_id': None, 'description': 'Evento Y no dia 24/06/2018', 'user_id_creator': 1002,
                        'keyword_id': None, 'is_denunciation': False
                    }
                },
                {
                    'type': 'Notification',
                    'properties': {
                        'id': 1001, 'notification_id_parent': None, 'created_at': '2017-01-01 00:00:00',
                        'layer_id': None, 'description': 'Congresso X acontecerá em 2018/03/25',
                        'user_id_creator': 1001, 'keyword_id': None, 'is_denunciation': False
                    }
                }
            ]
        }

        self.tester.api_notification_related_to_user(expected, user_id="1002")


class TestAPINotificationRelatedToUserErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # notification errors - get

    def test_get_api_notification_error_400_bad_request(self):
        list_of_bad_user_id = ["abc", 0, -1, "-1", "0"]

        for bad_user_id in list_of_bad_user_id:
            self.tester.api_notification_related_to_user_error_400_bad_request(user_id=bad_user_id)

    def test_get_api_notification_error_404_not_found_user_doesn_exist(self):
        self.tester.api_notification_related_to_user_error_404_not_found(user_id="999")
        self.tester.api_notification_related_to_user_error_404_not_found(user_id="998")


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
