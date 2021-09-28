
from util.tester import RequestTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/

class TestAPIKeyword(RequestTester):

    def setUp(self):
        self.set_urn('/api/keyword')

    # keyword - get

    def test__get_api_keyword__return_all_keywords(self):
        expected = {
            "features": [
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1001,
                        "name": "generic",
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1001
                    }
                },
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1002,
                        "name": "event",
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1001
                    }
                },
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1003,
                        "name": "crime",
                        "username": "rodrigo",
                        "user_name": "Rodrigo",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1002
                    }
                },
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1004,
                        "name": "assault",
                        "username": "rodrigo",
                        "user_name": "Rodrigo",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1002
                    }
                },
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1005,
                        "name": "robbery",
                        "username": "rodrigo",
                        "user_name": "Rodrigo",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1002
                    }
                },
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1010,
                        "name": "disease",
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1001
                    }
                },
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1020,
                        "name": "object",
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1001
                    }
                },
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1021,
                        "name": "building",
                        "username": "miguel",
                        "user_name": "Miguel",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1003
                    }
                },
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1022,
                        "name": "school",
                        "username": "miguel",
                        "user_name": "Miguel",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1003
                    }
                },
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1023,
                        "name": "hospital",
                        "username": "miguel",
                        "user_name": "Miguel",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1003
                    }
                },
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1030,
                        "name": "cultural place",
                        "username": "miguel",
                        "user_name": "Miguel",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1003
                    }
                },
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1031,
                        "name": "cinema",
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1001
                    }
                },
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1040,
                        "name": "street",
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1001
                    }
                },
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1041,
                        "name": "address",
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1001
                    }
                }
            ],
            "type": "FeatureCollection"
        }

        self.get(expected)

    def test__get_api_keyword__return_keyword_by_keyword_id(self):
        expected = {
            'features': [
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1003,
                        "name": "crime",
                        "username": "rodrigo",
                        "user_name": "Rodrigo",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1002
                    }
                },
            ],
            'type': 'FeatureCollection'
        }

        self.get(expected, id="1003")

    def test__get_api_keyword__return_keyword_by_user_id_creator(self):
        expected = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1001,
                        "name": "generic",
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1001
                    }
                },
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1002,
                        "name": "event",
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1001
                    }
                },
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1010,
                        "name": "disease",
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1001
                    }
                },
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1020,
                        "name": "object",
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1001
                    }
                },
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1031,
                        "name": "cinema",
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1001
                    }
                },
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1040,
                        "name": "street",
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1001
                    }
                },
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1041,
                        "name": "address",
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1001
                    }
                }
            ]
        }

        self.get(expected, user_id_creator="1001")

    def test__get_api_keyword__return_keyword_by_name(self):
        expected = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1004,
                        "name": "assault",
                        "username": "rodrigo",
                        "user_name": "Rodrigo",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1002
                    }
                },
                {
                    "type": "Keyword",
                    "properties": {
                        "id": 1010,
                        "name": "disease",
                        "username": "admin",
                        "user_name": "Administrator",
                        "created_at": "2017-01-01 00:00:00",
                        "user_id_creator": 1001
                    }
                }
            ]
        }

        self.get(expected, name="As")

    def test__get_api_keyword__return_zero_resources(self):
        expected = {'features': [], 'type': 'FeatureCollection'}

        self.get(expected, id="999")
        self.get(expected, id="998")

        self.get(expected, user_id_creator="999")
        self.get(expected, user_id_creator="998")

    # keyword - create, update and delete

    def test__api_keyword_create_but_update_and_delete_with_admin_user(self):
        self.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # create a keyword with user gabriel
        ##################################################
        resource = {
            'properties': {'id': -1, 'name': 'newkeyword'},
            'type': 'Keyword'
        }
        keyword_id = self.post(resource, add_suffix_to_uri="/create")
        resource["properties"]["id"] = keyword_id

        # logout with gabriel and login with admin user
        self.auth_logout()
        self.auth_login("admin@admin.com", "admin")

        ##################################################
        # update the keyword with admin
        ##################################################
        resource["properties"]["name"] = "newname"
        self.put(resource)

        ##################################################
        # check if the resource was modified
        ##################################################
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.get(expected_at_least=expected_resource, id=keyword_id)

        ##################################################
        # remove the keyword with admin
        ##################################################
        # remove the resource
        self.delete(argument=keyword_id)

        # it is not possible to find the resource that just deleted
        expected = {'features': [], 'type': 'FeatureCollection'}
        self.get(expected, id=keyword_id)

        self.auth_logout()


