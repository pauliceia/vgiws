# -*- coding: utf-8 -*-

from util.tester import RequestTester


class TestAPIReference(RequestTester):

    def setUp(self):
        self.set_urn('/api/reference')

    # reference - get

    def test__get_api_reference__return_all_references(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1001, 'reference_id': 1001, 'description': '@Misc{jorge2017book1,\nauthor = {Jorge},\ntitle = {Book1},\nhowpublished = {\\url{http://www.link.org/}},\nnote = {Accessed on 01/01/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1001, 'reference_id': 1002, 'description': '@Misc{ana2017article2,\nauthor = {Ana},\ntitle = {Article2},\nhowpublished = {\\url{http://www.myhost.org/}},\nnote = {Accessed on 05/02/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1001, 'reference_id': 1005, 'description': '@Misc{marco2017articleB,\nauthor = {Marco},\ntitle = {ArticleB},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1005, 'reference_id': 1010, 'description': '@Misc{marco2017articleC,\nauthor = {Marco},\ntitle = {ArticleC},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1007, 'reference_id': 1025, 'description': '@Misc{frisina2017bookZ,\nauthor = {Frisina},\ntitle = {BookZ},\nhowpublished = {\\url{http://www.school.com/}},\nnote = {Accessed on 03/04/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1001, 'reference_id': 1050, 'description': 'BookA'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1002, 'reference_id': 1051, 'description': 'ArticleB'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1003, 'reference_id': 1052, 'description': 'ThesisC'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1003, 'reference_id': 1053, 'description': 'DissertationD'}
                }
            ]
        }

        self.get(expected)

    def test__get_api_reference__return_reference_by_reference_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1001, 'reference_id': 1001,
                                   'description': '@Misc{jorge2017book1,\nauthor = {Jorge},\ntitle = {Book1},\nhowpublished = {\\url{http://www.link.org/}},\nnote = {Accessed on 01/01/2017},\nyear={2017}\n}'}
                }
            ]
        }

        self.get(expected, reference_id="1001")

    def test__get_api_reference__return_reference_by_user_id_creator(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1001, 'reference_id': 1001,
                                   'description': '@Misc{jorge2017book1,\nauthor = {Jorge},\ntitle = {Book1},\nhowpublished = {\\url{http://www.link.org/}},\nnote = {Accessed on 01/01/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1001, 'reference_id': 1002,
                                   'description': '@Misc{ana2017article2,\nauthor = {Ana},\ntitle = {Article2},\nhowpublished = {\\url{http://www.myhost.org/}},\nnote = {Accessed on 05/02/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1001, 'reference_id': 1005, 'description': '@Misc{marco2017articleB,\nauthor = {Marco},\ntitle = {ArticleB},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1001, 'reference_id': 1050, 'description': 'BookA'}
                }
            ]
        }

        self.get(expected, user_id_creator="1001")

    def test__get_api_reference__return_reference_by_description(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1001, 'reference_id': 1005, 'description': '@Misc{marco2017articleB,\nauthor = {Marco},\ntitle = {ArticleB},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}'}
                },
                {
                    'type': 'Reference',
                    'properties': {'user_id_creator': 1005, 'reference_id': 1010,
                                   'description': '@Misc{marco2017articleC,\nauthor = {Marco},\ntitle = {ArticleC},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}'}
                }
            ]
        }

        self.get(expected, description="marco")

    def test__get_api_reference__return_zero_resources(self):
        expected = {'type': 'FeatureCollection', 'features': []}

        self.get(expected, reference_id="999")
        self.get(expected, reference_id="998")

        self.get(expected, user_id_creator="999")
        self.get(expected, user_id_creator="998")

    # reference - create, update and delete

    def test__api_reference_create_update_and_delete(self):
        self.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # create a reference
        ##################################################
        resource = {
            'type': 'Reference',
            'properties': {'description': 'ArticleA'}
        }
        resource_id = self.post(resource, add_suffix_to_uri="/create")
        resource["properties"]["reference_id"] = resource_id

        ##################################################
        # update the reference
        ##################################################
        resource["properties"]["description"] = 'SomeArticleB'
        self.put(resource)

        ##################################################
        # check if the resource was modified
        ##################################################
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.get(expected_at_least=expected_resource, reference_id=resource_id)

        ##################################################
        # remove the reference
        ##################################################
        # remove the resource
        self.delete(argument=resource_id)

        # it is not possible to find the resource that just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.get(expected, reference_id=resource_id)

        self.auth_logout()

    def test__api_reference_create_but_update_and_delete__with_admin_user(self):
        self.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # create a reference
        ##################################################
        resource = {
            'type': 'Reference',
            'properties': {'description': 'ArticleA'}
        }
        resource_id = self.post(resource, add_suffix_to_uri="/create")
        resource["properties"]["reference_id"] = resource_id

        # logout with gabriel and login with admin user
        self.auth_logout()
        self.auth_login("admin@admin.com", "admin")

        ##################################################
        # update the reference
        ##################################################
        resource["properties"]["description"] = 'SomeArticleB'
        self.put(resource)

        ##################################################
        # check if the resource was modified
        ##################################################
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.get(expected_at_least=expected_resource, reference_id=resource_id)

        ##################################################
        # remove the reference
        ##################################################
        # remove the resource
        self.delete(argument=resource_id)

        # it is not possible to find the resource that just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.get(expected, reference_id=resource_id)


        self.auth_logout()


