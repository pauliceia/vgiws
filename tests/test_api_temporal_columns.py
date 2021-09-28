
from util.tester import RequestTester


class TestAPITemporalColumns(RequestTester):

    def setUp(self):
        self.base_urn_tc = '/api/temporal_columns'
        self.base_urn_layer = '/api/layer'
        self.base_urn_ul = '/api/user_layer'
        self.set_urn(self.base_urn_tc)

    # temporal_columns - get

    def test__get_api_temporal_columns__return_all_temporal_columns(self):
        expected = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "TemporalColumns",
                    "properties": {
                        "end_date": "1975-12-31",
                        "start_date": "1869-01-01",
                        "f_table_name": "layer_1001",
                        "end_date_mask": {
                            "id": 1001,
                            "mask": "YYYY-MM-DD"
                        },
                        "start_date_mask": {
                            "id": 1001,
                            "mask": "YYYY-MM-DD"
                        },
                        "end_date_column_name": "end_date",
                        "start_date_column_name": "start_date"
                    }
                },
                {
                    "type": "TemporalColumns",
                    "properties": {
                        "end_date": "1890-12-31",
                        "start_date": "1886-01-01",
                        "f_table_name": "layer_1002",
                        "end_date_mask": {
                            "id": 1001,
                            "mask": "YYYY-MM-DD"
                        },
                        "start_date_mask": {
                            "id": 1001,
                            "mask": "YYYY-MM-DD"
                        },
                        "end_date_column_name": "end_date",
                        "start_date_column_name": "start_date"
                    }
                },
                {
                    "type": "TemporalColumns",
                    "properties": {
                        "end_date": "1930-12-31",
                        "start_date": "1920-01-01",
                        "f_table_name": "layer_1003",
                        "end_date_mask": {
                            "id": 1001,
                            "mask": "YYYY-MM-DD"
                        },
                        "start_date_mask": {
                            "id": 1001,
                            "mask": "YYYY-MM-DD"
                        },
                        "end_date_column_name": "end_date",
                        "start_date_column_name": "start_date"
                    }
                },
                {
                    "type": "TemporalColumns",
                    "properties": {
                        "end_date": "1920-12-31",
                        "start_date": "1920-01-01",
                        "f_table_name": "layer_1004",
                        "end_date_mask": {
                            "id": 1002,
                            "mask": "YYYY-MM"
                        },
                        "start_date_mask": {
                            "id": 1002,
                            "mask": "YYYY-MM"
                        },
                        "end_date_column_name": "end_date",
                        "start_date_column_name": "start_date"
                    }
                },
                {
                    "type": "TemporalColumns",
                    "properties": {
                        "end_date": "1940-12-31",
                        "start_date": "1920-01-01",
                        "f_table_name": "layer_1005",
                        "end_date_mask": {
                            "id": 1002,
                            "mask": "YYYY-MM"
                        },
                        "start_date_mask": {
                            "id": 1002,
                            "mask": "YYYY-MM"
                        },
                        "end_date_column_name": "end_date",
                        "start_date_column_name": "start_date"
                    }
                },
                {
                    "type": "TemporalColumns",
                    "properties": {
                        "end_date": "1930-12-31",
                        "start_date": "1900-01-01",
                        "f_table_name": "layer_1006",
                        "end_date_mask": {
                            "id": 1003,
                            "mask": "YYYY"
                        },
                        "start_date_mask": {
                            "id": 1003,
                            "mask": "YYYY"
                        },
                        "end_date_column_name": "end_date",
                        "start_date_column_name": "start_date"
                    }
                }
            ]
        }

        self.get(expected)

    def test__get_api_temporal_columns__return_temporal_columns_by_f_table_name(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    "type": "TemporalColumns",
                    "properties": {
                        "end_date": "1930-12-31",
                        "start_date": "1920-01-01",
                        "f_table_name": "layer_1003",
                        "end_date_mask": {
                            "id": 1001,
                            "mask": "YYYY-MM-DD"
                        },
                        "start_date_mask": {
                            "id": 1001,
                            "mask": "YYYY-MM-DD"
                        },
                        "end_date_column_name": "end_date",
                        "start_date_column_name": "start_date"
                    }
                }
            ]
        }

        self.get(expected, f_table_name="1003")

    def test__get_api_temporal_columns__return_temporal_columns_by_temporal_bounding_box(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    "type": "TemporalColumns",
                    "properties": {
                        "end_date": "1920-12-31",
                        "start_date": "1920-01-01",
                        "f_table_name": "layer_1004",
                        "end_date_mask": {
                            "id": 1002,
                            "mask": "YYYY-MM"
                        },
                        "start_date_mask": {
                            "id": 1002,
                            "mask": "YYYY-MM"
                        },
                        "end_date_column_name": "end_date",
                        "start_date_column_name": "start_date"
                    }
                }
            ]
        }

        self.get(expected, start_date_gte='1890-01-01', end_date_lte='1920-12-31')

    def test__get_api_temporal_columns__return_temporal_columns_by_start_date_greater_than_or_equal(self):
        expected = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "TemporalColumns",
                    "properties": {
                        "end_date": "1930-12-31",
                        "start_date": "1920-01-01",
                        "f_table_name": "layer_1003",
                        "end_date_mask": {
                            "id": 1001,
                            "mask": "YYYY-MM-DD"
                        },
                        "start_date_mask": {
                            "id": 1001,
                            "mask": "YYYY-MM-DD"
                        },
                        "end_date_column_name": "end_date",
                        "start_date_column_name": "start_date"
                    }
                },
                {
                    "type": "TemporalColumns",
                    "properties": {
                        "end_date": "1920-12-31",
                        "start_date": "1920-01-01",
                        "f_table_name": "layer_1004",
                        "end_date_mask": {
                            "id": 1002,
                            "mask": "YYYY-MM"
                        },
                        "start_date_mask": {
                            "id": 1002,
                            "mask": "YYYY-MM"
                        },
                        "end_date_column_name": "end_date",
                        "start_date_column_name": "start_date"
                    }
                },
                {
                    "type": "TemporalColumns",
                    "properties": {
                        "end_date": "1940-12-31",
                        "start_date": "1920-01-01",
                        "f_table_name": "layer_1005",
                        "end_date_mask": {
                            "id": 1002,
                            "mask": "YYYY-MM"
                        },
                        "start_date_mask": {
                            "id": 1002,
                            "mask": "YYYY-MM"
                        },
                        "end_date_column_name": "end_date",
                        "start_date_column_name": "start_date"
                    }
                }
            ]
        }

        self.get(expected, start_date_gte="1910-01-01")

    def test__get_api_temporal_columns__return_temporal_columns_by_end_date_less_than_or_equal(self):
        expected = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "TemporalColumns",
                    "properties": {
                        "end_date": "1890-12-31",
                        "start_date": "1886-01-01",
                        "f_table_name": "layer_1002",
                        "end_date_mask": {
                            "id": 1001,
                            "mask": "YYYY-MM-DD"
                        },
                        "start_date_mask": {
                            "id": 1001,
                            "mask": "YYYY-MM-DD"
                        },
                        "end_date_column_name": "end_date",
                        "start_date_column_name": "start_date"
                    }
                },
                {
                    "type": "TemporalColumns",
                    "properties": {
                        "end_date": "1920-12-31",
                        "start_date": "1920-01-01",
                        "f_table_name": "layer_1004",
                        "end_date_mask": {
                            "id": 1002,
                            "mask": "YYYY-MM"
                        },
                        "start_date_mask": {
                            "id": 1002,
                            "mask": "YYYY-MM"
                        },
                        "end_date_column_name": "end_date",
                        "start_date_column_name": "start_date"
                    }
                }
            ]
        }

        self.get(expected, end_date_lte="1920-12-31")

    def test__get_api_temporal_columns__return_temporal_columns_by_start_date(self):
        expected = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "TemporalColumns",
                    "properties": {
                        "end_date": "1930-12-31",
                        "start_date": "1900-01-01",
                        "f_table_name": "layer_1006",
                        "end_date_mask": {
                            "id": 1003,
                            "mask": "YYYY"
                        },
                        "start_date_mask": {
                            "id": 1003,
                            "mask": "YYYY"
                        },
                        "end_date_column_name": "end_date",
                        "start_date_column_name": "start_date"
                    }
                }
            ]
        }

        self.get(expected, start_date="1900-01-01")

    def test__get_api_temporal_columns__return_temporal_columns_by_end_date(self):
        expected = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "TemporalColumns",
                    "properties": {
                        "end_date": "1920-12-31",
                        "start_date": "1920-01-01",
                        "f_table_name": "layer_1004",
                        "end_date_mask": {
                            "id": 1002,
                            "mask": "YYYY-MM"
                        },
                        "start_date_mask": {
                            "id": 1002,
                            "mask": "YYYY-MM"
                        },
                        "end_date_column_name": "end_date",
                        "start_date_column_name": "start_date"
                    }
                }
            ]
        }

        self.get(expected, end_date="1920-12-31")

    def test__get_api_temporal_columns__return_zero_resources(self):
        expected = {'type': 'FeatureCollection', 'features': []}

        self.get(expected, f_table_name="layer_x")
        self.get(expected, start_date="1800-01-01")
        self.get(expected, end_date="2000-01-01")
        self.get(expected, start_date_gte="2000-01-01")
        self.get(expected, end_date_lte="1800-01-01")

    # temporal_columns - create and update

    def test__post_put_delete_api_temporal_columns(self):
        self.auth_login("miguel@admin.com", "miguel")

        f_table_name = 'addresses_1930'

        ##################################################
        # create a layer
        ##################################################
        self.set_urn(self.base_urn_layer)
        layer = {
            "type": "Layer",
            "properties": {
                "id": -1, "f_table_name": f_table_name,
                "name": "Addresses in 1930", "description": "", "source_description": "",
                "collaborators": [
                    {"id": 1001, "name": "Administrator", 'is_the_creator': False},
                    {"id": 1005, "name": "Gabriel", 'is_the_creator': False}
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
        layer_id = self.post(layer, add_suffix_to_uri="/create")

        ####################################################################################################

        ##################################################
        # create the time columns for the layer above
        ##################################################
        self.set_urn(self.base_urn_tc)
        temporal_columns = {
            "properties": {
                "f_table_name": f_table_name,
                "start_date": "1900-01-01",
                "end_date": "1920-12-31",
                "start_date_column_name": "start_date",
                "end_date_column_name": "end_date",
                "end_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"},
                "start_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"}
            },
            "type": "TemporalColumns"
        }
        self.post(temporal_columns, expected_text='', add_suffix_to_uri="/create")

        ##################################################
        # update the time columns
        ##################################################
        temporal_columns["properties"]["start_date"] = '1920-01-01'
        self.put(temporal_columns)

        ##################################################
        # check if the resource was modified
        ##################################################
        expected_temporal_columns = {'type': 'FeatureCollection', 'features': [temporal_columns]}
        self.get(expected_temporal_columns, f_table_name=f_table_name)

        ##################################################
        # the temporal columns table is removed automatically when its layer is deleted
        ##################################################

        ####################################################################################################

        ##################################################
        # delete the layer
        ##################################################
        self.set_urn(self.base_urn_layer)
        self.delete(argument=layer_id)

        # check if the layer does not exist
        expected = {'type': 'FeatureCollection', 'features': []}
        self.get(expected, id=layer_id)

        # check if the temporal columns does not exist
        self.set_urn(self.base_urn_tc)
        self.get(expected, f_table_name=f_table_name)

        self.auth_logout()

    def test__post_put_delete_api_temporal_columns___with_collaborator_user(self):
        ####################################################################################################
        # log in with a normal user
        ####################################################################################################
        self.auth_login("miguel@admin.com", "miguel")

        f_table_name = 'addresses_1930'

        ##################################################
        # create a layer with the normal user
        ##################################################
        self.set_urn(self.base_urn_layer)
        layer = {
            "type": "Layer",
            "properties": {
                "id": -1, "f_table_name": f_table_name,
                "name": "Addresses in 1930", "description": "", "source_description": "",
                "collaborators": [
                    {"id": 1001, "name": "Administrator", 'is_the_creator': False},
                    {"id": 1005, "name": "Gabriel", 'is_the_creator': False}
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
        layer_id = self.post(layer, add_suffix_to_uri="/create")

        ##################################################
        # create the temporal columns for the layer above with the normal user
        ##################################################
        self.set_urn(self.base_urn_tc)
        temporal_columns = {
            "properties": {
                "f_table_name": f_table_name,
                "start_date": "1900-01-01",
                "end_date": "1920-12-31",
                "start_date_column_name": "start_date",
                "end_date_column_name": "end_date",
                "end_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"},
                "start_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"}
            },
            "type": "TemporalColumns"
        }

        self.post(temporal_columns, expected_text='', add_suffix_to_uri="/create")

        ##################################################
        # add a collaborator to the layer
        ##################################################
        user_id_collaborator = 1004

        self.set_urn(self.base_urn_ul)
        self.post({
            'properties': {'user_id': user_id_collaborator, 'layer_id': layer_id},
            'type': 'UserLayer'
        }, add_suffix_to_uri="/create")

        ####################################################################################################
        # log in with the collaborator user in order to update the temporal columns
        ####################################################################################################
        self.auth_logout()
        self.auth_login("rafael@admin.com", "rafael")

        self.set_urn(self.base_urn_tc)

        ##################################################
        # update the temporal columns with the collaborator user
        ##################################################
        temporal_columns["properties"]["start_date"] = '1920-01-01'
        self.put(temporal_columns)

        ##################################################
        # check if the resource was modified
        ##################################################
        expected_temporal_columns = {'type': 'FeatureCollection', 'features': [temporal_columns]}
        self.get(expected_temporal_columns, f_table_name=f_table_name)

        ##################################################
        # the temporal columns table is removed automatically when its layer is deleted
        ##################################################
        # log out the collaborator user
        self.auth_logout()

        ####################################################################################################
        # log in with the normal user again in order to delete the layer
        ####################################################################################################
        self.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # delete the layer
        ##################################################
        self.set_urn(self.base_urn_layer)
        self.delete(argument=layer_id)

        # check if the layer does not exist
        expected = {'type': 'FeatureCollection', 'features': []}
        self.get(expected, id=layer_id)

        # check if the temporal columns does not exist
        self.set_urn(self.base_urn_tc)
        self.get(expected, f_table_name=f_table_name)

        self.auth_logout()

    def test__post_put_delete_api_temporal_columns___with_admin_user(self):
        ####################################################################################################
        # log in with a normal user
        ####################################################################################################
        self.auth_login("miguel@admin.com", "miguel")

        f_table_name = 'addresses_1930'

        ##################################################
        # create a layer with a normal user
        ##################################################
        self.set_urn(self.base_urn_layer)
        layer = {
            "type": "Layer",
            "properties": {
                "id": -1, "f_table_name": f_table_name,
                "name": "Addresses in 1930", "description": "", "source_description": "",
                "collaborators": [
                    {"id": 1001, "name": "Administrator", 'is_the_creator': False},
                    {"id": 1005, "name": "Gabriel", 'is_the_creator': False}
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
        layer_id = self.post(layer, add_suffix_to_uri="/create")

        ####################################################################################################
        # log in with an admin user in order to create and update the time columns
        ####################################################################################################
        self.auth_logout()
        self.auth_login("rodrigo@admin.com", "rodrigo")

        ##################################################
        # create the time columns for the layer above
        ##################################################
        self.set_urn(self.base_urn_tc)
        temporal_columns = {
            "properties": {
                "f_table_name": f_table_name,
                "start_date": "1900-01-01",
                "end_date": "1920-12-31",
                "start_date_column_name": "start_date",
                "end_date_column_name": "end_date",
                "end_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"},
                "start_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"}
            },
            "type": "TemporalColumns"
        }
        self.post(temporal_columns, expected_text='', add_suffix_to_uri="/create")

        ##################################################
        # update the time columns
        ##################################################
        temporal_columns["properties"]["start_date"] = '1920-01-01'
        self.put(temporal_columns)

        ##################################################
        # check if the resource has been modified
        ##################################################
        expected_temporal_columns = {'type': 'FeatureCollection', 'features': [temporal_columns]}
        self.get(expected_temporal_columns, f_table_name=f_table_name)

        ##################################################
        # the temporal columns table is removed automatically when its layer is deleted
        ##################################################

        ####################################################################################################
        # log in with the normal user again in order to delete the layer
        ####################################################################################################
        self.auth_logout()
        self.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # delete the layer
        ##################################################
        self.set_urn(self.base_urn_layer)
        self.delete(argument=layer_id)

        # check if the layer does not exist
        expected = {'type': 'FeatureCollection', 'features': []}
        self.get(expected, id=layer_id)

        # check if the temporal columns does not exist
        self.set_urn(self.base_urn_tc)
        self.get(expected, f_table_name=f_table_name)

        self.auth_logout()

    def test__post_put_delete_api_temporal_columns___not_fill_all_fields(self):
        ####################################################################################################
        # log in with a normal user
        ####################################################################################################
        self.auth_login("miguel@admin.com", "miguel")

        f_table_name = 'addresses_1930_12'

        ##################################################
        # create a layer
        ##################################################
        self.set_urn(self.base_urn_layer)
        layer = {
            "type": "Layer",
            "properties": {
                "id": -1, "f_table_name": f_table_name,
                "name": "Addresses in 1930", "description": "", "source_description": "",
                "collaborators": [
                    {"id": 1001, "name": "Administrator", 'is_the_creator': False},
                    {"id": 1005, "name": "Gabriel", 'is_the_creator': False}
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
        layer_id = self.post(layer, add_suffix_to_uri="/create")

        ####################################################################################################

        ##################################################
        # create the time columns for the layer above
        ##################################################
        self.set_urn(self.base_urn_tc)
        temporal_columns = {
            "properties": {
                "f_table_name": f_table_name,
                "start_date": "1900-01-01",
                "end_date": "1920-12-31",
                "start_date_column_name": "",
                "end_date_column_name": "",
                "end_date_mask": {'id': None, 'mask': None},
                "start_date_mask": {'id': None, 'mask': None}
            },
            "type": "TemporalColumns"
        }
        self.post(temporal_columns, expected_text='', add_suffix_to_uri="/create")

        ##################################################
        # update the time columns
        ##################################################
        temporal_columns["properties"]["start_date"] = '1920-01-01'
        self.put(temporal_columns)

        ##################################################
        # check if the resource was modified
        ##################################################
        expected_temporal_columns = {'type': 'FeatureCollection', 'features': [temporal_columns]}
        self.get(expected_temporal_columns, f_table_name=f_table_name)

        ##################################################
        # the temporal columns table is removed automatically when its layer is deleted
        ##################################################

        ####################################################################################################

        ##################################################
        # delete the layer
        ##################################################
        self.set_urn(self.base_urn_layer)
        self.delete(argument=layer_id)

        # check if the layer does not exist
        expected = {'type': 'FeatureCollection', 'features': []}
        self.get(expected, id=layer_id)

        # check if the temporal columns does not exist
        self.set_urn(self.base_urn_tc)
        self.get(expected, f_table_name=f_table_name)

        self.auth_logout()


class TestAPITemporalColumnsErrors(RequestTester):

    def setUp(self):
        self.set_urn('/api/temporal_columns')

    # temporal_columns errors - get

    def test__get_api_temporal_columns__400_bad_request(self):
        test_cases = [
            {"start_date": "1910/01-01"},
            {"end_date": "1910-01/01"},
            {"start_date_gte": "1910/01=01"},
            {"end_date_lte": "1910-01)01"}
        ]

        for item in test_cases:
            self.get(**item, status_code=400, expected_text="Invalid date format.")

    # temporal_columns errors - create

    def test__post_api_temporal_columns__400_bad_request__attribute_already_exist(self):
        self.auth_login("miguel@admin.com", "miguel")

        f_table_name = 'layer_1003'

        # try to insert a temporal_columns with a f_table_name that already exist
        resource = {
            'properties': {'f_table_name': f_table_name, 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                           'end_date_column_name': 'end_date', 'start_date_column_name': 'start_date',
                           "end_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"},
                           "start_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"}},
            'type': 'TemporalColumns'
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=400,
            expected_text=(f"Attribute already exists. (error: Key (f_table_name)=({f_table_name})"
                            " already exists.)")
        )

        self.auth_logout()

    def test__post_api_temporal_columns__400_bad_request__attribute_in_JSON_is_missing(self):
        self.auth_login("miguel@admin.com", "miguel")

        test_cases = [
            {
                'resource': {
                    'properties': {'start_date': '1900-01-01', 'end_date': '1920-12-31',
                                'end_date_column_name': 'end_date', 'start_date_column_name': 'start_date',
                                "end_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"},
                                "start_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"}},
                    'type': 'TemporalColumns'
                },
                'missing': 'f_table_name'
            },
            {
                'resource': {
                    'properties': {'f_table_name': 'layer_1003', 'end_date': '1920-12-31',
                                'end_date_column_name': 'end_date', 'start_date_column_name': 'start_date',
                                "end_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"},
                                "start_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"}},
                    'type': 'TemporalColumns'
                },
                'missing': 'start_date'
            },
            {
                'resource': {
                    'properties': {'f_table_name': 'layer_1003', 'start_date': '1900-01-01',
                                'end_date_column_name': 'end_date', 'start_date_column_name': 'start_date',
                                "end_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"},
                                "start_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"}},
                    'type': 'TemporalColumns'
                },
                'missing': 'end_date'
            },
            {
                'resource': {
                    'properties': {'f_table_name': 'layer_1003', 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                                'end_date_column_name': 'end_date',
                                "end_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"},
                                "start_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"}},
                    'type': 'TemporalColumns'
                },
                'missing': 'start_date_column_name'
            },
            {
                'resource': {
                    'properties': {'f_table_name': 'layer_1003', 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                                'start_date_column_name': 'start_date',
                                "end_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"},
                                "start_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"}},
                    'type': 'TemporalColumns'
                },
                'missing': 'end_date_column_name'
            },
            {
                'resource': {
                    'properties': {'f_table_name': 'layer_1003', 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                                'start_date_column_name': 'start_date', 'end_date_column_name': 'end_date',
                                "end_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"}},
                    'type': 'TemporalColumns'
                },
                'missing': 'start_date_mask'
            },
            {
                'resource': {
                    'properties': {'f_table_name': 'layer_1003', 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                                'start_date_column_name': 'start_date', 'end_date_column_name': 'end_date',
                                "start_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"}},
                    'type': 'TemporalColumns'
                },
                'missing': 'end_date_mask'
            }
        ]
        for item in test_cases:
            self.post(
                item['resource'], add_suffix_to_uri="/create", status_code=400,
                expected_text=("Some attribute in the JSON is missing. "
                              f'Look at the documentation! (error: \'{item["missing"]}\' is missing)')
            )

        self.auth_logout()
        # try to do the test with a admin
        self.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a temporal_columns (without start_date_column_name)
        resource = {
            'properties': {'f_table_name': 'layer_1003', 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                           'end_date_column_name': 'end_date',
                           'start_date_mask_id': 1001, 'end_date_mask_id': 1001},
            'type': 'TemporalColumns'
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=400,
            expected_text=("Some attribute in the JSON is missing. "
                           "Look at the documentation! (error: 'start_date_column_name' is missing)")
        )

        self.auth_logout()

    def test__post_api_temporal_columns__400_bad_request__f_table_name_has_special_chars_or_it_starts_with_number(self):
        self.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a layer with invalid f_table_name
        list_invalid_f_table_name = [
            "*)layer", "lay+-er", "layer_(/", "837_layer", "0_layer",
            " new_layer", "new_layer ", "new layer"
        ]

        for invalid_f_table_name in list_invalid_f_table_name:
            resource = {
                'properties': {'f_table_name': invalid_f_table_name, 'start_date': '1900-01-01',
                               'end_date': '1920-12-31', 'end_date_column_name': 'end_date',
                               'start_date_column_name': 'start_date',
                               'start_date_mask_id': 1001, 'end_date_mask_id': 1001},
                'type': 'TemporalColumns'
            }
            self.post(
                resource, add_suffix_to_uri="/create", status_code=400,
                expected_text=('`f_table_name` property can not have special characters.'
                              f' (f_table_name: `{invalid_f_table_name}`)')
            )

        self.auth_logout()

    def test__post_api_temporal_columns__401_unauthorized(self):
        resource = {
            'properties': {'f_table_name': 'layer_1002', 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                           'end_date_column_name': 'end_date', 'start_date_column_name': 'start_date',
                           'start_date_mask_id': 1001, 'end_date_mask_id': 1001},
            'type': 'TemporalColumns'
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=401,
            expected_text="A valid `Authorization` header is necessary!"
        )

    def test__post_api_temporal_columns__403_forbidden(self):
        self.auth_login("miguel@admin.com", "miguel")

        # try to insert a curator with user_id and keyword_id that already exist
        resource = {
            'properties': {'f_table_name': 'layer_1002', 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                           'end_date_column_name': 'end_date', 'start_date_column_name': 'start_date',
                           'start_date_mask_id': 1001, 'end_date_mask_id': 1001},
            'type': 'TemporalColumns'
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=403,
            expected_text=("The layer owner or administrator user are who can create or "
                           "delete this resource.")
        )

        self.auth_logout()

    def test__post_api_temporal_columns__404_not_found(self):
        self.auth_login("miguel@admin.com", "miguel")

        # try to insert a curator with user_id and keyword_id that already exist
        resource = {
            'properties': {'f_table_name': 'address', 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                           'end_date_column_name': 'end_date', 'start_date_column_name': 'start_date',
                           'start_date_mask_id': 1001, 'end_date_mask_id': 1001},
            'type': 'TemporalColumns'
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=404,
            expected_text=("Not found any layer with the passed `f_table_name` property. "
                           "You need to create a layer with the `f_table_name` property before "
                           "using this function.")
        )

        self.auth_logout()

    def test__post_api_temporal_columns__409_conflict(self):
        self.auth_login("miguel@admin.com", "miguel")

        # try to create a layer with f_table_name that table that already exist or with reserved name
        list_invalid_f_table_name = ["abort", "access"]

        for invalid_f_table_name in list_invalid_f_table_name:
            resource = {
                'properties': {'f_table_name': invalid_f_table_name, 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                               'end_date_column_name': 'end_date', 'start_date_column_name': 'start_date',
                               'start_date_mask_id': 1001, 'end_date_mask_id': 1001},
                'type': 'TemporalColumns'
            }
            self.post(
                resource, add_suffix_to_uri="/create", status_code=409,
                expected_text=("Conflict with `f_table_name` property. The table name is a "
                              f"reserved word. Please, rename it. (`f_table_name`: `{invalid_f_table_name}`)")
            )

        self.auth_logout()

    # temporal_columns errors - update

    def test__put_api_temporal_columns__400_bad_request(self):
        self.auth_login("miguel@admin.com", "miguel")

        # try to update a temporal_columns (without item['missing'])
        test_cases = [
            {
                'resource': {
                    'properties': {'start_date': '1900-01-01', 'end_date': '1920-12-31',
                                'end_date_column_name': 'end_date', 'start_date_column_name': 'start_date',
                                "end_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"},
                                "start_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"}},
                    'type': 'TemporalColumns'
                },
                'missing': 'f_table_name'
            },
            {
                'resource': {
                    'properties': {'f_table_name': 'layer_1003', 'end_date': '1920-12-31',
                                'end_date_column_name': 'end_date', 'start_date_column_name': 'start_date',
                                "end_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"},
                                "start_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"}},
                    'type': 'TemporalColumns'
                },
                'missing': 'start_date'
            },
            {
                'resource': {
                    'properties': {'f_table_name': 'layer_1003', 'start_date': '1900-01-01',
                                'end_date_column_name': 'end_date', 'start_date_column_name': 'start_date',
                                "end_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"},
                                "start_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"}},
                    'type': 'TemporalColumns'
                },
                'missing': 'end_date'
            },
            {
                'resource': {
                    'properties': {'f_table_name': 'layer_1003', 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                                'end_date_column_name': 'end_date',
                                "end_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"},
                                "start_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"}},
                    'type': 'TemporalColumns'
                },
                'missing': 'start_date_column_name'
            },
            {
                'resource': {
                    'properties': {'f_table_name': 'layer_1003', 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                                'start_date_column_name': 'start_date',
                                "end_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"},
                                "start_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"}},
                    'type': 'TemporalColumns'
                },
                'missing': 'end_date_column_name'
            },
            {
                'resource': {
                    'properties': {'f_table_name': 'layer_1003', 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                                'start_date_column_name': 'start_date', 'end_date_column_name': 'end_date',
                                "end_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"}},
                    'type': 'TemporalColumns'
                },
                'missing': 'start_date_mask'
            },
            {
                'resource': {
                    'properties': {'f_table_name': 'layer_1003', 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                                'start_date_column_name': 'start_date', 'end_date_column_name': 'end_date',
                                "start_date_mask": {"id": 1001, "mask": "YYYY-MM-DD"}},
                    'type': 'TemporalColumns'
                },
                'missing': 'end_date_mask'
            }
        ]
        for item in test_cases:
            self.put(
                item['resource'], status_code=400,
                expected_text=("Some attribute in the JSON is missing. Look at the documentation! "
                              f"(error: '{item['missing']}' is missing)")
            )

        self.auth_logout()
        # try to do the test case with an administrator user
        self.auth_login("rodrigo@admin.com", "rodrigo")

        # try to update a temporal_columns (without start_date_column_name)
        resource = {
            'properties': {'f_table_name': 'layer_1003', 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                           'end_date_column_name': 'end_date',
                           'start_date_mask_id': 1001, 'end_date_mask_id': 1001},
            'type': 'TemporalColumns'
        }
        self.put(
            resource, status_code=400,
            expected_text=("Some attribute in the JSON is missing. Look at the documentation! "
                           "(error: 'start_date_column_name' is missing)")
        )

        self.auth_logout()

    def test__put_api_temporal_columns__401_unauthorized(self):
        resource = {
            'properties': {'f_table_name': 'layer_1002', 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                           'end_date_column_name': 'end_date', 'start_date_column_name': 'start_date',
                           'start_date_mask_id': 1001, 'end_date_mask_id': 1001},
            'type': 'TemporalColumns'
        }
        self.put(
            resource, status_code=401,
            expected_text="A valid `Authorization` header is necessary!"
        )

    def test__put_api_temporal_columns__403_forbidden(self):
        self.auth_login("miguel@admin.com", "miguel")

        # try to update a temporal_columns with an invalid user
        resource = {
            'properties': {'f_table_name': 'layer_1002', 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                           'end_date_column_name': 'end_date', 'start_date_column_name': 'start_date',
                           'start_date_mask_id': 1001, 'end_date_mask_id': 1001},
            'type': 'TemporalColumns'
        }
        self.put(
            resource, status_code=403,
            expected_text=("The layer owner or collaborator user, or administrator one are who "
                           "can update this resource.")
        )

        self.auth_logout()

    def test__put_api_temporal_columns__404_not_found(self):
        self.auth_login("miguel@admin.com", "miguel")

        # try to update a temporal_columns with an invalid user
        resource = {
            'properties': {'f_table_name': 'address', 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                           'end_date_column_name': 'end_date', 'start_date_column_name': 'start_date',
                           'start_date_mask_id': 1001, 'end_date_mask_id': 1001},
            'type': 'TemporalColumns'
        }
        self.put(
            resource, status_code=404,
            expected_text=("Not found any layer with the passed `f_table_name` property. "
                           "You need to create a layer with the `f_table_name` property before "
                           "using this function.")
        )

        self.auth_logout()


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