class TestAPIKeywordErrors(RequestTester):

    def setUp(self):
        self.set_urn('/api/keyword')

    # keyword errors - get

    def test__get_api_keyword__400_bad_request(self):
        expected = {
            "status_code": 400,
            "expected_text": "Invalid parameter."
        }

        for item in ["abc", 0, -1, "-1", "0"]:
            self.get(id=item, **expected)
            self.get(user_id_creator=item, **expected)

        # invalid argument
        self.get(
            parent_id=1001, status_code=400,
            expected_text="TypeError: get_keywords() got an unexpected keyword argument 'parent_id'"
        )
        self.get(
            usee_id=1001, status_code=400,
            expected_text="TypeError: get_keywords() got an unexpected keyword argument 'usee_id'"
        )
        self.get(
            keyboard_id=1001, status_code=400,
            expected_text="TypeError: get_keywords() got an unexpected keyword argument 'keyboard_id'"
        )

    # keyword errors - create

    def test__post_api_keyword__400_bad_request__attribute_already_exist(self):
        self.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a keyword with a name that already exist
        resource = {
            'properties': {'name': 'event'},
            'type': 'Keyword'
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=400,
            expected_text="Attribute already exists. (error: Key (name)=(event) already exists.)"
        )

        self.auth_logout()

    def test__post_api_keyword__400_bad_request__attribute_in_JSON_is_missing(self):
        self.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a layer (without name)
        resource = {
            'properties': {},
            'type': 'Keyword'
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=400,
            expected_text=("Some attribute in the JSON is missing. "
                           "Look at the documentation! (error: 'name' is missing)")
        )

        self.auth_logout()

    def test__post_api_keyword__401_unauthorized(self):
        resource = {
            'properties': {'id': -1, 'name': 'newkeyword'},
            'type': 'Keyword'
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=401,
            expected_text="A valid `Authorization` header is necessary!"
        )

    # keyword errors - update

    def test__put_api_keyword__400_bad_request__attribute_already_exist(self):
        self.auth_login("rodrigo@admin.com", "rodrigo")

        ##################################################
        # try to update the keyword with a name that already exist, raising the 400
        ##################################################
        resource = {
            'properties': {'id': 1003, 'name': 'street'},
            'type': 'Keyword'
        }
        self.put(
            resource, status_code=400,
            expected_text="Attribute already exists. (error: Key (name)=(street) already exists.)"
        )

        self.auth_logout()

    def test__put_api_keyword__400_bad_request__attribute_in_JSON_is_missing(self):
        self.auth_login("rodrigo@admin.com", "rodrigo")

        # try to update the keyword without a keyword_id, raising the 400
        resource = {
            'properties': {'name': 'newkeyword'},
            'type': 'Keyword'
        }
        self.put(
            resource, status_code=400,
            expected_text=("Some attribute in the JSON is missing. "
                           "Look at the documentation! (error: 'id' is missing)")
        )

        # try to update the keyword without a name, raising the 400
        resource = {
            'properties': {'id': 1003},
            'type': 'Keyword'
        }
        self.put(
            resource, status_code=400,
            expected_text=("Some attribute in the JSON is missing. "
                           "Look at the documentation! (error: 'name' is missing)")
        )

        self.auth_logout()

    def test__put_api_keyword__401_unauthorized(self):
        resource = {
            'properties': {'id': 1001, 'name': 'newkeyword'},
            'type': 'Keyword'
        }
        self.put(
            resource, status_code=401,
            expected_text="A valid `Authorization` header is necessary!"
        )

    def test__put_api_keyword__403_forbidden(self):
        self.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # gabriel tries to update one keyword that doesn't belong to him
        ##################################################
        resource = {
            'properties': {'id': 1003, 'name': 'street'},
            'type': 'Keyword'
        }
        self.put(
            resource, status_code=403,
            expected_text="The administrator is who can update/delete the keyword."
        )

        self.auth_logout()

    def test__put_api_keyword__404_not_found(self):
        self.auth_login("admin@admin.com", "admin")

        resource = {
            'properties': {'id': 999, 'name': 'street'},
            'type': 'Keyword'
        }
        self.put(
            resource, status_code=404,
            expected_text="Not found any resource."
        )

        self.auth_logout()

    # keyword errors - delete

    def test__delete_api_keyword__400_bad_request(self):
        self.auth_login("rodrigo@admin.com", "rodrigo")

        for item in ["abc", 0, -1, "-1", "0"]:
            self.delete(argument=item, status_code=400, expected_text="Invalid parameter.")

        self.auth_logout()

    def test__delete_api_keyword__401_unauthorized(self):
        for item in ["abc", 0, -1, "-1", "0", "1001"]:
            self.delete(
                param=item, status_code=401,
                expected_text="A valid `Authorization` header is necessary!"
            )

    def test__delete_api_keyword__403_forbidden(self):
        self.auth_login("miguel@admin.com", "miguel")

        ########################################
        # try to delete the keyword with user miguel
        ########################################
        self.delete(
            param=1001, status_code=403,
            expected_text="The administrator is who can update/delete the keyword."
        )

        self.auth_logout()

    def test__delete_api_keyword__404_not_found(self):
        self.auth_login("rodrigo@admin.com", "rodrigo")

        for item in [5000, 5001]:
            self.delete(argument=item, status_code=404, expected_text="Not found any resource.")

        self.auth_logout()


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
