#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from requests import get


class TestInvalidURLs(TestCase):

    def test_invalid_urls(self):
        response = get('http://localhost:8888/api/nodex/create/')

        self.assertEqual(response.status_code, 404)

        response = get('http://localhost:8888/api/element33/abx/')

        self.assertEqual(response.status_code, 404)

        response = get('http://localhost:8888/api/nodi/')

        self.assertEqual(response.status_code, 404)

        response = get('http://localhost:8888/areaa/nodi/')

        self.assertEqual(response.status_code, 404)


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
