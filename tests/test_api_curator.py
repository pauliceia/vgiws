# -*- coding: utf-8 -*-

from util.tester import RequestTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/


class TestAPICurator(RequestTester):

    def setUp(self):
        self.set_urn('/api/curator')

    # curator - get

    def test__get_api_curator__return_all_curators(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'created_at': '2018-01-01 00:00:00', 'keyword_id': 1001,
                                   'user_id': 1001, 'region': 'amaro'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-01-10 00:00:00', 'keyword_id': 1002,
                                   'user_id': 1001, 'region': 'azure'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-01-10 00:00:00', 'keyword_id': 1002,
                                   'user_id': 1002, 'region': 'belondres'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-02-22 00:00:00', 'keyword_id': 1010,
                                   'user_id': 1003, 'region': 'jorge'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-01-15 00:00:00', 'keyword_id': 1020,
                                   'user_id': 1003, 'region': 'centro'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-02-20 00:00:00', 'keyword_id': 1003,
                                   'user_id': 1004, 'region': 'são francisco'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-02-22 00:00:00', 'keyword_id': 1010,
                                   'user_id': 1005, 'region': 'são bento'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-03-24 00:00:00', 'keyword_id': 1021,
                                   'user_id': 1006, 'region': 'avenida rodônia'},
                    'type': 'Curator'
                }
            ]
        }

        self.get(expected)

    def test__get_api_curator__return_curator_by_user_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'created_at': '2018-02-22 00:00:00', 'keyword_id': 1010,
                                   'user_id': 1003, 'region': 'jorge'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-01-15 00:00:00', 'keyword_id': 1020,
                                   'user_id': 1003, 'region': 'centro'},
                    'type': 'Curator'
                }
            ]
        }

        self.get(expected, user_id="1003")

    def test__get_api_curator__return_curator_by_keyword_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'created_at': '2018-01-10 00:00:00', 'keyword_id': 1002,
                                   'user_id': 1001, 'region': 'azure'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-01-10 00:00:00', 'keyword_id': 1002,
                                   'user_id': 1002, 'region': 'belondres'},
                    'type': 'Curator'
                }
            ]
        }

        self.get(expected, keyword_id="1002")

    def test__get_api_curator__return_curator_by_region(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'created_at': '2018-02-20 00:00:00', 'keyword_id': 1003,
                                   'user_id': 1004, 'region': 'são francisco'},
                    'type': 'Curator'
                },
                {
                    'properties': {'created_at': '2018-02-22 00:00:00', 'keyword_id': 1010,
                                   'user_id': 1005, 'region': 'são bento'},
                    'type': 'Curator'
                }
            ]
        }

        self.get(expected, region="SÃo")

    def test__get_api_curator__return_curator_by_user_id_and_keyword_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'created_at': '2018-01-10 00:00:00', 'keyword_id': 1002,
                                   'user_id': 1002, 'region': 'belondres'},
                    'type': 'Curator'
                }
            ]
        }

        self.get(expected, user_id="1002", keyword_id="1002")

    def test__get_api_curator__return_zero_resources(self):
        expected = {'type': 'FeatureCollection', 'features': []}

        self.get(expected, keyword_id="999")
        self.get(expected, keyword_id="998")

        self.get(expected, user_id="999")
        self.get(expected, user_id="998")

    # curator - create, update and delete

    def test__api_curator__create_update_and_delete(self):
        # DO LOGIN
        self.auth_login("rodrigo@admin.com", "rodrigo")

        ##################################################
        # create curator
        ##################################################
        resource = {
            'properties': {'user_id': 1002, 'keyword_id': 1003, 'region': 'jorge'},
            'type': 'Curator'
        }
        self.post(resource, add_suffix_to_uri="/create")

        ##################################################
        # update curator
        ##################################################
        resource["properties"]["region"] = "cabral"
        self.put(resource)

        ##################################################
        # check if the resource was modified
        ##################################################
        p = resource["properties"]
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.get(expected_at_least=expected_resource, user_id=p["user_id"], keyword_id=p["keyword_id"])

        ##################################################
        # remove curator
        ##################################################
        # get the id of layer to REMOVE it
        user_id = resource["properties"]["user_id"]
        keyword_id = resource["properties"]["keyword_id"]

        # remove the user in layer
        self.delete(user_id=user_id, keyword_id=keyword_id)

        # it is not possible to find the layer that just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.get(expected, user_id=user_id, keyword_id=keyword_id)

        # DO LOGOUT AFTER THE TESTS
        self.auth_logout()


