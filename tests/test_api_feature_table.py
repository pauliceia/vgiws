from util.tester import RequestTester


class TestAPIFeatureTable(RequestTester):

    def setUp(self):
        self.set_urn('/api/feature_table')

    # feature_table - get

    def test__get_api_feature_table__return_all_feature_tables(self):
        expected = {
            'features': [
                {
                    'type': 'FeatureTable',
                    'f_table_name': 'layer_1001',
                    'properties': {'id': 'integer', 'end_date': 'timestamp without time zone', 'geom': 'geometry',
                                   'address': 'text', 'version': 'integer', 'changeset_id': 'integer',
                                   'start_date': 'timestamp without time zone'},
                    'geometry': {
                        'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
                        'type': 'MULTIPOINT'
                    }
                },
                {
                    'type': 'FeatureTable',
                    'f_table_name': 'layer_1002',
                    'properties': {'id': 'integer', 'end_date': 'text', 'geom': 'geometry', 'address': 'text',
                                   'version': 'integer', 'changeset_id': 'integer',
                                   'start_date': 'timestamp without time zone'},
                    'geometry': {
                        'crs': {'type':'name', 'properties': {'name': 'EPSG:4326'}},
                        'type': 'MULTIPOINT'
                    }
                },
                {
                    'type': 'FeatureTable',
                    'f_table_name': 'layer_1003',
                    'properties': {'name': 'text', 'id': 'integer', 'end_date': 'timestamp without time zone',
                                   'geom': 'geometry', 'version': 'integer', 'changeset_id': 'integer',
                                   'start_date': 'timestamp without time zone'},
                    'geometry': {
                        'crs': {'type':'name', 'properties': {'name': 'EPSG:4326'}},
                        'type': 'MULTILINESTRING'
                    }
                },
                {
                    'type': 'FeatureTable',
                    'f_table_name': 'layer_1004',
                    'properties': {'name': 'text', 'id': 'integer', 'end_date': 'text', 'geom': 'geometry',
                                   'version': 'integer', 'changeset_id': 'integer', 'start_date': 'text'},
                    'geometry': {
                        'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
                        'type': 'MULTILINESTRING'
                    }
                },
                {
                    'type': 'FeatureTable',
                    'f_table_name': 'layer_1005',
                    'properties': {'name': 'text', 'id': 'integer', 'end_date': 'text', 'geom': 'geometry',
                                   'version': 'integer', 'changeset_id': 'integer', 'start_date': 'text'},
                    'geometry': {
                        'crs': {'type': 'name', 'properties':{'name': 'EPSG:4326'}},
                        'type': 'MULTIPOLYGON'
                    }
                },
                {
                    'type': 'FeatureTable',
                    'f_table_name': 'layer_1006',
                    'properties': {'name': 'text', 'id': 'integer', 'end_date': 'integer', 'geom': 'geometry',
                                   'version': 'integer', 'changeset_id': 'integer', 'start_date': 'integer'},
                    'geometry': {
                        'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
                        'type': 'MULTIPOLYGON'
                    }
                }
            ],
            'type': 'FeatureCollection'
        }

        self.get(expected)

    def test__get_api_feature_table__return_feature_table_by_f_table_name(self):
        expected = {
            'features': [
                {
                    'type': 'FeatureTable',
                    'f_table_name': 'layer_1003',
                    'properties': {'name': 'text', 'id': 'integer', 'end_date': 'timestamp without time zone',
                                   'geom': 'geometry', 'version': 'integer', 'changeset_id': 'integer',
                                   'start_date': 'timestamp without time zone'},
                    'geometry': {
                        'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
                        'type': 'MULTILINESTRING'
                    }
                }
            ],
            'type': 'FeatureCollection'
        }

        self.get(expected, f_table_name="1003")

    def test__get_api_feature_table__return_zero_resources(self):
        expected = {'features': [], 'type': 'FeatureCollection'}

        self.get(expected, f_table_name="998")
        self.get(expected, f_table_name="999")

    # feature table - create and update

    def test__api_feature_table_create_and_update(self):
        ####################################################################################################
        # login with a normal user
        ####################################################################################################
        self.auth_login("miguel@admin.com", "miguel")

        f_table_name = 'addresses_1930'

        ##################################################
        # create a layer
        ##################################################
        layer = {
            'type': 'Layer',
            'properties': {'id': -1, 'f_table_name': f_table_name, 'name': 'Addresses in 1930',
                           'description': '', 'source_description': '', 'collaborators': [],
                           "keywords": [{"id": 1041, "name": "address"}],
                           "references": [{"id": 1002, "description": "@Misc{ana2017article2"}]}
        }
        layer_id = self.post(URI='/api/layer/create', body=layer)

        ####################################################################################################

        ##################################################
        # create the feature_table for the layer above
        ##################################################
        feature_table = {
            'type': 'FeatureTable',
            'f_table_name': f_table_name,
            'properties': {'start_date': 'timestamp without time zone',
                           'end_date': 'timestamp without time zone',
                           'address': 'text'},
            'geometry': {
                'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
                'type': 'MULTIPOINT'
            }
        }
        self.post(feature_table, add_suffix_to_uri="/create")

        ##################################################
        # update the feature_table
        ##################################################
        feature_table_column = {
            'f_table_name': f_table_name,
            'column_name': 'name',
            'column_type': 'text',
        }
        self.post(URI="/api/feature_table_column/create", body=feature_table_column)
        self.delete(URI="/api/feature_table_column", f_table_name=f_table_name, column_name="name")

        ##################################################
        # the feature_table is removed automatically when the layer is deleted
        ##################################################

        ####################################################################################################

        ##################################################
        # delete the layer
        ##################################################
        self.delete(argument=layer_id, URI="/api/layer")

        # finding the layer that just deleted is not possible
        expected = {'type': 'FeatureCollection', 'features': []}
        self.get(URI='/api/layer', expected=expected, id=layer_id)

        self.auth_logout()

    def test__api_feature_table_create_and_update__with_collaborator_user(self):
        ####################################################################################################
        # login with a normal user
        ####################################################################################################
        self.auth_login("miguel@admin.com", "miguel")

        f_table_name = 'addresses_1930'

        ##################################################
        # create a layer
        ##################################################
        layer = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': f_table_name, 'name': 'Addresses in 1930',
                           'description': '', 'source_description': '', 'collaborators': [],
                           "keywords": [{"id": 1041, "name": "address"}],
                           "references": [{"id": 1002, "description": "@Misc{ana2017article2"}]}
        }
        layer_id = self.post(URI='/api/layer/create', body=layer)

        ##################################################
        # add a collaborator to the layer above
        ##################################################
        user_id_collaborator = 1004

        user_layer = {
            'properties': {'user_id': user_id_collaborator, 'layer_id': layer_id},
            'type': 'UserLayer'
        }
        self.post(URI='/api/user_layer/create/', body=user_layer)

        ####################################################################################################
        # login with a collaborator user in order to try to create the feature table
        ####################################################################################################
        self.auth_logout()
        self.auth_login("rafael@admin.com", "rafael")

        ##################################################
        # only the creator user can create the feature_table for the layer above
        ##################################################
        feature_table = {
            'type': 'FeatureTable',
            'f_table_name': f_table_name,
            'properties': {'start_date': 'timestamp without time zone', 'end_date': 'timestamp without time zone',
                           'address': 'text'},
            'geometry': {
                'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
                'type': 'MULTIPOINT'
            }
        }
        self.post(
            feature_table, add_suffix_to_uri="/create", status_code=403,
            expected_text="The layer owner or administrator user are who can create or delete this resource."
        )

        ####################################################################################################
        # login with the creator user in order to create the feature table
        ####################################################################################################
        self.auth_logout()
        self.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # create the feature_table for the layer above
        ##################################################
        feature_table = {
            'type': 'FeatureTable',
            'f_table_name': f_table_name,
            'properties': {'start_date': 'timestamp without time zone', 'end_date': 'timestamp without time zone',
                           'address': 'text'},
            'geometry': {
                'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
                'type': 'MULTIPOINT'
            }
        }
        self.post(feature_table, add_suffix_to_uri="/create")

        ####################################################################################################
        # login with a collaborator user again in order to update the feature table
        ####################################################################################################
        self.auth_logout()
        self.auth_login("rafael@admin.com", "rafael")

        ##################################################
        # update the feature_table with the collaborator user
        ##################################################
        feature_table_column = {
            'f_table_name': f_table_name,
            'column_name': 'name',
            'column_type': 'text',
        }
        self.post(URI="/api/feature_table_column/create", body=feature_table_column)
        self.delete(URI="/api/feature_table_column", f_table_name=f_table_name, column_name="name")

        ##################################################
        # the feature_table is removed automatically when the layer is deleted
        ##################################################

        ####################################################################################################
        # login with a normal user again in order to delete the layer
        ####################################################################################################
        self.auth_logout()
        self.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # delete the layer
        ##################################################
        self.delete(argument=layer_id, URI="/api/layer")

        # finding the layer that just deleted is not possible
        expected = {'type': 'FeatureCollection', 'features': []}
        self.get(URI='/api/layer', expected=expected, id=layer_id)

        self.auth_logout()

    def test__api_feature_table_create_and_update__with_admin_user(self):
        ####################################################################################################
        # login with a normal user
        ####################################################################################################
        self.auth_login("miguel@admin.com", "miguel")

        f_table_name = 'addresses_1930'

        ##################################################
        # create a layer
        ##################################################
        layer = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': f_table_name, 'name': 'Addresses in 1930',
                           'description': '', 'source_description': '', 'collaborators': [],
                           "keywords": [{"id": 1041, "name": "address"}],
                           "references": [{"id": 1002, "description": "@Misc{ana2017article2"}]}
        }
        layer_id = self.post(URI='/api/layer/create', body=layer)

        ####################################################################################################

        self.auth_logout()
        self.auth_login("admin@admin.com", "admin")

        ##################################################
        # create the feature_table for the layer above
        ##################################################
        feature_table = {
            'type': 'FeatureTable',
            'f_table_name': f_table_name,
            'properties': {'start_date': 'timestamp without time zone', 'end_date': 'timestamp without time zone',
                           'address': 'text'},
            'geometry': {
                'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
                'type': 'MULTIPOINT'
            }
        }
        self.post(feature_table, add_suffix_to_uri="/create")

        ##################################################
        # update the feature_table
        ##################################################
        feature_table_column = {
            'f_table_name': f_table_name,
            'column_name': 'name',
            'column_type': 'text',
        }
        self.post(URI="/api/feature_table_column/create", body=feature_table_column)
        self.delete(URI="/api/feature_table_column", f_table_name=f_table_name, column_name="name")

        ##################################################
        # the feature_table is automatically removed when delete its layer
        ##################################################

        ####################################################################################################
        # login with a normal user again in order to delete the layer
        ####################################################################################################
        self.auth_logout()
        self.auth_login("miguel@admin.com", "miguel")

        ####################################################################################################

        ##################################################
        # delete the layer
        ##################################################
        self.delete(argument=layer_id, URI="/api/layer")

        # it is not possible to find the layer that just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.get(URI='/api/layer', expected=expected, id=layer_id)

        self.auth_logout()


