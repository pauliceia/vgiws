#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


class TestAPITheme(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # theme tree - get

    def test_get_api_theme_tree_return_theme_tree(self):
        expected = {
            'columns': ['value'],
            'data': [
                [
                    {
                        'key': 'generic', '_id': 0, '_type': 'Theme',
                        'can_be': [
                            {
                                'key': 'cultural_place', '_id': 1, '_type': 'Theme',
                                'can_be': [{'key': 'theater', '_id': 2, '_type': 'Theme'},
                                           {'key': 'cinema', '_id': 3, '_type': 'Theme'}]
                            },
                            {
                                'key': 'crime', '_id': 4, '_type': 'Theme',
                                'can_be': [{'key': 'assalt', '_id': 5, '_type': 'Theme'},
                                           {'key': 'robbery', '_id': 6, '_type': 'Theme'}]
                            },
                            {
                                'key': 'building', '_id': 7, '_type': 'Theme',
                                'can_be': [{'key': 'school', '_id': 8, '_type': 'Theme'},
                                           {'key': 'hospital', '_id': 9, '_type': 'Theme'}],
                            }
                        ]
                    }
                ]
            ]
        }

        self.tester.api_theme_tree(expected)
