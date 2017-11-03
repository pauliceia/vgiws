#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from json import loads
from requests import get

#
# class TestAPI(TestCase):
#
#     def test_get_api_node_return_all_elements_as_wkt(self):
#         # do a GET call
#         response = get('http://localhost:8888/api/changeset/create/')
#
#         self.assertTrue(response.ok)
#         self.assertEqual(response.status_code, 200)
#
#         resulted = loads(response.text)  # convert string to dict/JSON
#
#         print("resulted: ", resulted)
#
#         self.assertIn("id_changeset", resulted)



# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
