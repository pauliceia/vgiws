#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from json import loads
from requests import get





# class TestAPI(TestCase):
#
#     def test(self):
#         # do a GET call
#         response = get('http://localhost:8888/api/changeset/create/')
#
#         response = get('http://localhost:8888/api/element/create/')
#
#         response = get('http://localhost:8888/api/element33/')





# class TestAPI(TestCase):

    # def test_get_api_create_changeset_without_login(self):
    #     # do a GET call
    #     response = get('http://localhost:8888/api/changeset/create/')
    #
    #     self.assertEqual(response.status_code, 400)
    #
    #     expected = {'statusText': 'There is no user logged', 'status': 400}
    #     resulted = loads(response.text)  # convert string to dict/JSON
    #
    #     self.assertEqual(expected, resulted)

    # def test_get_api_node_return_all_elements_as_wkt(self):
    #
    #     # first of all, do login
    #
    #     print("Doing login")
    #     response = get('http://localhost:8888/auth/login/fake/')
    #
    #     print("Doing logout")
    #     response = get('http://localhost:8888/auth/logout')
    #
    #
    #     self.assertEqual(1, 1)


        # do a GET call
        # response = get('http://localhost:8888/api/changeset/create/')
        #
        # self.assertEqual(response.status_code, 200)
        #
        # resulted = loads(response.text)  # convert string to dict/JSON
        #
        # print("resulted: ", resulted)
        #
        # self.assertIn("id_changeset", resulted)



# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
