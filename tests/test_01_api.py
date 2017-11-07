#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from json import loads, dumps
from requests import get

from util.tester import UtilTester


# TODO: create cases of test:
# TODO: DELETE A ELEMENT WITH ID THAT DOESN'T EXIST


class TestAPI(TestCase):

    def test_get_api_create_changeset_without_login(self):
        # do a GET call
        response = get('http://localhost:8888/api/changeset/create/')

        self.assertEqual(response.status_code, 403)

        expected = {'status': 403, 'statusText': 'It needs a user looged to access this URL'}
        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(expected, resulted)

    def test_get_api_create_changeset_with_login(self):
        # create a tester passing the unittest self
        tester = UtilTester(self)

        # DO LOGIN
        tester.do_login()

        # CREATE A CHANGESET
        changeset = tester.create_a_changeset()

        # get the id of changeset to use
        fk_id_changeset = changeset["plc"]["changeset"]["properties"]["id"]

        # ADD ELEMENTS
        node = tester.add_a_node(fk_id_changeset)
        way = tester.add_a_way(fk_id_changeset)
        area = tester.add_a_area(fk_id_changeset)

        # SEARCH IN DB, IF THE ELEMENTS EXIST

        id_element = node["features"][0]["properties"]["id"]  # get the id of element

        # do a GET call with default format (GeoJSON)
        response = tester.session.get('http://localhost:8888/api/node/?q=[id={0}]'.format(id_element))

        self.assertTrue(response.ok)
        self.assertEqual(response.status_code, 200)

        resulted = loads(response.text)  # convert string to dict/JSON

        self.assertEqual(node, resulted)



        # REMOVE THE ELEMENTS CREATED
        id_element = node["features"][0]["properties"]["id"]  # get the id of element
        tester.delete_element("node", id_element)

        id_element = way["features"][0]["properties"]["id"]
        tester.delete_element("way", id_element)

        id_element = area["features"][0]["properties"]["id"]
        tester.delete_element("area", id_element)

        # CLOSE THE CHANGESET
        tester.close_a_changeset(fk_id_changeset)

        # DO LOGOUT
        tester.do_logout()

        ################################################################################
        # TRY TO CREATE ANOTHER CHANGESET WITHOUT LOGIN
        ################################################################################

        # do a GET call, sending a changeset to add in DB
        response = tester.session.get('http://localhost:8888/api/changeset/create/',
                                      data=dumps(changeset), headers=tester.headers)

        # it is not possible to create a changeset without login, so get a 403 Forbidden
        self.assertEqual(response.status_code, 403)




# TODO: create a test to remove the elements added


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
