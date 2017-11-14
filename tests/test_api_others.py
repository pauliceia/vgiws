#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/


class TestAPIOthers(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_get_api_capabilities(self):
        self.tester.api_capabilities()


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
