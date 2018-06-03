#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/

"""
class TestAPIKeyword(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # keyword - get

    def test_get_api_keyword_return_all_keywords(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'keyword',
                    'properties': {'user_id': 1001, 'keyword_id': 1001, 'description': '@Misc{jorge2017book1,\nauthor = {Jorge},\ntitle = {Book1},\nhowpublished = {\\url{http://www.link.org/}},\nnote = {Accessed on 01/01/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'keyword',
                    'properties': {'user_id': 1001, 'keyword_id': 1002, 'description': '@Misc{ana2017article2,\nauthor = {Ana},\ntitle = {Article2},\nhowpublished = {\\url{http://www.myhost.org/}},\nnote = {Accessed on 05/02/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'keyword',
                    'properties': {'user_id': 1001, 'keyword_id': 1005, 'description': '@Misc{marco2017articleB,\nauthor = {Marco},\ntitle = {ArticleB},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'keyword',
                    'properties': {'user_id': 1005, 'keyword_id': 1010, 'description': '@Misc{marco2017articleC,\nauthor = {Marco},\ntitle = {ArticleC},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'keyword',
                    'properties': {'user_id': 1007, 'keyword_id': 1025, 'description': '@Misc{frisina2017bookZ,\nauthor = {Frisina},\ntitle = {BookZ},\nhowpublished = {\\url{http://www.school.com/}},\nnote = {Accessed on 03/04/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'keyword',
                    'properties': {'user_id': 1001, 'keyword_id': 1050, 'description': 'BookA'}
                },
                {
                    'type': 'keyword',
                    'properties': {'user_id': 1002, 'keyword_id': 1051, 'description': 'ArticleB'}
                },
                {
                    'type': 'keyword',
                    'properties': {'user_id': 1003, 'keyword_id': 1052, 'description': 'ThesisC'}
                },
                {
                    'type': 'keyword',
                    'properties': {'user_id': 1003, 'keyword_id': 1053, 'description': 'DissertationD'}
                }
            ]
        }

        self.tester.api_keyword(expected)

    def test_get_api_keyword_return_keyword_by_keyword_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'keyword',
                    'properties': {'user_id': 1001, 'keyword_id': 1001,
                                   'description': '@Misc{jorge2017book1,\nauthor = {Jorge},\ntitle = {Book1},\nhowpublished = {\\url{http://www.link.org/}},\nnote = {Accessed on 01/01/2017},\nyear={2017}\n}'}
                }
            ]
        }

        self.tester.api_keyword(expected, keyword_id="1001")

    def test_get_api_keyword_return_keyword_by_user_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'keyword',
                    'properties': {'user_id': 1001, 'keyword_id': 1001,
                                   'description': '@Misc{jorge2017book1,\nauthor = {Jorge},\ntitle = {Book1},\nhowpublished = {\\url{http://www.link.org/}},\nnote = {Accessed on 01/01/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'keyword',
                    'properties': {'user_id': 1001, 'keyword_id': 1002,
                                   'description': '@Misc{ana2017article2,\nauthor = {Ana},\ntitle = {Article2},\nhowpublished = {\\url{http://www.myhost.org/}},\nnote = {Accessed on 05/02/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'keyword',
                    'properties': {'user_id': 1001, 'keyword_id': 1005, 'description': '@Misc{marco2017articleB,\nauthor = {Marco},\ntitle = {ArticleB},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'keyword',
                    'properties': {'user_id': 1001, 'keyword_id': 1050, 'description': 'BookA'}
                }
            ]
        }

        self.tester.api_keyword(expected, user_id="1001")

    def test_get_api_keyword_return_keyword_by_description(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'keyword',
                    'properties': {'user_id': 1001, 'keyword_id': 1005, 'description': '@Misc{marco2017articleB,\nauthor = {Marco},\ntitle = {ArticleB},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'keyword',
                    'properties': {'user_id': 1005, 'keyword_id': 1010,
                                   'description': '@Misc{marco2017articleC,\nauthor = {Marco},\ntitle = {ArticleC},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}'}
                }
            ]
        }

        self.tester.api_keyword(expected, description="marco")

    # keyword - create and delete

    def test_api_keyword_create_and_delete(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # create a keyword
        resource = {
            'type': 'keyword',
            'properties': {'description': 'ArticleA'}
        }
        resource = self.tester.api_keyword_create(resource)

        # get the id of layer to REMOVE it
        resource_id = resource["properties"]["keyword_id"]

        # remove the resource
        self.tester.api_keyword_delete(resource_id)

        # it is not possible to find the resource that just deleted
        self.tester.api_keyword_error_404_not_found(keyword_id=resource_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()
"""