class TestAPIReferenceErrors(RequestTester):

    def setUp(self):
        self.set_urn('/api/reference')

    # reference errors - get

    def test__get_api_reference__400_bad_request(self):
        expected = {
            "status_code": 400,
            "expected_text": "Invalid parameter."
        }

        for item in ["abc", 0, -1, "-1", "0"]:
            self.get(reference_id=item, **expected)
            self.get(user_id_creator=item, **expected)

    # reference errors - create

    # def test__post_api_reference_create___400_bad_request__attribute_already_exist(self):
    #     self.auth_login("rodrigo@admin.com", "rodrigo")
    #
    #     ##################################################
    #     # try to insert one reference that already exist, raising the 400
    #     ##################################################
    #     resource = {
    #         'type': 'Reference',
    #         'properties': {'description': 'BookA'}
    #     }
    #     self.tester.api_reference_create_error_400_bad_request(resource)
    #
    #     self.auth_logout()

    def test__post_api_reference_create__400_bad_request__attribute_in_JSON_is_missing(self):
        self.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a layer (without description)
        resource = {
            'type': 'Reference',
            'properties': {}
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=400,
            expected_text=("Some attribute in the JSON is missing. "
                           "Look at the documentation! (error: 'description' is missing)")
        )

        self.auth_logout()

    def test__post_api_reference_create__401_unauthorized(self):
        resource = {
            'properties': {'description': 'BookA'},
            'type': 'Reference'
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=401,
            expected_text="A valid `Authorization` header is necessary!"
        )

    # reference errors - update

    # def test__put_api_reference__400_bad_request__attribute_already_exist(self):
    #     self.auth_login("rodrigo@admin.com", "rodrigo")
    #
    #     ##################################################
    #     # try to update a reference with a description that already exist, raising the 400
    #     ##################################################
    #     resource = {
    #         'type': 'Reference',
    #         'properties': {'reference_id': 1051, 'description': 'ThesisC'}
    #     }
    #     self.tester.api_reference_update_error_400_bad_request(resource)
    #
    #     self.auth_logout()

    def test__put_api_reference__400_bad_request__attribute_in_JSON_is_missing(self):
        self.auth_login("rodrigo@admin.com", "rodrigo")

        # try to update a layer (without reference_id)
        resource = {
            'type': 'Reference',
            'properties': {'description': 'BookA'}
        }
        self.put(
            resource, status_code=400,
            expected_text=("Some attribute in the JSON is missing. "
                           "Look at the documentation! (error: 'reference_id' is missing)")
        )

        # try to update a layer (without description)
        resource = {
            'type': 'Reference',
            'properties': {'reference_id': 1001}
        }
        self.put(
            resource, status_code=400,
            expected_text=("Some attribute in the JSON is missing. "
                           "Look at the documentation! (error: 'description' is missing)")
        )

        self.auth_logout()

    def test__put_api_reference__401_unauthorized(self):
        resource = {
            'properties': {'reference_id': 1001, 'description': 'BookA'},
            'type': 'Reference'
        }
        self.put(
            resource, status_code=401,
            expected_text="A valid `Authorization` header is necessary!"
        )

    def test__put_api_reference__403_forbidden(self):
        self.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # gabriel tries to update one reference that doesn't belong to him
        ##################################################
        resource = {
            'type': 'Reference',
            'properties': {'reference_id': 1051, 'description': 'SomeArticleB'}
        }
        self.put(
            resource, status_code=403,
            expected_text=("The layer owner or collaborator user, or administrator one "
                           "are who can update or delete a reference.")
        )

        self.auth_logout()

    def test__put_api_reference__404_not_found(self):
        self.auth_login("miguel@admin.com", "miguel")

        resource = {
            'type': 'Reference',
            'properties': {'reference_id': 999, 'description': 'SomeArticleB'}
        }
        self.put(
            resource, status_code=404,
            expected_text="Not found any resource."
        )

        self.auth_logout()

    # reference errors - delete

    def test__delete_api_reference__400_bad_request(self):
        self.auth_login("rodrigo@admin.com", "rodrigo")

        for item in ["abc", 0, -1, "-1", "0"]:
            self.delete(argument=item, status_code=400, expected_text="Invalid parameter.")

        self.auth_logout()

    def test__delete_api_reference__401_unauthorized(self):
        for item in ["abc", 0, -1, "-1", "0", "1001"]:
            self.delete(
                param=item, status_code=401,
                expected_text="A valid `Authorization` header is necessary!"
            )

    def test__delete_api_reference__403_forbidden(self):
        self.auth_login("miguel@admin.com", "miguel")

        # try to delete the reference with an invalid user
        self.delete(
            param=1001, status_code=403,
            expected_text=("The layer owner or collaborator user, or administrator one"
                           " are who can update or delete a reference.")
        )

        self.auth_logout()

    def test__delete_api_reference__404_not_found(self):
        self.auth_login("rodrigo@admin.com", "rodrigo")

        for item in [5000, 5001]:
            self.delete(argument=item, status_code=404, expected_text="Not found any resource.")

        self.auth_logout()


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
