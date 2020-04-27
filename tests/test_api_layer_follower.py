#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/


class TestAPILayerFollower(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # layer_follower - get

    def test_get_api_layer_follower_return_all_followers_in_layer(self):
        expected = {
            'features': [
                {
                    'properties': {'created_at': '2017-01-01 00:00:00', 'layer_id': 1001, 'user_id': 1001},
                    'type': 'LayerFollower'
                },
                {
                    'properties': {'created_at': '2017-01-05 00:00:00', 'layer_id': 1001, 'user_id': 1002},
                    'type': 'LayerFollower'
                },
                {
                    'properties': {'created_at': '2017-01-08 00:00:00', 'layer_id': 1001, 'user_id': 1003},
                    'type': 'LayerFollower'
                },
                {
                    'properties': {'created_at': '2017-01-02 00:00:00', 'layer_id': 1002, 'user_id': 1001},
                    'type': 'LayerFollower'
                },
                {
                    'properties': {'created_at': '2017-01-02 00:00:00', 'layer_id': 1002, 'user_id': 1003},
                    'type': 'LayerFollower'
                },
                {
                    'properties': {'created_at': '2017-01-02 00:00:00', 'layer_id': 1002, 'user_id': 1005},
                    'type': 'LayerFollower'
                },
                {
                    'properties': {'created_at': '2017-01-02 00:00:00', 'layer_id': 1003, 'user_id': 1003},
                    'type': 'LayerFollower'
                },
                {
                    'properties': {'created_at': '2017-01-02 00:00:00', 'layer_id': 1003, 'user_id': 1006},
                    'type': 'LayerFollower'
                },
                {
                    'properties': {'created_at': '2017-01-02 00:00:00', 'layer_id': 1003, 'user_id': 1007},
                    'type': 'LayerFollower'
                },
                {
                    'properties': {'created_at': '2017-01-09 00:00:00', 'layer_id': 1004, 'user_id': 1003},
                    'type': 'LayerFollower'
                },
                {
                    'properties': {'created_at': '2017-01-02 00:00:00', 'layer_id': 1005, 'user_id': 1003},
                    'type': 'LayerFollower'
                },
                {
                    'properties': {'created_at': '2017-01-02 00:00:00', 'layer_id': 1005, 'user_id': 1004},
                    'type': 'LayerFollower'
                },
                {
                    'properties': {'created_at': '2017-01-02 00:00:00', 'layer_id': 1005, 'user_id': 1005},
                    'type': 'LayerFollower'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_layer_follower(expected)

    def test_get_api_layer_follower_return_user_layer_by_layer_id(self):
        expected = {
            'features': [
                {
                    'properties': {'created_at': '2017-01-02 00:00:00', 'layer_id': 1002, 'user_id': 1001},
                    'type': 'LayerFollower'
                },
                {
                    'properties': {'created_at': '2017-01-02 00:00:00', 'layer_id': 1002, 'user_id': 1003},
                    'type': 'LayerFollower'
                },
                {
                    'properties': {'created_at': '2017-01-02 00:00:00', 'layer_id': 1002, 'user_id': 1005},
                    'type': 'LayerFollower'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_layer_follower(expected, layer_id="1002")

    def test_get_api_layer_follower_return_user_layer_by_user_id(self):
        expected = {
            'features': [
                {
                    'properties': {'created_at': '2017-01-02 00:00:00', 'layer_id': 1002, 'user_id': 1005},
                    'type': 'LayerFollower'
                },
                {
                    'properties': {'created_at': '2017-01-02 00:00:00', 'layer_id': 1005, 'user_id': 1005},
                    'type': 'LayerFollower'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_layer_follower(expected, user_id="1005")

    def test_get_api_layer_follower_return_user_layer_by_user_id_and_layer_id(self):
        expected = {
            'features': [
                {
                    'properties': {'created_at': '2017-01-02 00:00:00', 'layer_id': 1002, 'user_id': 1003},
                    'type': 'LayerFollower'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.tester.api_layer_follower(expected, user_id="1003", layer_id="1002")

    def test_get_api_layer_follower_return_zero_resources(self):
        expected = {'features': [], 'type': 'FeatureCollection'}

        self.tester.api_layer_follower(expected, layer_id="999")
        self.tester.api_layer_follower(expected, layer_id="998")

        self.tester.api_layer_follower(expected, user_id="999")
        self.tester.api_layer_follower(expected, user_id="998")

    # layer_follower - create and delete

    def test_api_layer_follower_create_and_delete(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        # add a user in a layer
        layer_follower = {
            'properties': {'layer_id': 1006},
            'type': 'LayerFollower'
        }
        self.tester.api_layer_follower_create(layer_follower)

        # get the id of layer to REMOVE it
        user_id = 1003
        layer_id = layer_follower["properties"]["layer_id"]

        # remove the user in layer
        self.tester.api_layer_follower_delete(user_id=user_id, layer_id=layer_id)

        # it is not possible to find the layer that just deleted
        expected = {'features': [], 'type': 'FeatureCollection'}
        self.tester.api_layer_follower(expected, user_id=user_id, layer_id=layer_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPIUserLayerErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # layer_follower errors - get

    def test_get_api_layer_follower_error_400_bad_request(self):
        self.tester.api_layer_follower_error_400_bad_request(layer_id="abc")
        self.tester.api_layer_follower_error_400_bad_request(layer_id=0)
        self.tester.api_layer_follower_error_400_bad_request(layer_id=-1)
        self.tester.api_layer_follower_error_400_bad_request(layer_id="-1")
        self.tester.api_layer_follower_error_400_bad_request(layer_id="0")

        self.tester.api_layer_follower_error_400_bad_request(user_id="abc")
        self.tester.api_layer_follower_error_400_bad_request(user_id=0)
        self.tester.api_layer_follower_error_400_bad_request(user_id=-1)
        self.tester.api_layer_follower_error_400_bad_request(user_id="-1")
        self.tester.api_layer_follower_error_400_bad_request(user_id="0")

    # layer_follower errors - create

    def test_post_api_layer_follower_create_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        # try to add a user in a layer (without is_the_creator)
        user_layer = {
            'properties': {},
            'type': 'LayerFollower'
        }
        # try to add the user in layer again and raise an error
        self.tester.api_layer_follower_create_error_400_bad_request(user_layer)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_layer_follower_create_error_401_unauthorized_without_authorization_header(self):
        resource = {
            'properties': {'layer_id': 1001},
            'type': 'LayerFollower'
        }
        self.tester.api_layer_follower_create_error_401_unauthorized(resource)

    def test_post_api_layer_follower_create_error_409_conflict_user_already_follow_or_is_collaborator(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        # user miguel (1003) tries to follow a layer that he already follow
        layer_follower = {
            'properties': {'layer_id': 1001},
            'type': 'LayerFollower'
        }

        self.tester.api_layer_follower_create_error_409_conflict(layer_follower)

        # # user miguel (1003) tries to follow a layer that he is a owner
        # layer_follower = {
        #     'properties': {'layer_id': 1003},
        #     'type': 'LayerFollower'
        # }
        #
        # self.tester.api_layer_follower_create_error_409_conflict(layer_follower)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    # def test_post_api_layer_follower_create_error_403_forbidden_invalid_user_tries_to_add_user_in_layer(self):
    #     # DO LOGIN
    #     # login with gabriel and he tries to add a user in the layer of admin
    #     self.tester.auth_login("miguel@admin.com", "miguel")
    #
    #     # add a user in a layer
    #     user_layer = {
    #         'properties': {'is_the_creator': True, 'user_id': 1004, 'layer_id': 1002},
    #         'type': 'UserLayer'
    #     }
    #     self.tester.api_user_layer_create_error_403_forbidden(user_layer)
    #
    #     # DO LOGOUT AFTER THE TESTS
    #     self.tester.auth_logout()

    # layer_follower errors - delete

    def test_delete_api_layer_follower_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        self.tester.api_layer_follower_delete_error_400_bad_request(user_id="abc", layer_id="abc")
        self.tester.api_layer_follower_delete_error_400_bad_request(user_id=0, layer_id=0)
        self.tester.api_layer_follower_delete_error_400_bad_request(user_id=-1, layer_id=-1)
        self.tester.api_layer_follower_delete_error_400_bad_request(user_id="-1", layer_id="-1")
        self.tester.api_layer_follower_delete_error_400_bad_request(user_id="0", layer_id="0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_layer_follower_error_401_unauthorized_user_without_login(self):
        self.tester.api_layer_follower_delete_error_401_unauthorized(user_id=1001, layer_id=1001)
        self.tester.api_layer_follower_delete_error_401_unauthorized(user_id=1001, layer_id="1001")
        self.tester.api_layer_follower_delete_error_401_unauthorized(user_id=0, layer_id=-1)
        self.tester.api_layer_follower_delete_error_401_unauthorized(user_id="0", layer_id="-1")

    # def test_delete_api_layer_follower_error_403_forbidden_user_forbidden_to_delete_user_in_layer(self):
    #     # DO LOGIN
    #
    #     # login with other user (admin) and he tries to delete a user from a layer of rodrigo
    #     self.tester.auth_login("miguel@admin.com", "miguel")
    #
    #     # try to remove the user in layer
    #     self.tester.api_user_layer_delete_error_403_forbidden(user_id=1004, layer_id=1002)
    #
    #     # DO LOGOUT AFTER THE TESTS
    #     self.tester.auth_logout()

    def test_delete_api_layer_follower_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_layer_follower_delete_error_404_not_found(user_id=1001, layer_id=5000)
        self.tester.api_layer_follower_delete_error_404_not_found(user_id=1001, layer_id=5001)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