"""
class TestAPIKeywordErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # keyword errors - get

    def test_get_api_keyword_error_400_bad_request(self):
        self.tester.api_keyword_error_400_bad_request(keyword_id="abc")
        self.tester.api_keyword_error_400_bad_request(keyword_id=0)
        self.tester.api_keyword_error_400_bad_request(keyword_id=-1)
        self.tester.api_keyword_error_400_bad_request(keyword_id="-1")
        self.tester.api_keyword_error_400_bad_request(keyword_id="0")

        self.tester.api_keyword_error_400_bad_request(user_id="abc")
        self.tester.api_keyword_error_400_bad_request(user_id=0)
        self.tester.api_keyword_error_400_bad_request(user_id=-1)
        self.tester.api_keyword_error_400_bad_request(user_id="-1")
        self.tester.api_keyword_error_400_bad_request(user_id="0")

    def test_get_api_keyword_error_404_not_found(self):
        self.tester.api_keyword_error_404_not_found(keyword_id="999")
        self.tester.api_keyword_error_404_not_found(keyword_id="998")

        self.tester.api_keyword_error_404_not_found(user_id="999")
        self.tester.api_keyword_error_404_not_found(user_id="998")

    # keyword errors - create
    
    def test_put_api_keyword_create_error_400_bad_request_attribute_already_exist(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # create a layer
        resource = {
            'type': 'keyword',
            'properties': {'description': 'ArticleA'}
        }
        resource = self.tester.api_keyword_create(resource)

        # get the id of layer to REMOVE it
        resource_id = resource["properties"]["keyword_id"]

        ##################################################
        # try to insert the keyword again, raising the 400
        ##################################################
        self.tester.api_keyword_create_error_400_bad_request(resource)

        # remove the resource after the tests
        self.tester.api_keyword_delete(resource_id)

        # it is not possible to find the resource that just deleted
        self.tester.api_keyword_error_404_not_found(keyword_id=resource_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_keyword_create_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a layer (without description)
        resource = {
            'type': 'keyword',
            'properties': {}
        }
        self.tester.api_keyword_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_keyword_create_error_401_unauthorized(self):
        feature = {
            'properties': {'description': 'BookA'},
            'type': 'keyword'
        }
        self.tester.api_keyword_create_error_401_unauthorized(feature)

    # keyword errors - delete

    def test_delete_api_keyword_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_keyword_delete_error_400_bad_request("abc")
        self.tester.api_keyword_delete_error_400_bad_request(0)
        self.tester.api_keyword_delete_error_400_bad_request(-1)
        self.tester.api_keyword_delete_error_400_bad_request("-1")
        self.tester.api_keyword_delete_error_400_bad_request("0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_keyword_error_401_unauthorized_user_without_login(self):
        self.tester.api_keyword_delete_error_401_unauthorized("abc")
        self.tester.api_keyword_delete_error_401_unauthorized(0)
        self.tester.api_keyword_delete_error_401_unauthorized(-1)
        self.tester.api_keyword_delete_error_401_unauthorized("-1")
        self.tester.api_keyword_delete_error_401_unauthorized("0")
        self.tester.api_keyword_delete_error_401_unauthorized("1001")

    def test_delete_api_keyword_error_403_forbidden_user_forbidden_to_delete(self):
        ########################################
        # create a keyword with user admin
        ########################################

        self.tester.auth_login("admin@admin.com", "admin")

        # create a layer
        resource = {
            'type': 'keyword',
            'properties': {'description': 'ArticleA'}
        }
        resource = self.tester.api_keyword_create(resource)

        # logout with admin
        self.tester.auth_logout()

        ########################################
        # try to delete the keyword with user rodrigo
        ########################################
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # get the id of layer to REMOVE it
        resource_id = resource["properties"]["keyword_id"]

        # TRY TO REMOVE THE LAYER
        self.tester.api_keyword_delete_error_403_forbidden(resource_id)

        # logout with user rodrigo
        self.tester.auth_logout()

        ########################################
        # really delete the layer with user admin
        ########################################
        self.tester.auth_login("admin@admin.com", "admin")

        # delete the layer
        self.tester.api_keyword_delete(resource_id)

        # it is not possible to find the layer that just deleted
        self.tester.api_keyword_error_404_not_found(keyword_id=resource_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_keyword_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_keyword_delete_error_404_not_found("5000")
        self.tester.api_keyword_delete_error_404_not_found("5001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()
"""

# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
