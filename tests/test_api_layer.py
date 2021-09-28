
from unittest import TestCase
from util.tester import UtilTester


class TestAPILayer(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # layer - get

    def test_get_api_layer_return_all_layers(self):
        expected = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Layer",
                    "properties": {
                        "id": 1001,
                        "name": "Addresses in 1869",
                        "keywords": [
                            {
                                "id": 1041,
                                "name": "address"
                            },
                            {
                                "id": 1001,
                                "name": "generic"
                            }
                        ],
                        "created_at": "2017-01-01 00:00:00",
                        "references": [
                            {
                                "id": 1002,
                                "description": "@Misc{ana2017article2,\nauthor = {Ana},\ntitle = {Article2},\nhowpublished = {\\url{http://www.myhost.org/}},\nnote = {Accessed on 05/02/2017},\nyear={2017}\n}"
                            },
                            {
                                "id": 1001,
                                "description": "@Misc{jorge2017book1,\nauthor = {Jorge},\ntitle = {Book1},\nhowpublished = {\\url{http://www.link.org/}},\nnote = {Accessed on 01/01/2017},\nyear={2017}\n}"
                            }
                        ],
                        "description": "",
                        "f_table_name": "layer_1001",
                        "collaborators": [
                            {
                                "id": 1001,
                                "name": "Administrator",
                                "username": "admin",
                                "is_the_creator": True
                            },
                            {
                                "id": 1002,
                                "name": "Rodrigo",
                                "username": "rodrigo",
                                "is_the_creator": False
                            }
                        ],
                        "source_description": ""
                    }
                },
                {
                    "type": "Layer",
                    "properties": {
                        "id": 1002,
                        "name": "Robberies between 1880 to 1900",
                        "keywords": [
                            {
                                "id": 1010,
                                "name": "disease"
                            }
                        ],
                        "created_at": "2017-03-05 00:00:00",
                        "references": [
                            {
                                "id": 1005,
                                "description": "@Misc{marco2017articleB,\nauthor = {Marco},\ntitle = {ArticleB},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}"
                            }
                        ],
                        "description": "",
                        "f_table_name": "layer_1002",
                        "collaborators": [
                            {
                                "id": 1001,
                                "name": "Administrator",
                                "username": "admin",
                                "is_the_creator": True
                            },
                            {
                                "id": 1004,
                                "name": "Rafael",
                                "username": "rafael",
                                "is_the_creator": False
                            }
                        ],
                        "source_description": ""
                    }
                },
                {
                    "type": "Layer",
                    "properties": {
                        "id": 1003,
                        "name": "Streets in 1930",
                        "keywords": [
                            {
                                "id": 1001,
                                "name": "generic"
                            },
                            {
                                "id": 1040,
                                "name": "street"
                            }
                        ],
                        "created_at": "2017-04-10 00:00:00",
                        "references": [
                            {
                                "id": 1010,
                                "description": "@Misc{marco2017articleC,\nauthor = {Marco},\ntitle = {ArticleC},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}"
                            }
                        ],
                        "description": "",
                        "f_table_name": "layer_1003",
                        "collaborators": [
                            {
                                "id": 1001,
                                "name": "Administrator",
                                "username": "admin",
                                "is_the_creator": False
                            },
                            {
                                "id": 1003,
                                "name": "Miguel",
                                "username": "miguel",
                                "is_the_creator": True
                            },
                            {
                                "id": 1006,
                                "name": None,
                                "username": "fernanda",
                                "is_the_creator": False
                            },
                            {
                                "id": 1007,
                                "name": None,
                                "username": "ana",
                                "is_the_creator": False
                            }
                        ],
                        "source_description": ""
                    }
                },
                {
                    "type": "Layer",
                    "properties": {
                        "id": 1004,
                        "name": "Streets in 1920",
                        "keywords": [
                            {
                                "id": 1040,
                                "name": "street"
                            }
                        ],
                        "created_at": "2017-06-15 00:00:00",
                        "references": [],
                        "description": "streets",
                        "f_table_name": "layer_1004",
                        "collaborators": [
                            {
                                "id": 1003,
                                "name": "Miguel",
                                "username": "miguel",
                                "is_the_creator": True
                            },
                            {
                                "id": 1007,
                                "name": None,
                                "username": "ana",
                                "is_the_creator": False
                            },
                            {
                                "id": 1008,
                                "name": None,
                                "username": "bea",
                                "is_the_creator": False
                            }
                        ],
                        "source_description": ""
                    }
                },
                {
                    "type": "Layer",
                    "properties": {
                        "id": 1005,
                        "name": "Hospitals between 1800 to 1950",
                        "keywords": [
                            {
                                "id": 1023,
                                "name": "hospital"
                            }
                        ],
                        "created_at": "2017-08-04 00:00:00",
                        "references": [],
                        "description": "some hospitals",
                        "f_table_name": "layer_1005",
                        "collaborators": [
                            {
                                "id": 1007,
                                "name": None,
                                "username": "ana",
                                "is_the_creator": True
                            }
                        ],
                        "source_description": None
                    }
                },
                {
                    "type": "Layer",
                    "properties": {
                        "id": 1006,
                        "name": "Cinemas between 1900 to 1950",
                        "keywords": [
                            {
                                "id": 1031,
                                "name": "cinema"
                            }
                        ],
                        "created_at": "2017-09-04 00:00:00",
                        "references": [
                            {
                                "id": 1025,
                                "description": "@Misc{frisina2017bookZ,\nauthor = {Frisina},\ntitle = {BookZ},\nhowpublished = {\\url{http://www.school.com/}},\nnote = {Accessed on 03/04/2017},\nyear={2017}\n}"
                            }
                        ],
                        "description": "",
                        "f_table_name": "layer_1006",
                        "collaborators": [
                            {
                                "id": 1007,
                                "name": None,
                                "username": "ana",
                                "is_the_creator": True
                            },
                            {
                                "id": 1008,
                                "name": None,
                                "username": "bea",
                                "is_the_creator": False
                            }
                        ],
                        "source_description": None
                    }
                }
            ]
        }

        self.tester.api_layer(expected)

    def test_get_api_layer_return_layer_by_layer_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    "type": "Layer",
                    "properties": {
                        "id": 1001,
                        "name": "Addresses in 1869",
                        "keywords": [
                            {
                                "id": 1041,
                                "name": "address"
                            },
                            {
                                "id": 1001,
                                "name": "generic"
                            }
                        ],
                        "created_at": "2017-01-01 00:00:00",
                        "references": [
                            {
                                "id": 1002,
                                "description": "@Misc{ana2017article2,\nauthor = {Ana},\ntitle = {Article2},\nhowpublished = {\\url{http://www.myhost.org/}},\nnote = {Accessed on 05/02/2017},\nyear={2017}\n}"
                            },
                            {
                                "id": 1001,
                                "description": "@Misc{jorge2017book1,\nauthor = {Jorge},\ntitle = {Book1},\nhowpublished = {\\url{http://www.link.org/}},\nnote = {Accessed on 01/01/2017},\nyear={2017}\n}"
                            }
                        ],
                        "description": "",
                        "f_table_name": "layer_1001",
                        "collaborators": [
                            {
                                "id": 1001,
                                "name": "Administrator",
                                "username": "admin",
                                "is_the_creator": True
                            },
                            {
                                "id": 1002,
                                "name": "Rodrigo",
                                "username": "rodrigo",
                                "is_the_creator": False
                            }
                        ],
                        "source_description": ""
                    }
                }
            ]
        }

        self.tester.api_layer(expected, id="1001")

    def test_get_api_layer_return_layer_by_f_table_name(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    "type": "Layer",
                    "properties": {
                        "id": 1003,
                        "name": "Streets in 1930",
                        "keywords": [
                            {
                                "id": 1001,
                                "name": "generic"
                            },
                            {
                                "id": 1040,
                                "name": "street"
                            }
                        ],
                        "created_at": "2017-04-10 00:00:00",
                        "references": [
                            {
                                "id": 1010,
                                "description": "@Misc{marco2017articleC,\nauthor = {Marco},\ntitle = {ArticleC},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}"
                            }
                        ],
                        "description": "",
                        "f_table_name": "layer_1003",
                        "collaborators": [
                            {
                                "id": 1001,
                                "name": "Administrator",
                                "username": "admin",
                                "is_the_creator": False
                            },
                            {
                                "id": 1003,
                                "name": "Miguel",
                                "username": "miguel",
                                "is_the_creator": True
                            },
                            {
                                "id": 1006,
                                "name": None,
                                "username": "fernanda",
                                "is_the_creator": False
                            },
                            {
                                "id": 1007,
                                "name": None,
                                "username": "ana",
                                "is_the_creator": False
                            }
                        ],
                        "source_description": ""
                    }
                }
            ]
        }

        self.tester.api_layer(expected, f_table_name="1003")

    def test_get_api_layer_return_layer_by_keyword_id(self):
        expected = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Layer",
                    "properties": {
                        "id": 1001,
                        "name": "Addresses in 1869",
                        "keywords": [
                            {
                                "id": 1041,
                                "name": "address"
                            },
                            {
                                "id": 1001,
                                "name": "generic"
                            }
                        ],
                        "created_at": "2017-01-01 00:00:00",
                        "references": [
                            {
                                "id": 1002,
                                "description": "@Misc{ana2017article2,\nauthor = {Ana},\ntitle = {Article2},\nhowpublished = {\\url{http://www.myhost.org/}},\nnote = {Accessed on 05/02/2017},\nyear={2017}\n}"
                            },
                            {
                                "id": 1001,
                                "description": "@Misc{jorge2017book1,\nauthor = {Jorge},\ntitle = {Book1},\nhowpublished = {\\url{http://www.link.org/}},\nnote = {Accessed on 01/01/2017},\nyear={2017}\n}"
                            }
                        ],
                        "description": "",
                        "f_table_name": "layer_1001",
                        "collaborators": [
                            {
                                "id": 1001,
                                "name": "Administrator",
                                "username": "admin",
                                "is_the_creator": True
                            },
                            {
                                "id": 1002,
                                "name": "Rodrigo",
                                "username": "rodrigo",
                                "is_the_creator": False
                            }
                        ],
                        "source_description": ""
                    }
                },
                {
                    "type": "Layer",
                    "properties": {
                        "id": 1003,
                        "name": "Streets in 1930",
                        "keywords": [
                            {
                                "id": 1001,
                                "name": "generic"
                            },
                            {
                                "id": 1040,
                                "name": "street"
                            }
                        ],
                        "created_at": "2017-04-10 00:00:00",
                        "references": [
                            {
                                "id": 1010,
                                "description": "@Misc{marco2017articleC,\nauthor = {Marco},\ntitle = {ArticleC},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}"
                            }
                        ],
                        "description": "",
                        "f_table_name": "layer_1003",
                        "collaborators": [
                            {
                                "id": 1001,
                                "name": "Administrator",
                                "username": "admin",
                                "is_the_creator": False
                            },
                            {
                                "id": 1003,
                                "name": "Miguel",
                                "username": "miguel",
                                "is_the_creator": True
                            },
                            {
                                "id": 1006,
                                "name": None,
                                "username": "fernanda",
                                "is_the_creator": False
                            },
                            {
                                "id": 1007,
                                "name": None,
                                "username": "ana",
                                "is_the_creator": False
                            }
                        ],
                        "source_description": ""
                    }
                }
            ]
        }

        self.tester.api_layer(expected, keyword_id="1001")

    def test_get_api_layer_return_zero_resources(self):
        expected = {'type': 'FeatureCollection', 'features': []}

        self.tester.api_layer(expected, id="999")
        self.tester.api_layer(expected, id="998")

    # layer - create, update and delete

    def test_api_layer_create_update_and_delete(self):
        ##################################################
        # log in with a normal user
        ##################################################
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # get creator user id
        ##################################################
        user = self.tester.function_api_user_by_token()
        creator_user_id = user["properties"]["id"]

        ##################################################
        # create a layer with a normal user
        ##################################################
        resource = {
            "type": "Layer",
            "properties": {
                "id": -1, "f_table_name": "addresses_1930",
                "name": "Addresses in 1930", "description": "", "source_description": "",
                "collaborators": [
                    {"id": 1001, "name": "Administrator", 'username': 'admin', 'is_the_creator': False},
                    {"id": 1005, "name": "Gabriel", 'username': 'gabriel', 'is_the_creator': False}
                ],
                "keywords": [
                    {"id": 1041, "name": "address"},
                    {"id": 1001, "name": "generic"}
                ],
                "references": [
                    {"id": 1050, "description": "BookA"},
                    {"id": 1052, "description": "ThesisC"}
                ]
            }
        }
        # get the layer id
        resource_id = self.tester.api_layer_create(resource)

        # I add myself as a collaborator user
        resource["properties"]["collaborators"].append(
            {"id": 1003, "name": "Miguel", 'username': 'miguel', 'is_the_creator': True}
        )

        ##################################################
        # creator user updates the layer data
        ##################################################
        resource["properties"]["id"] = resource_id
        resource["properties"]["name"] = "Some addresses"
        resource["properties"]["description"] = "Addresses"
        self.tester.api_layer_update(resource)

        ##################################################
        # user continues updating the layer by adding a collaborator
        ##################################################
        user_id_collaborator = 1004

        user_layer = {
            'properties': {'user_id': user_id_collaborator, 'layer_id': resource_id},
            'type': 'UserLayer'
        }
        self.tester.api_user_layer_create(user_layer)

        # add new collaborator to the list of collaborators
        resource["properties"]["collaborators"].append(
            {"id": user_id_collaborator, "name": "Rafael", 'username': 'rafael', 'is_the_creator': False}
        )

        ##################################################
        # check if the resource was modified in the database
        ##################################################
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.tester.api_layer(expected_at_least=expected_resource, id=resource_id)

        ##################################################
        # check if the creator and collaborator users have started to follow the created layer automatically
        ##################################################
        # creator user
        expected_at_least = {
            'features': [{
                'properties': {'layer_id': resource_id, 'user_id': creator_user_id},
                'type': 'LayerFollower'
            }],
            'type': 'FeatureCollection'
        }
        self.tester.api_layer_follower(expected_at_least=expected_at_least,
                                       user_id=creator_user_id, layer_id=resource_id)

        # collaborator user
        expected_at_least = {
            'features': [{
                'properties': {'layer_id': resource_id, 'user_id': user_id_collaborator},
                'type': 'LayerFollower'
            }],
            'type': 'FeatureCollection'
        }
        self.tester.api_layer_follower(expected_at_least=expected_at_least,
                                       user_id=user_id_collaborator, layer_id=resource_id)

        ##################################################
        # check if the collaborator user can update the layer, but he can not delete it
        ##################################################
        # log in with the collaborator user
        self.tester.auth_logout()
        self.tester.auth_login("rafael@admin.com", "rafael")

        # collaborator user updates the layer
        resource["properties"]["name"] = "New addresses"
        resource["properties"]["description"] = "New addresses"
        self.tester.api_layer_update(resource)

        # collaborator user tries to delete the layer, but a 403 error is raised
        self.tester.api_layer_delete_error_403_forbidden(resource_id)

        ##################################################
        # delete the layer in the final with the creator user
        ##################################################
        # log in the creator user again
        self.tester.auth_logout()
        self.tester.auth_login("miguel@admin.com", "miguel")

        self.tester.api_layer_delete(resource_id)

        ##################################################
        # final validations
        ##################################################

        # finding the layer that just deleted is not possible
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_layer(expected, id=resource_id)

        # finding a user in a layer that just deleted (creator user) is not possible
        expected = {'features': [], 'type': 'FeatureCollection'}
        self.tester.api_user_layer(expected, user_id=creator_user_id, layer_id=resource_id)

        # check if the creator user stopped automatically of following the layer
        expected = {'features': [], 'type': 'FeatureCollection'}
        self.tester.api_layer_follower(expected, user_id=creator_user_id, layer_id=resource_id)

        # finding a user in a layer that just deleted (collaborator user) is not possible
        expected = {'features': [], 'type': 'FeatureCollection'}
        self.tester.api_user_layer(expected, user_id=user_id_collaborator, layer_id=resource_id)

        # check if the collaborator user has stopped automatically of following the layer
        expected = {'features': [], 'type': 'FeatureCollection'}
        self.tester.api_layer_follower(expected, user_id=user_id_collaborator, layer_id=resource_id)

        ##################################################
        # log out the user after the test case be executed
        ##################################################
        self.tester.auth_logout()

    def test_api_layer_create_but_update_and_delete_with_admin(self):
        # login a normal user
        self.tester.auth_login("miguel@admin.com", "miguel")

        f_table_name = 'addresses_1930'

        ##################################################
        # create a layer with a normal user
        ##################################################
        resource = {
            "type": "Layer",
            "properties": {
                "id": -1, "f_table_name": f_table_name,
                "name": "Addresses in 1930", "description": "", "source_description": "",
                "collaborators": [
                    {"id": 1001, "name": "Administrator", 'username': 'admin', 'is_the_creator': False},
                    {"id": 1005, "name": "Gabriel", 'username': 'gabriel', 'is_the_creator': False}
                ],
                "keywords": [
                    {"id": 1041, "name": "address"},
                    {"id": 1001, "name": "generic"}
                ],
                "references": [
                    {"id": 1050, "description": "BookA"},
                    {"id": 1052, "description": "ThesisC"}
                ]
            }
        }
        # get the layer id
        resource_id = self.tester.api_layer_create(resource)

        # I add myself as a collaborator user
        resource["properties"]["collaborators"].append(
            {"id": 1003, "name": "Miguel", 'username': 'miguel', 'is_the_creator': True}
        )

        ##################################################
        # log in with an admin user in order to check if he can update and delete the layer
        ##################################################
        self.tester.auth_logout()
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        ##################################################
        # admin user updates the layer
        ##################################################
        resource["properties"]["id"] = resource_id
        resource["properties"]["name"] = "Some addresses"
        resource["properties"]["description"] = "Addresses"
        self.tester.api_layer_update(resource)

        # check if the resource was modified
        expected_resource = {'type': 'FeatureCollection', 'features': [resource]}
        self.tester.api_layer(expected_at_least=expected_resource, id=resource_id)

        ##################################################
        # admin user deletes the layer
        ##################################################
        self.tester.api_layer_delete(resource_id)

        # finding the layer that just deleted is not possible
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_layer(expected, id=resource_id)

        # log out the admin user
        self.tester.auth_logout()


class TestAPILayerErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # layer errors - get

    def test_get_api_layer_error_400_bad_request(self):
        self.tester.api_layer_error_400_bad_request(id="abc")
        self.tester.api_layer_error_400_bad_request(id=0)
        self.tester.api_layer_error_400_bad_request(id=-1)
        self.tester.api_layer_error_400_bad_request(id="-1")
        self.tester.api_layer_error_400_bad_request(id="0")

    # layer errors - create

    def test_post_api_layer_create_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a layer (without f_table_name)
        resource = {
            'properties': {'description': '', 'name': 'Addresses in 1869', 'references': [1001, 1002],
                           'source_description': '', 'keywords': [1001, 1041],
                           'collaborators': []},
            'type': 'Layer'
        }
        self.tester.api_layer_create_error_400_bad_request(resource)

        # try to create a layer (without name)
        resource = {
            'properties': {'description': '', 'references': [1001, 1002], 'collaborators': [],
                           'f_table_name': 'address', 'source_description': '', 'keywords': [1001, 1041]},
            'type': 'Layer'
        }
        self.tester.api_layer_create_error_400_bad_request(resource)

        # try to create a layer (without description)
        resource = {
            'properties': {'name': 'Addresses in 1869', 'references': [1001, 1002], 'collaborators': [],
                           'f_table_name': 'address', 'source_description': '', 'keywords': [1001, 1041]},
            'type': 'Layer'
        }
        self.tester.api_layer_create_error_400_bad_request(resource)

        # try to create a layer (without source_description)
        resource = {
            'properties': {'description': '', 'name': 'Addresses in 1869', 'references': [1001, 1002],
                           'f_table_name': 'address', 'keywords': [1001, 1041], 'collaborators': []},
            'type': 'Layer'
        }
        self.tester.api_layer_create_error_400_bad_request(resource)

        # try to create a layer (without collaborators)
        resource = {
            'properties': {'description': '', 'name': 'Addresses in 1869', 'references': [1001, 1002],
                           'f_table_name': 'address', 'source_description': '', 'keywords': [1001, 1041]},
            'type': 'Layer'
        }
        self.tester.api_layer_create_error_400_bad_request(resource)

        # try to create a layer (without references)
        resource = {
            'properties': {'description': '', 'name': 'Addresses in 1869', 'collaborators': [],
                           'f_table_name': 'address', 'source_description': '', 'keywords': [1001, 1041]},
            'type': 'Layer'
        }
        self.tester.api_layer_create_error_400_bad_request(resource)

        # try to create a layer (without keywords)
        resource = {
            'properties': {'description': '', 'name': 'Addresses in 1869', 'references': [1001, 1002],
                           'f_table_name': 'address', 'source_description': '', 'collaborators': []},
            'type': 'Layer'
        }
        self.tester.api_layer_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_layer_create_error_400_bad_request_f_table_name_has_special_chars_or_it_starts_with_number(self):
        # DO LOGIN
        self.tester.auth_login('rodrigo@admin.com', 'rodrigo')

        # try to create a layer with invalid f_table_name
        list_invalid_f_table_name = [
            '*)new_layer', 'new_lay+-er', 'new_layer_(/', '837_new_layer', '0_new_layer',
            ' new_layer', 'new_layer ', 'new layer'
        ]

        for invalid_f_table_name in list_invalid_f_table_name:
            resource = {
                'properties': {
                    'f_table_name': invalid_f_table_name, 'description': '', 'name': 'Addresses in 1869',
                    'references': [1001, 1002], 'source_description': '', 'keywords': [1001, 1041],
                    'collaborators': []
                },
                'type': 'Layer'
            }
            self.tester.api_layer_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_layer_create_error__400_bad_request__f_table_name_is_less_than_5_chars(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        resource = {
            'properties': {
                'f_table_name': 'abcd', 'description': '', 'name': 'Addresses in 1869',
                'references': [1001, 1002], 'source_description': '', 'keywords': [1001, 1041],
                'collaborators': []
            },
            'type': 'Layer'
        }
        self.tester.api_layer_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_layer_create_error__400_bad_request__f_table_name_is_greater_than_63_chars(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        resource = {
            'properties': {
                'f_table_name': 'lorem_ipsum_dolor_sit_amet_consectetur_adipiscing_elit__sed_do_e',
                'description': '', 'name': 'Addresses in 1869', 'collaborators': [],
                'references': [1001, 1002], 'source_description': '', 'keywords': [1001, 1041]
            },
            'type': 'Layer'
        }
        self.tester.api_layer_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_layer_create_error_401_unauthorized(self):
        feature = {
            'properties': {'name': 'Addresses in 1869', 'table_name': 'new_layer', 'source': '',
                           'description': '', 'fk_keyword_id': 1041, 'collaborators': []},
            'type': 'Layer'
        }
        self.tester.api_layer_create_error_401_unauthorized(feature)

    def test_post_api_layer_create_error_404_not_found_non_existing_user(self):
        ##################################################
        # fake log in with a non-existing user
        ##################################################
        self.tester.auth_login_non_existing_user()

        ##################################################
        # try to handle the layer with the fake user
        ##################################################
        self.tester.api_layer_create_error_404_not_found({
            'type': 'Layer',
            'properties': {'id': -1, 'f_table_name': 'addresses_1930', 'name': 'Addresses in 1930',
                           'description': '', 'source_description': '', 'collaborators': [],
                           'references': [1050, 1052], 'keywords': [1001, 1041]}
        })

        self.tester.auth_logout()

    def test_post_api_layer_create_error_409_conflict_f_table_name_already_exist_or_reserved_name(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        # try to create a layer with f_table_name that table that already exist or with reserved name
        list_invalid_f_table_name = ["references", "changeset", "spatial_ref_sys", "abort", "access"]

        for invalid_f_table_name in list_invalid_f_table_name:
            resource = {
                'type': 'Layer',
                'properties': {'id': -1, 'f_table_name': invalid_f_table_name, 'name': '',
                               'description': '', 'source_description': '',
                               'references': [], 'keywords': [], 'collaborators': []}
            }
            self.tester.api_layer_create_error_409_conflict(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_layer_create_error_409_conflict_maximum_of_keywords_are_5(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        resource = {
            'type': 'Layer',
            'properties': {'id': -1, 'f_table_name': "new_table", 'name': '',
                           'description': '', 'source_description': '', 'collaborators': [],
                           'references': [], 'keywords': [1001, 1002, 1003, 1004, 1005, 1006]}
        }
        self.tester.api_layer_create_error_409_conflict(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    # layer errors - update

    def test_put_api_layer_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to update a layer (without id)
        resource = {
            'properties': {'f_table_name': 'layer_1003', 'name': 'Streets in 1930',
                           'description': '', 'source_description': '', 'created_at': '2017-04-10 00:00:00',
                           'references': [1010], 'keywords': [1001, 1040],
                           'collaborators': [{'id': 1002, 'name': 'Rodrigo', 'is_the_creator': True}]},
            'type': 'Layer'
        }
        self.tester.api_layer_update_error_400_bad_request(resource)

        # try to update a layer (without name)
        resource = {
            'properties': {'id': 1003, 'f_table_name': 'layer_1003', 'collaborators': [],
                           'description': '', 'source_description': '', 'created_at': '2017-04-10 00:00:00',
                           'references': [1010], 'keywords': [1001, 1040],
                           'collaborators': [{'id': 1002, 'name': 'Rodrigo', 'is_the_creator': True}]},
            'type': 'Layer'
        }
        self.tester.api_layer_update_error_400_bad_request(resource)

        # try to update a layer (without description)
        resource = {
            'properties': {'id': 1003, 'f_table_name': 'layer_1003', 'name': 'Streets in 1930',
                           'source_description': '', 'created_at': '2017-04-10 00:00:00',
                           'references': [1010], 'keywords': [1001, 1040],
                           'collaborators': [{'id': 1002, 'name': 'Rodrigo', 'is_the_creator': True}]},
            'type': 'Layer'
        }
        self.tester.api_layer_update_error_400_bad_request(resource)

        # try to update a layer (without source_description)
        resource = {
            'properties': {'id': 1003, 'f_table_name': 'layer_1003', 'name': 'Streets in 1930',
                           'description': '', 'created_at': '2017-04-10 00:00:00',
                           'references': [1010], 'keywords': [1001, 1040],
                           'collaborators': [{'id': 1002, 'name': 'Rodrigo', 'is_the_creator': True}]},
            'type': 'Layer'
        }
        self.tester.api_layer_update_error_400_bad_request(resource)

        # try to update a layer (without collaborators)
        resource = {
            'properties': {'id': 1003, 'f_table_name': 'layer_1003', 'name': 'Streets in 1930',
                           'description': '', 'source_description': '', 'created_at': '2017-04-10 00:00:00',
                           'keywords': [1001, 1040], 'references': [1010]},
            'type': 'Layer'
        }
        self.tester.api_layer_update_error_400_bad_request(resource)

        # try to update a layer (without references)
        resource = {
            'properties': {'id': 1003, 'f_table_name': 'layer_1003', 'name': 'Streets in 1930',
                           'description': '', 'source_description': '', 'created_at': '2017-04-10 00:00:00',
                           'keywords': [1001, 1040],
                           'collaborators': [{'id': 1002, 'name': 'Rodrigo', 'is_the_creator': True}]},
            'type': 'Layer'
        }
        self.tester.api_layer_update_error_400_bad_request(resource)

        # try to update a layer (without keywords)
        resource = {
            'properties': {'id': 1003, 'f_table_name': 'layer_1003', 'name': 'Streets in 1930',
                           'description': '', 'source_description': '', 'created_at': '2017-04-10 00:00:00',
                           'references': [1010],
                           'collaborators': [{'id': 1002, 'name': 'Rodrigo', 'is_the_creator': True}]},
            'type': 'Layer'
        }
        self.tester.api_layer_update_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_layer_error_401_unauthorized_user_is_not_logged(self):
        feature = {
            'properties': {'reference_id': 1001, 'description': 'BookA'},
            'type': 'Reference'
        }
        self.tester.api_layer_update_error_401_unauthorized(feature)

    def test_put_api_layer_error_403_forbidden_invalid_user_tries_to_manage(self):
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # miguel tries to update one references that doesn't belong to him
        ##################################################
        resource = {
            'properties': {'id': 1001, 'f_table_name': 'layer_1001', 'name': 'Streets in 1930',
                           'description': '', 'source_description': '', 'created_at': '2017-04-10 00:00:00',
                           'references': [1010], 'keywords': [1001, 1040]},
            'type': 'Layer'
        }
        self.tester.api_layer_update_error_403_forbidden(resource)

        self.tester.auth_logout()

    def test_put_api_layer_error_404_not_found_not_found_layer_x(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        resource = {
            'properties': {'id': 999, 'f_table_name': 'layer_1006', 'name': 'Streets in 1930',
                           'description': '', 'source_description': '', 'created_at': '2017-04-10 00:00:00',
                           'references': [1010], 'keywords': [1001, 1040]},
            'type': 'Layer'
        }
        self.tester.api_layer_update_error_404_not_found(resource)

        # DO LOGOUT
        self.tester.auth_logout()

    def test_put_api_layer_error_409_conflict_maximum_of_keywords_are_5(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        resource = {
            'type': 'Layer',
            'properties': {'id': -1, 'f_table_name': "new_table", 'name': '',
                           'description': '', 'source_description': '',
                           'references': [], 'keywords': [1001, 1002, 1003, 1004, 1005, 1006]}
        }
        self.tester.api_layer_update_error_409_conflict(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    # layer errors - delete

    def test_delete_api_layer_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_layer_delete_error_400_bad_request("abc")
        self.tester.api_layer_delete_error_400_bad_request(0)
        self.tester.api_layer_delete_error_400_bad_request(-1)
        self.tester.api_layer_delete_error_400_bad_request("-1")
        self.tester.api_layer_delete_error_400_bad_request("0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_layer_error_401_unauthorized_user_without_login(self):
        self.tester.api_layer_delete_error_401_unauthorized("abc")
        self.tester.api_layer_delete_error_401_unauthorized(0)
        self.tester.api_layer_delete_error_401_unauthorized(-1)
        self.tester.api_layer_delete_error_401_unauthorized("-1")
        self.tester.api_layer_delete_error_401_unauthorized("0")
        self.tester.api_layer_delete_error_401_unauthorized("1001")

    def test_delete_api_layer_error_403_forbidden_user_forbidden_to_delete(self):
        self.tester.auth_login("miguel@admin.com", "miguel")

        ########################################
        # miguel tries to delete a layer that does not belong to him
        ########################################
        self.tester.api_layer_delete_error_403_forbidden(1001)

        self.tester.auth_logout()

    def test_delete_api_layer_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_layer_delete_error_404_not_found("5000")
        self.tester.api_layer_delete_error_404_not_found("5001")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
