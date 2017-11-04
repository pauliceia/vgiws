#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from json import loads
from requests import get





class TestInvalidURLs(TestCase):

    def test_invalid_urls(self):
        response = get('http://localhost:8888/api/nodex/create/')

        self.assertEqual(response.status_code, 404)

        response = get('http://localhost:8888/api/element33/')

        self.assertEqual(response.status_code, 404)

        response = get('http://localhost:8888/api/nodi/')

        self.assertEqual(response.status_code, 404)

        response = get('http://localhost:8888/areaa/nodi/')

        self.assertEqual(response.status_code, 404)





class TestAPI(TestCase):

    def test_get_api_create_changeset_without_login(self):
        # do a GET call
        response = get('http://localhost:8888/api/changeset/create/')

        self.assertEqual(response.status_code, 403)

        expected = {'status': 403, 'statusText': 'It needs a user looged to access this URL'}
        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_create_changeset_without_login(self):
        # First: do login
        response = get('http://localhost:8888/auth/login/fake/')

        self.assertEqual(response.status_code, 200)


        # Create a changeset
        response = get('http://localhost:8888/api/changeset/create/')

        self.assertEqual(response.status_code, 403)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertIn("id_changeset", resulted)


        # On the final: do logout

        response = get('http://localhost:8888/auth/logout')

        self.assertEqual(response.status_code, 200)




# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
