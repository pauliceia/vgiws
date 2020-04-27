#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/


class TestAPIReference(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # reference - get

    def test_get_api_reference_return_all_references(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1001, 'reference_id': 1001, 'description': '@Misc{jorge2017book1,\nauthor = {Jorge},\ntitle = {Book1},\nhowpublished = {\\url{http://www.link.org/}},\nnote = {Accessed on 01/01/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1001, 'reference_id': 1002, 'description': '@Misc{ana2017article2,\nauthor = {Ana},\ntitle = {Article2},\nhowpublished = {\\url{http://www.myhost.org/}},\nnote = {Accessed on 05/02/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1001, 'reference_id': 1005, 'description': '@Misc{marco2017articleB,\nauthor = {Marco},\ntitle = {ArticleB},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1005, 'reference_id': 1010, 'description': '@Misc{marco2017articleC,\nauthor = {Marco},\ntitle = {ArticleC},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1007, 'reference_id': 1025, 'description': '@Misc{frisina2017bookZ,\nauthor = {Frisina},\ntitle = {BookZ},\nhowpublished = {\\url{http://www.school.com/}},\nnote = {Accessed on 03/04/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1001, 'reference_id': 1050, 'description': 'BookA'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1002, 'reference_id': 1051, 'description': 'ArticleB'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1003, 'reference_id': 1052, 'description': 'ThesisC'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1003, 'reference_id': 1053, 'description': 'DissertationD'}
                }
            ]
        }

        self.tester.api_reference(expected)

    def test_get_api_reference_return_reference_by_reference_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1001, 'reference_id': 1001,
                                   'description': '@Misc{jorge2017book1,\nauthor = {Jorge},\ntitle = {Book1},\nhowpublished = {\\url{http://www.link.org/}},\nnote = {Accessed on 01/01/2017},\nyear={2017}\n}'}
                }
            ]
        }

        self.tester.api_reference(expected, reference_id="1001")

    def test_get_api_reference_return_reference_by_user_id_creator(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1001, 'reference_id': 1001,
                                   'description': '@Misc{jorge2017book1,\nauthor = {Jorge},\ntitle = {Book1},\nhowpublished = {\\url{http://www.link.org/}},\nnote = {Accessed on 01/01/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1001, 'reference_id': 1002,
                                   'description': '@Misc{ana2017article2,\nauthor = {Ana},\ntitle = {Article2},\nhowpublished = {\\url{http://www.myhost.org/}},\nnote = {Accessed on 05/02/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1001, 'reference_id': 1005, 'description': '@Misc{marco2017articleB,\nauthor = {Marco},\ntitle = {ArticleB},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1001, 'reference_id': 1050, 'description': 'BookA'}
                }
            ]
        }

        self.tester.api_reference(expected, user_id_creator="1001")

    def test_get_api_reference_return_reference_by_description(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1001, 'reference_id': 1005, 'description': '@Misc{marco2017articleB,\nauthor = {Marco},\ntitle = {ArticleB},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1005, 'reference_id': 1010,
                                   'description': '@Misc{marco2017articleC,\nauthor = {Marco},\ntitle = {ArticleC},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}'}
                }
            ]
        }

        self.tester.api_reference(expected, description="marco")

    def test_get_api_reference_return_zero_resources(self):
        expected = {'type': 'FeatureCollection', 'features': []}

        self.tester.api_reference(expected, reference_id="999")
        self.tester.api_reference(expected, reference_id="998")

        self.tester.api_reference(expected, user_id_creator="999")
        self.tester.api_reference(expected, user_id_creator="998")

    # reference - create, update and delete

    def test_api_reference_create_update_and_delete(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # create a reference
        ##################################################
        resource = {
            'type': 'Reference',
            'properties': {'description': 'ArticleA'}
        }
        resource = self.tester.api_reference_create(resource)

        ##################################################
        # update the reference
        ##################################################
        resource["properties"]["description"] = 'SomeArticleB'
        self.tester.api_reference_update(resource)

        ##################################################
        # check if the resource was modified
        ##################################################
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.tester.api_reference(expected_at_least=expected_resource,
                                  reference_id=resource["properties"]["reference_id"])

        ##################################################
        # remove the reference
        ##################################################
        # get the id of layer to REMOVE it
        resource_id = resource["properties"]["reference_id"]

        # remove the resource
        self.tester.api_reference_delete(resource_id)

        # it is not possible to find the resource that just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_reference(expected, reference_id=resource_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_api_reference_create_but_update_and_delete_with_admin_user(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # create a reference
        ##################################################
        resource = {
            'type': 'Reference',
            'properties': {'description': 'ArticleA'}
        }
        resource = self.tester.api_reference_create(resource)

        # logout with gabriel and login with admin user
        self.tester.auth_logout()
        self.tester.auth_login("admin@admin.com", "admin")

        ##################################################
        # update the reference
        ##################################################
        resource["properties"]["description"] = 'SomeArticleB'
        self.tester.api_reference_update(resource)

        ##################################################
        # check if the resource was modified
        ##################################################
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.tester.api_reference(expected_at_least=expected_resource,
                                  reference_id=resource["properties"]["reference_id"])

        ##################################################
        # remove the reference
        ##################################################
        # get the id of layer to REMOVE it
        resource_id = resource["properties"]["reference_id"]

        # remove the resource
        self.tester.api_reference_delete(resource_id)

        # it is not possible to find the resource that just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_reference(expected, reference_id=resource_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPIReferenceErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # reference errors - get

    def test_get_api_reference_error_400_bad_request(self):
        self.tester.api_reference_error_400_bad_request(reference_id="abc")
        self.tester.api_reference_error_400_bad_request(reference_id=0)
        self.tester.api_reference_error_400_bad_request(reference_id=-1)
        self.tester.api_reference_error_400_bad_request(reference_id="-1")
        self.tester.api_reference_error_400_bad_request(reference_id="0")

        self.tester.api_reference_error_400_bad_request(user_id_creator="abc")
        self.tester.api_reference_error_400_bad_request(user_id_creator=0)
        self.tester.api_reference_error_400_bad_request(user_id_creator=-1)
        self.tester.api_reference_error_400_bad_request(user_id_creator="-1")
        self.tester.api_reference_error_400_bad_request(user_id_creator="0")

    # reference errors - create

    # def test_post_api_reference_create_error_400_bad_request_attribute_already_exist(self):
    #     # DO LOGIN
    #     self.tester.auth_login("rodrigo@admin.com", "rodrigo")
    #
    #     ##################################################
    #     # try to insert one reference that already exist, raising the 400
    #     ##################################################
    #     resource = {
    #         'type': 'Reference',
    #         'properties': {'description': 'BookA'}
    #     }
    #     self.tester.api_reference_create_error_400_bad_request(resource)
    #
    #     # DO LOGOUT AFTER THE TESTS
    #     self.tester.auth_logout()

    def test_post_api_reference_create_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a layer (without description)
        resource = {
            'type': 'Reference',
            'properties': {}
        }
        self.tester.api_reference_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_reference_create_error_401_unauthorized_user_is_not_logged(self):
        feature = {
            'properties': {'description': 'BookA'},
            'type': 'Reference'
        }
        self.tester.api_reference_create_error_401_unauthorized(feature)

    # reference errors - update

    # def test_put_api_reference_error_400_bad_request_attribute_already_exist(self):
    #     # DO LOGIN
    #     self.tester.auth_login("rodrigo@admin.com", "rodrigo")
    #
    #     ##################################################
    #     # try to update a reference with a description that already exist, raising the 400
    #     ##################################################
    #     resource = {
    #         'type': 'Reference',
    #         'properties': {'reference_id': 1051, 'description': 'ThesisC'}
    #     }
    #     self.tester.api_reference_update_error_400_bad_request(resource)
    #
    #     # DO LOGOUT AFTER THE TESTS
    #     self.tester.auth_logout()

    def test_put_api_reference_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to update a layer (without reference_id)
        resource = {
            'type': 'Reference',
            'properties': {'description': 'BookA'}
        }
        self.tester.api_reference_update_error_400_bad_request(resource)

        # try to update a layer (without description)
        resource = {
            'type': 'Reference',
            'properties': {'reference_id': 1001}
        }
        self.tester.api_reference_update_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_reference_error_401_unauthorized_user_is_not_logged(self):
        feature = {
            'properties': {'reference_id': 1001, 'description': 'BookA'},
            'type': 'Reference'
        }
        self.tester.api_reference_update_error_401_unauthorized(feature)

    def test_put_api_reference_error_403_forbidden_invalid_user_tries_to_manage(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # gabriel tries to update one reference that doesn't belong to him
        ##################################################
        resource = {
            'type': 'Reference',
            'properties': {'reference_id': 1051, 'description': 'SomeArticleB'}
        }
        self.tester.api_reference_update_error_403_forbidden(resource)

        # DO LOGOUT
        self.tester.auth_logout()

    def test_put_api_reference_error_404_not_found(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        resource = {
            'type': 'Reference',
            'properties': {'reference_id': 999, 'description': 'SomeArticleB'}
        }
        self.tester.api_reference_update_error_404_not_found(resource)

        # DO LOGOUT
        self.tester.auth_logout()

    # reference errors - delete

    def test_delete_api_reference_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_reference_delete_error_400_bad_request("abc")
        self.tester.api_reference_delete_error_400_bad_request(0)
        self.tester.api_reference_delete_error_400_bad_request(-1)
        self.tester.api_reference_delete_error_400_bad_request("-1")
        self.tester.api_reference_delete_error_400_bad_request("0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_reference_error_401_unauthorized_user_without_login(self):
        self.tester.api_reference_delete_error_401_unauthorized("abc")
        self.tester.api_reference_delete_error_401_unauthorized(0)
        self.tester.api_reference_delete_error_401_unauthorized(-1)
        self.tester.api_reference_delete_error_401_unauthorized("-1")
        self.tester.api_reference_delete_error_401_unauthorized("0")
        self.tester.api_reference_delete_error_401_unauthorized("1001")

    def test_delete_api_reference_error_403_forbidden_invalid_user_tries_to_manage(self):
        self.tester.auth_login("miguel@admin.com", "miguel")

        ########################################
        # try to delete the reference with user miguel
        ########################################
        self.tester.api_reference_delete_error_403_forbidden(1001)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_reference_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_reference_delete_error_404_not_found("5000")
        self.tester.api_reference_delete_error_404_not_found("5001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
