#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from requests import get, post, put, delete


class TestInvalidURLs(TestCase):

    def test_invalid_urls(self):
        response = get('http://localhost:8888/api/referencce')

        self.assertEqual(response.status_code, 404)

        response = post('http://localhost:8888/api/layyer/create/')

        self.assertEqual(response.status_code, 404)

        response = put('http://localhost:8888/apii/user')

        self.assertEqual(response.status_code, 404)

        response = delete('http://localhost:8888/api/keywoosd/382')

        self.assertEqual(response.status_code, 404)


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