class TestAPIFeatureTableErrors(RequestTester):

    def setUp(self):
        self.set_urn('/api/feature_table')

    # feature_table errors - get

    # feature_table errors - create

    def test__post_api_feature_table_create__error__400_bad_request__attribute_in_JSON_is_missing(self):
        self.auth_login("miguel@admin.com", "miguel")

        # try to create a feature table without a mandatory property
        resources = [
            {
                'resource': {
                    'type': 'FeatureTable',
                    'properties': {'start_date': 'timestamp without time zone', 'end_date': 'timestamp without time zone',
                                'address': 'text'},
                    'geometry': {
                        'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
                        'type': 'MULTIPOINT'
                    }
                },
                'missing': 'f_table_name'
            },
            {
                'resource': {
                    'type': 'FeatureTable',
                    'f_table_name': 'layer_1003',
                    'properties': {'start_date': 'timestamp without time zone', 'end_date': 'timestamp without time zone',
                                'address': 'text'}
                },
                'missing': 'geometry'
            },
            {
                'resource': {
                    'type': 'FeatureTable',
                    'f_table_name': 'layer_1003',
                    'geometry': {
                        'crs': {'type': 'name', 'properties': {}},
                        'type': 'MULTIPOINT'
                    },
                    'properties': {'start_date': 'timestamp without time zone', 'end_date': 'timestamp without time zone',
                                'address': 'text'}
                },
                'missing': 'name'
            },
            {
                'resource': {
                    'type': 'FeatureTable',
                    'f_table_name': 'layer_1003',
                    'geometry': {
                        'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}}
                    },
                    'properties': {'start_date': 'timestamp without time zone', 'end_date': 'timestamp without time zone',
                                'address': 'text'},
                },
                'missing': 'type'
            }
        ]

        for item in resources:
            # self.tester.api_feature_table_create_error_400_bad_request(resource)
            self.post(
                item['resource'], add_suffix_to_uri="/create", status_code=400,
                expected_text=("Some attribute in the JSON is missing. "
                              f"Look at the documentation! (error: '{item['missing']}' is missing)")
            )

        self.auth_logout()
        # try to do the test with a admin
        self.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a feature table without a mandatory property
        resource = {
            'type': 'FeatureTable',
            'f_table_name': 'layer_1003',
            'properties': {'start_date': 'timestamp without time zone', 'end_date': 'timestamp without time zone',
                           'address': 'text'},
            'geometry': {
                'type': 'MULTIPOINT'
            }
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=400,
            expected_text=("Some attribute in the JSON is missing. "
                          "Look at the documentation! (error: 'crs' is missing)")
        )

        self.auth_logout()

    def test__post_api_feature_table_create__error__400_bad_request__property_is_a_reserved_word(self):
        self.auth_login("miguel@admin.com", "miguel")

        # try to create feature tables with reserved words
        resources = [
            {
                'resource': {
                    'type': 'FeatureTable',
                    'f_table_name': 'layer_1003',
                    'geometry': {
                        'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}}
                    },
                    'properties': {'id': 'integer', 'start_date': 'timestamp without time zone',
                                   'end_date': 'timestamp without time zone', 'address': 'text'}
                },
                'reserved': 'id'
            },
            {
                'resource': {
                    'type': 'FeatureTable',
                    'f_table_name': 'layer_1003',
                    'geometry': {
                        'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}}
                    },
                    'properties': {'geom': 'geometry', 'start_date': 'timestamp without time zone',
                                   'end_date': 'timestamp without time zone', 'address': 'text'}
                },
                'reserved': 'geom'
            },
            {
                'resource': {
                    'type': 'FeatureTable',
                    'f_table_name': 'layer_1003',
                    'geometry': {
                        'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}}
                    },
                    'properties': {'version': 'integer', 'start_date': 'timestamp without time zone',
                                   'end_date': 'timestamp without time zone', 'address': 'text'}
                },
                'reserved': 'version'
            },
            {
                'resource': {
                    'type': 'FeatureTable',
                    'f_table_name': 'layer_1003',
                    'geometry': {
                        'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}}
                    },
                    'properties': {'changeset_id': 'integer', 'start_date': 'timestamp without time zone',
                                   'end_date': 'timestamp without time zone', 'address': 'text'}
                },
                'reserved': 'changeset_id'
            },
            {
                'resource': {
                    'type': 'FeatureTable',
                    'f_table_name': 'layer_1003',
                    'geometry': {
                        'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}}
                    },
                    'properties': {'abort': 'text', 'start_date': 'timestamp without time zone',
                                   'end_date': 'timestamp without time zone', 'address': 'text'}
                },
                'reserved': 'abort'
            }
        ]

        for item in resources:
            self.post(
                item['resource'], add_suffix_to_uri="/create", status_code=400,
                expected_text=("There is a field that is a reserved word. "
                              f"Please, rename it. (field: `{item['reserved']}`)")
            )

        self.auth_logout()

    def test__post_api_feature_table_create__error__400_bad_request__f_table_name_has_special_chars_or_it_starts_with_number(self):
        self.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a layer with a invalid 'f_table_name' value
        list_invalid_f_table_name = [
            "*)layer", "lay+-er", "layer_(/", "837_layer", "0_layer",
            " new_layer", "new_layer ", "new layer"
        ]

        for invalid_f_table_name in list_invalid_f_table_name:
            resource = {
                'type': 'FeatureTable',
                'f_table_name': invalid_f_table_name,
                'properties': {'id': 'integer', 'geom': 'geometry', 'version': 'integer', 'changeset_id': 'integer',
                               'start_date': 'timestamp without time zone', 'end_date': 'timestamp without time zone',
                               'address': 'text'},
                'geometry': {
                    'type': 'MULTIPOINT'
                }
            }
            self.post(
                resource, add_suffix_to_uri="/create", status_code=400,
                expected_text=("`f_table_name` property can not have special characters. "
                              f"(f_table_name: `{invalid_f_table_name}`)")
            )

        self.auth_logout()

    def test__post_api_feature_table_create__error__400_bad_request__invalid_fields(self):
        self.auth_login("rodrigo@admin.com", "rodrigo")

        resources = [
            # try to create a layer with invalid field (special chars)
            {
                'resource': {
                    'type': 'FeatureTable',
                    'f_table_name': "layer_100X",
                    'properties': {'a(ddre*ss': 'text', 'end_date': 'timestamp without time zone'},
                    'geometry': {
                        'type': 'MULTIPOINT'
                    }
                },
                'invalid_field': 'a(ddre*ss'
            },
            # try to create a layer with invalid field (starts with number)
            {
                'resource': {
                    'type': 'FeatureTable',
                    'f_table_name': "layer_100X",
                    'properties': {'0address': 'text', 'end_date': 'timestamp without time zone'},
                    'geometry': {
                        'type': 'MULTIPOINT'
                    }
                },
                'invalid_field': '0address'
            },
            # try to create a layer with invalid field (white space)
            {
                'resource': {
                    'type': 'FeatureTable',
                    'f_table_name': "layer_100X",
                    'properties': {'address ': 'text', 'end_date': 'timestamp without time zone'},
                    'geometry': {
                        'type': 'MULTIPOINT'
                    }
                },
                'invalid_field': 'address '
            }
        ]

        for item in resources:
            self.post(
                item['resource'], add_suffix_to_uri="/create", status_code=400,
                expected_text=('There is a field with have special characters. '
                              f"Please, rename it. (field: `{item['invalid_field']}`)")
            )

        self.auth_logout()

    def test__post_api_feature_table_create__error__401_unauthorized(self):
        resource = {
            'type': 'FeatureTable',
            'f_table_name': 'layer_1003',
            'properties': {'start_date': 'timestamp without time zone', 'end_date': 'timestamp without time zone',
                           'address': 'text'},
            'geometry': {
                'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
                'type': 'MULTIPOINT'
            }
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=401,
            expected_text=("A valid `Authorization` header is necessary!")
        )

    def test__post_api_feature_table_create__error__403_forbidden__invalid_user_tries_to_create_a_feature_table(self):
        self.auth_login("miguel@admin.com", "miguel")

        resource = {
            'type': 'FeatureTable',
            'f_table_name': 'layer_1002',
            'properties': {'start_date': 'timestamp without time zone', 'end_date': 'timestamp without time zone',
                           'address': 'text'},
            'geometry': {
                'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
                'type': 'MULTIPOINT'
            }
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=403,
            expected_text=("The layer owner or administrator user are who can create or delete this resource.")
        )

        self.auth_logout()

    def test__post_api_feature_table_create__error__404_not_found__f_table_name_doesnt_exist(self):
        self.auth_login("miguel@admin.com", "miguel")

        # try to insert a feature table with a 'f_table_name' that does not exist
        resource = {
            'type': 'FeatureTable',
            'f_table_name': 'address',
            'properties': {'start_date': 'timestamp without time zone', 'end_date': 'timestamp without time zone',
                           'address': 'text'},
            'geometry': {
                'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
                'type': 'MULTIPOINT'
            }
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=404,
            expected_text=("Not found any layer with the passed `f_table_name` property. "
                          "You need to create a layer with the `f_table_name` property "
                          "before using this function.")
        )

        self.auth_logout()

    def test__post_api_feature_table_create__error__409_conflict__f_table_name_is_reserved_name(self):
        self.auth_login("miguel@admin.com", "miguel")

        # try to create a layer with f_table_name that table that already exist or with reserved name
        list_invalid_f_table_name = [ "abort", "access"]

        for invalid_f_table_name in list_invalid_f_table_name:
            resource = {
                'type': 'FeatureTable',
                'f_table_name': invalid_f_table_name,
                'properties': {'start_date': 'timestamp without time zone', 'end_date': 'timestamp without time zone',
                               'address': 'text'},
                'geometry': {
                    'type': 'MULTIPOINT'
                }
            }
            self.post(
                resource, add_suffix_to_uri="/create", status_code=409,
                expected_text=("Conflict with `f_table_name` property. The table name is a reserved word. "
                              f"Please, rename it. (`f_table_name`: `{invalid_f_table_name}`)")
            )

        self.auth_logout()

    # feature_table column errors - create

    def test__post_api_feature_table_column_create__error__400_bad_request__attribute_in_JSON_is_missing(self):
        self.auth_login("miguel@admin.com", "miguel")

        # try to create a feature table column without `f_table_name` property
        feature_table_column = {
            'type': 'FeatureTableColumn',
            'column_name': 'name',
            'column_type': 'text'
        }
        self.post(
            URI="/api/feature_table_column/create", body=feature_table_column, status_code=400,
            expected_text=("Some attribute in the JSON is missing. "
                          "Look at the documentation! (error: 'f_table_name' is missing)")
        )

        # try to create a feature table column without `column_name` property
        feature_table_column = {
            'type': 'FeatureTableColumn',
            'f_table_name': 'layer_1003',
            'column_type': 'text'
        }
        self.post(
            URI="/api/feature_table_column/create", body=feature_table_column, status_code=400,
            expected_text=("Some attribute in the JSON is missing. "
                          "Look at the documentation! (error: 'column_name' is missing)")
        )

        self.auth_logout()
        # try to do the test with an admin
        self.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a feature table column without `column_type` property
        feature_table_column = {
            'type': 'FeatureTableColumn',
            'f_table_name': 'layer_1003',
            'column_name': 'name'
        }
        self.post(
            URI="/api/feature_table_column/create", body=feature_table_column, status_code=400,
            expected_text=("Some attribute in the JSON is missing. "
                          "Look at the documentation! (error: 'column_type' is missing)")
        )

        self.auth_logout()

    def test__post_api_feature_table_column_create__error__401_unauthorized(self):
        resource = {
            'type': 'FeatureTableColumn',
            'f_table_name': 'layer_1003',
            'column_name': 'name',
            'column_type': 'text',
        }
        self.post(
            URI="/api/feature_table_column/create", body=resource, status_code=401,
            expected_text="A valid `Authorization` header is necessary!"
        )

    def test__post_api_feature_table_column_create__error__403_forbidden__invalid_user_tries_to_create_a_resource(self):
        self.auth_login("miguel@admin.com", "miguel")

        resource = {
            'type': 'FeatureTableColumn',
            'f_table_name': 'layer_1002',
            'column_name': 'name',
            'column_type': 'text',
        }
        self.post(
            URI="/api/feature_table_column/create", body=resource, status_code=403,
            expected_text=("The layer owner or collaborator user, or administrator one are "
                          "who can update this resource.")
        )

        self.auth_logout()

    def test__post_api_feature_table_column_create__error__404_not_found__f_table_name_doesnt_exist(self):
        self.auth_login("miguel@admin.com", "miguel")

        resource = {
            'type': 'FeatureTableColumn',
            'f_table_name': 'address',
            'column_name': 'name',
            'column_type': 'text',
        }
        self.post(
            URI="/api/feature_table_column/create", body=resource, status_code=404,
            expected_text=("Not found any layer with the passed `f_table_name` property. "
                          "You need to create a layer with the `f_table_name` property before "
                          "using this function.")
        )

        self.auth_logout()

    # feature_table column errors - delete

    def test__delete_api_feature_table_column__error__400_bad_request__invalid_column_name(self):
        self.auth_login("rodrigo@admin.com", "rodrigo")

        items = [
            {"f_table_name": 'layer_1003', "column_name": 'id'},
            {"f_table_name": 'layer_1003', "column_name": 'geom'},
            {"f_table_name": 'layer_1003', "column_name": 'changeset_id'},
            {"f_table_name": 'layer_1003', "column_name": 'geom'}
        ]

        for item in items:
            self.delete(
                URI="/api/feature_table_column", **item, status_code=400,
                expected_text="Invalid parameter."
            )

        self.auth_logout()

    def test__delete_api_feature_table_column__error__401_unauthorized__user_without_login(self):
        self.delete(
            URI="/api/feature_table_column", f_table_name='layer_1003', column_name="start_date",
            status_code=401, expected_text="A valid `Authorization` header is necessary!"
        )

    def test__delete_api_feature_table_column__error__403_forbidden__invalid_user_tries_to_manage(self):
        self.auth_login("miguel@admin.com", "miguel")

        self.delete(
            URI="/api/feature_table_column", f_table_name='layer_1002', column_name="start_date",
            status_code=403, expected_text=("The layer owner or collaborator user, or administrator one "
                                           "are who can update this resource.")
        )

        self.auth_logout()

    def test__delete_api_feature_table_column__error__404_not_found(self):
        self.auth_login("rodrigo@admin.com", "rodrigo")

        # invalid f_table_name
        self.delete(
            URI="/api/feature_table_column", f_table_name='addresses', column_name="start_date",
            status_code=404, expected_text=("Not found any layer with the passed `f_table_name` property. "
                                           "You need to create a layer with the `f_table_name` property "
                                           "before using this function.")
        )

        # invalid column name
        self.delete(
            URI="/api/feature_table_column", f_table_name='layer_1002', column_name="name",
            status_code=404, expected_text=("Not found the specified column. (error: column `name` of "
                                           "relation `layer_1002` does not exist)")
        )

        self.auth_logout()


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