class TestAPIUserCuratorErrors(RequestTester):

    def setUp(self):
        self.set_urn('/api/curator')

    # curator errors - get

    def test__get_api_curator__error__400_bad_request__invalid_parameter(self):
        expected = {
            "status_code": 400,
            "expected_text": "Invalid parameter."
        }

        self.get(keyword_id="abc", **expected)
        self.get(keyword_id=0, **expected)
        self.get(keyword_id=-1, **expected)
        self.get(keyword_id="-1", **expected)
        self.get(keyword_id="0", **expected)

        self.get(user_id="abc", **expected)
        self.get(user_id=0, **expected)
        self.get(user_id=-1, **expected)
        self.get(user_id="-1", **expected)
        self.get(user_id="0", **expected)

    # curator errors - create

    def test__post_api_curator__create__error__400_bad_request__attribute_already_exist(self):
        # DO LOGIN
        self.auth_login("rodrigo@admin.com", "rodrigo")

        # try to insert a curator with 'user_id' and 'keyword_id' that already exist
        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 1010, 'region': 'joana'},
            'type': 'Curator'
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=400,
            expected_text="Attribute already exists. (error: Key (user_id, keyword_id)=(1003, 1010) already exists.)"
        )

        # DO LOGOUT AFTER THE TESTS
        self.auth_logout()

    def test__post_api_curator__create__error__400_bad_request__attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a curator without 'user_id' property
        resource = {
            'properties': {'keyword_id': 1010, 'region': 'joana'},
            'type': 'Curator'
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=400,
            expected_text="Some attribute in the JSON is missing. Look at the documentation! (error: 'user_id' is missing)"
        )

        # try to create a curator without 'keyword_id' property
        resource = {
            'properties': {'user_id': 1003, 'region': 'joana'},
            'type': 'Curator'
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=400,
            expected_text="Some attribute in the JSON is missing. Look at the documentation! (error: 'keyword_id' is missing)"
        )

        # try to create a curator without 'region' property
        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 1010},
            'type': 'Curator'
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=400,
            expected_text="Some attribute in the JSON is missing. Look at the documentation! (error: 'region' is missing)"
        )

        # DO LOGOUT AFTER THE TESTS
        self.auth_logout()

    def test__post_api_curator__create__error__401_unauthorized__without_authorization_header(self):
        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 1010, 'region': 'joana'},
            'type': 'Curator'
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=401,
            expected_text="A valid `Authorization` header is necessary!"
        )

    def test__post_api_curator__create__error__403_forbidden__invalid_user_tries_to_manage_a_curator(self):
        # DO LOGIN
        self.auth_login("miguel@admin.com", "miguel")

        # add a user in a layer
        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 1010, 'region': 'joana'},
            'type': 'Curator'
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=403,
            expected_text="The administrator is who can manage a curator."
        )

        # DO LOGOUT AFTER THE TESTS
        self.auth_logout()

    # curator errors - update

    def test__put__api_curator__error__400_bad_request__attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a curator without 'user_id' property
        resource = {
            'properties': {'keyword_id': 1010, 'region': 'joana'},
            'type': 'Curator'
        }
        self.put(
            resource, status_code=400,
            expected_text="Some attribute in the JSON is missing. Look at the documentation! (error: 'user_id' is missing)"
        )

        # try to create a curator (without 'keyword_id' property
        resource = {
            'properties': {'user_id': 1003, 'region': 'joana'},
            'type': 'Curator'
        }
        self.put(
            resource, status_code=400,
            expected_text="Some attribute in the JSON is missing. Look at the documentation! (error: 'keyword_id' is missing)"
        )

        # try to create a curator (without 'region' property
        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 1010},
            'type': 'Curator'
        }
        self.put(
            resource, status_code=400,
            expected_text="Some attribute in the JSON is missing. Look at the documentation! (error: 'region' is missing)"
        )

        # DO LOGOUT AFTER THE TESTS
        self.auth_logout()

    def test__put__api_curator__error__401_unauthorized__without_authorization_header(self):
        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 1010, 'region': 'joana'},
            'type': 'Curator'
        }
        self.put(
            resource, status_code=401,
            expected_text="A valid `Authorization` header is necessary!"
        )

    def test__put__api_curator__error__403_forbidden__invalid_user_tries_to_manage_a_curator(self):
        # DO LOGIN
        self.auth_login("miguel@admin.com", "miguel")

        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 1010, 'region': 'joana'},
            'type': 'Curator'
        }
        self.put(
            resource, status_code=403,
            expected_text="The administrator is who can manage a curator."
        )

        # DO LOGOUT AFTER THE TESTS
        self.auth_logout()

    def test__put__api_curator__error__404_not_found__not_found_any_resource(self):
        # DO LOGIN
        self.auth_login("admin@admin.com", "admin")

        # try to update with an invalid 'user_id' property
        resource = {
            'properties': {'user_id': 999, 'keyword_id': 1010, 'region': 'joana'},
            'type': 'Curator'
        }
        self.put(resource, status_code=404, expected_text="Not found any resource.")

        # try to update with an invalid 'keyword_id' property
        resource = {
            'properties': {'user_id': 1003, 'keyword_id': 999, 'region': 'joana'},
            'type': 'Curator'
        }
        self.put(resource, status_code=404, expected_text="Not found any resource.")

        # try to update with an invalid 'user_id' and 'keyword_id' properties
        resource = {
            'properties': {'user_id': 999, 'keyword_id': 999, 'region': 'joana'},
            'type': 'Curator'
        }
        self.put(resource, status_code=404, expected_text="Not found any resource.")

        # DO LOGOUT AFTER THE TESTS
        self.auth_logout()

    # curator errors - delete

    def test__delete__api_curator__error__400_bad_request(self):
        # DO LOGIN
        self.auth_login("rodrigo@admin.com", "rodrigo")

        expected = {
            "status_code": 400,
            "expected_text": "Invalid parameter."
        }

        self.delete(user_id="abc", keyword_id="abc", **expected)
        self.delete(user_id=0, keyword_id=0, **expected)
        self.delete(user_id=-1, keyword_id=-1, **expected)
        self.delete(user_id="-1", keyword_id="-1", **expected)
        self.delete(user_id="0", keyword_id="0", **expected)

        # DO LOGOUT AFTER THE TESTS
        self.auth_logout()

    def test__delete__api_curator__error__401_unauthorized(self):
        expected = {
            "status_code": 401,
            "expected_text": "A valid `Authorization` header is necessary!"
        }

        self.delete(user_id=1001, keyword_id=1001, **expected)
        self.delete(user_id=1001, keyword_id="1001", **expected)
        self.delete(user_id=0, keyword_id=-1, **expected)
        self.delete(user_id="0", keyword_id="-1", **expected)

    def test__delete__api_curator__error__403_forbidden(self):
        # login with a user who is NOT an administrator
        self.auth_login("miguel@admin.com", "miguel")

        # try to remove the user in layer
        self.delete(
            user_id=1001, keyword_id=1001, status_code=403,
            expected_text="The administrator is who can manage a curator."
        )

        # DO LOGOUT AFTER THE TESTS
        self.auth_logout()

    def test__delete__api_curator__error__404_not_found(self):
        # DO LOGIN
        self.auth_login("rodrigo@admin.com", "rodrigo")

        self.delete(
            user_id=1001, keyword_id=5000, status_code=404,
            expected_text="Not found any resource."
        )
        self.delete(
            user_id=5001, keyword_id=1001, status_code=404,
            expected_text="Not found any resource."
        )

        # DO LOGOUT AFTER THE TESTS
        self.auth_logout()


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
