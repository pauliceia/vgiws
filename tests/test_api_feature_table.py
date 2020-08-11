#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/

class TestAPIFeatureTable(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # feature_table - get

    def test_get_api_feature_table_return_all_feature_tables(self):
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

        self.tester.api_feature_table(expected)

    def test_get_api_feature_table_return_feature_table_by_f_table_name(self):
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

        self.tester.api_feature_table(expected, f_table_name="1003")

    def test_get_api_feature_table_return_zero_resources(self):
        expected = {'features': [], 'type': 'FeatureCollection'}
        self.tester.api_feature_table(expected, f_table_name="998")
        self.tester.api_feature_table(expected, f_table_name="999")

    # feature table - create and update

    def test_api_feature_table_create_and_update(self):
        ####################################################################################################
        # login with a normal user
        ####################################################################################################
        self.tester.auth_login("miguel@admin.com", "miguel")

        f_table_name = 'addresses_1930'

        ##################################################
        # create a layer
        ##################################################
        layer = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': f_table_name, 'name': 'Addresses in 1930',
                           'description': '', 'source_description': '',
                           'reference': [1050, 1052], 'keyword': [1001, 1041]}
        }
        layer = self.tester.api_layer_create(layer)

        ####################################################################################################

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
        self.tester.api_feature_table_create(feature_table)

        ##################################################
        # update the feature_table
        ##################################################
        feature_table_column = {
            'f_table_name': f_table_name,
            'column_name': 'name',
            'column_type': 'text',
        }
        self.tester.api_feature_table_column_create(feature_table_column)
        self.tester.api_feature_table_column_delete(f_table_name=f_table_name, column_name="name")

        ##################################################
        # the feature_table is removed automatically when the layer is deleted
        ##################################################

        ####################################################################################################

        ##################################################
        # delete the layer
        ##################################################
        layer_id = layer["properties"]["layer_id"]

        self.tester.api_layer_delete(layer_id)

        # finding the layer that just deleted is not possible
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_layer(expected, layer_id=layer_id)

        self.tester.auth_logout()

    def test_api_feature_table_create_and_update_with_collaborator_user(self):
        ####################################################################################################
        # login with a normal user
        ####################################################################################################
        self.tester.auth_login("miguel@admin.com", "miguel")

        f_table_name = 'addresses_1930'

        ##################################################
        # create a layer
        ##################################################
        layer = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': f_table_name, 'name': 'Addresses in 1930',
                           'description': '', 'source_description': '',
                           'reference': [1050, 1052], 'keyword': [1001, 1041]}
        }
        layer = self.tester.api_layer_create(layer)
        layer_id = layer["properties"]["layer_id"]

        ##################################################
        # add a collaborator to the layer above
        ##################################################
        user_id_collaborator = 1004

        user_layer = {
            'properties': {'user_id': user_id_collaborator, 'layer_id': layer_id},
            'type': 'UserLayer'
        }
        self.tester.api_user_layer_create(user_layer)

        ####################################################################################################
        # login with a collaborator user in order to try to create the feature table
        ####################################################################################################
        self.tester.auth_logout()
        self.tester.auth_login("rafael@admin.com", "rafael")

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
        self.tester.api_feature_table_create_error_403_forbidden(feature_table)

        ####################################################################################################
        # login with the creator user in order to create the feature table
        ####################################################################################################
        self.tester.auth_logout()
        self.tester.auth_login("miguel@admin.com", "miguel")

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
        self.tester.api_feature_table_create(feature_table)

        ####################################################################################################
        # login with a collaborator user again in order to update the feature table
        ####################################################################################################
        self.tester.auth_logout()
        self.tester.auth_login("rafael@admin.com", "rafael")

        ##################################################
        # update the feature_table with the collaborator user
        ##################################################
        feature_table_column = {
            'f_table_name': f_table_name,
            'column_name': 'name',
            'column_type': 'text',
        }
        self.tester.api_feature_table_column_create(feature_table_column)
        self.tester.api_feature_table_column_delete(f_table_name=f_table_name, column_name="name")

        ##################################################
        # the feature_table is removed automatically when the layer is deleted
        ##################################################

        ####################################################################################################
        # login with a normal user again in order to delete the layer
        ####################################################################################################
        self.tester.auth_logout()
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # delete the layer
        ##################################################
        self.tester.api_layer_delete(layer_id)

        # finding the layer that just deleted is not possible
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_layer(expected, layer_id=layer_id)

        self.tester.auth_logout()

    def test_api_feature_table_create_and_update_with_admin_user(self):
        ####################################################################################################
        # login with a normal user
        ####################################################################################################
        self.tester.auth_login("miguel@admin.com", "miguel")

        f_table_name = 'addresses_1930'

        ##################################################
        # create a layer
        ##################################################
        layer = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': f_table_name, 'name': 'Addresses in 1930',
                           'description': '', 'source_description': '',
                           'reference': [1050, 1052], 'keyword': [1001, 1041]}
        }
        layer = self.tester.api_layer_create(layer)

        ####################################################################################################

        self.tester.auth_logout()
        self.tester.auth_login("admin@admin.com", "admin")

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

        self.tester.api_feature_table_create(feature_table)

        ##################################################
        # update the feature_table
        ##################################################
        feature_table_column = {
            'f_table_name': f_table_name,
            'column_name': 'name',
            'column_type': 'text',
        }
        self.tester.api_feature_table_column_create(feature_table_column)

        self.tester.api_feature_table_column_delete(f_table_name=f_table_name, column_name="name")

        ##################################################
        # the feature_table is automatically removed when delete its layer
        ##################################################

        self.tester.auth_logout()
        self.tester.auth_login("miguel@admin.com", "miguel")

        ####################################################################################################

        ##################################################
        # delete the layer
        ##################################################
        # get the id of layer to SEARCH AND REMOVE it
        layer_id = layer["properties"]["layer_id"]

        # REMOVE THE layer AFTER THE TESTS
        self.tester.api_layer_delete(layer_id)

        # it is not possible to find the layer that just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_layer(expected, layer_id=layer_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPIFeatureTableErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # feature_table errors - get

    # feature_table errors - create

    def test_post_api_feature_table_create_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        resources = [
            # try to create a feature table (without f_table_name)
            {
                'type': 'FeatureTable',
                'properties': {'start_date': 'timestamp without time zone', 'end_date': 'timestamp without time zone',
                            'address': 'text'},
                'geometry': {
                    'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
                    'type': 'MULTIPOINT'
                }
            },
            # try to create a feature table (without geometry)
            {
                'type': 'FeatureTable',
                'f_table_name': 'layer_1003',
                'properties': {'start_date': 'timestamp without time zone', 'end_date': 'timestamp without time zone',
                            'address': 'text'}
            },
            # try to create a feature table (without name)
            {
                'type': 'FeatureTable',
                'f_table_name': 'layer_1003',
                'properties': {'start_date': 'timestamp without time zone', 'end_date': 'timestamp without time zone',
                            'address': 'text'},
                'geometry': {
                    'crs': {'type': 'name', 'properties': {}},
                    'type': 'MULTIPOINT'
                }
            },
            # try to create a feature table (without type)
            {
                'type': 'FeatureTable',
                'f_table_name': 'layer_1003',
                'properties': {'id': 'integer', 'geom': 'geometry', 'version': 'integer', 'changeset_id': 'integer',
                            'start_date': 'timestamp without time zone', 'end_date': 'timestamp without time zone',
                            'address': 'text'},
                'geometry': {
                    'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}}
                }
            }
        ]

        for resource in resources:
            self.tester.api_feature_table_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()
        # try to do the test with a admin
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a feature table (without crs)
        resource = {
            'type': 'FeatureTable',
            'f_table_name': 'layer_1003',
            'properties': {'id': 'integer', 'geom': 'geometry', 'version': 'integer', 'changeset_id': 'integer',
                           'start_date': 'timestamp without time zone', 'end_date': 'timestamp without time zone',
                           'address': 'text'},
            'geometry': {
                'type': 'MULTIPOINT'
            }
        }
        self.tester.api_feature_table_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_feature_table_create_error_400_bad_request_f_table_name_has_special_chars_or_it_starts_with_number(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a layer with invalid f_table_name
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

            self.tester.api_feature_table_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_feature_table_create_error_400_bad_request_invalid_fields(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a layer with invalid field (special chars)
        resource = {
            'type': 'FeatureTable',
            'f_table_name': "layer_100X",
            'properties': {'a(ddre*ss': 'text', 'end_date': 'timestamp without time zone'},
            'geometry': {
                'type': 'MULTIPOINT'
            }
        }
        self.tester.api_feature_table_create_error_400_bad_request(resource)

        # try to create a layer with invalid field (starts with number)
        resource = {
            'type': 'FeatureTable',
            'f_table_name': "layer_100X",
            'properties': {'0address': 'text', 'end_date': 'timestamp without time zone'},
            'geometry': {
                'type': 'MULTIPOINT'
            }
        }
        self.tester.api_feature_table_create_error_400_bad_request(resource)

        # try to create a layer with invalid field (white space)
        resource = {
            'type': 'FeatureTable',
            'f_table_name': "layer_100X",
            'properties': {'address ': 'text', 'end_date': 'timestamp without time zone'},
            'geometry': {
                'type': 'MULTIPOINT'
            }
        }
        self.tester.api_feature_table_create_error_400_bad_request(resource)

        # try to create a layer with invalid field (db reserved word)
        resource = {
            'type': 'FeatureTable',
            'f_table_name': "layer_100X",
            'properties': {'abort': 'text', 'end_date': 'timestamp without time zone'},
            'geometry': {
                'type': 'MULTIPOINT'
            }
        }
        self.tester.api_feature_table_create_error_400_bad_request(resource)

        # try to create a layer with invalid field (db reserved word)
        resource = {
            'type': 'FeatureTable',
            'f_table_name': "layer_100X",
            'properties': {'id': 'integer', 'end_date': 'timestamp without time zone'},
            'geometry': {
                'type': 'MULTIPOINT'
            }
        }
        self.tester.api_feature_table_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_feature_table_create_error_401_unauthorized_without_authorization_header(self):
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
        self.tester.api_feature_table_create_error_401_unauthorized(resource)

    def test_post_api_feature_table_create_error_403_forbidden_invalid_user_tries_to_create_a_feature_table(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        # try to insert a curator with user_id and keyword_id that already exist
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
        self.tester.api_feature_table_create_error_403_forbidden(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_feature_table_create_error_404_not_found_f_table_name_doesnt_exist(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        # try to insert a feature table with a f_table_name that already exist
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
        self.tester.api_feature_table_create_error_404_not_found(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_feature_table_create_error_409_conflict_f_table_name_is_reserved_name(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        # try to create a layer with f_table_name that table that already exist or with reserved name
        list_invalid_f_table_name = ["abort", "access"]

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
            self.tester.api_feature_table_create_error_409_conflict(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    # feature_table column errors - create

    def test_post_api_feature_table_column_create_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        # try to create a feature_table_column without f_table_name
        feature_table_column = {
            'type': 'FeatureTableColumn',
            'column_name': 'name',
            'column_type': 'text'
        }
        self.tester.api_feature_table_column_create_error_400_bad_request(feature_table_column)

        # try to create a feature_table_column without column_name
        feature_table_column = {
            'type': 'FeatureTableColumn',
            'f_table_name': 'layer_1003',
            'column_type': 'text'
        }
        self.tester.api_feature_table_column_create_error_400_bad_request(feature_table_column)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()
        # try to do the test with a admin
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # try to create a feature_table_column without column_type
        feature_table_column = {
            'type': 'FeatureTableColumn',
            'f_table_name': 'layer_1003',
            'column_name': 'name'
        }
        self.tester.api_feature_table_column_create_error_400_bad_request(feature_table_column)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_feature_table_column_create_error_401_unauthorized_without_authorization_header(self):
        resource = {
            'type': 'FeatureTableColumn',
            'f_table_name': 'layer_1003',
            'column_name': 'name',
            'column_type': 'text',
        }
        self.tester.api_feature_table_column_create_error_401_unauthorized(resource)

    def test_post_api_feature_table_column_create_error_403_forbidden_invalid_user_tries_to_create_a_resource(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        resource = {
            'type': 'FeatureTableColumn',
            'f_table_name': 'layer_1002',
            'column_name': 'name',
            'column_type': 'text',
        }
        self.tester.api_feature_table_column_create_error_403_forbidden(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_feature_table_column_create_error_404_not_found_f_table_name_doesnt_exist(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        # try to insert a feature table with a f_table_name that already exist
        resource = {
            'type': 'FeatureTableColumn',
            'f_table_name': 'address',
            'column_name': 'name',
            'column_type': 'text',
        }
        self.tester.api_feature_table_column_create_error_404_not_found(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    # feature_table column errors - delete

    def test_delete_api_feature_table_column_error_400_bad_request_invalid_column_name(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        self.tester.api_feature_table_column_delete_error_400_bad_request(f_table_name='layer_1003', column_name='id')
        self.tester.api_feature_table_column_delete_error_400_bad_request(f_table_name='layer_1003', column_name='geom')
        self.tester.api_feature_table_column_delete_error_400_bad_request(f_table_name='layer_1003', column_name='changeset_id')
        self.tester.api_feature_table_column_delete_error_400_bad_request(f_table_name='layer_1003', column_name='geom')

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_feature_table_column_error_401_unauthorized_user_without_login(self):
        self.tester.api_feature_table_column_delete_error_401_unauthorized(f_table_name='layer_1003',
                                                                           column_name="start_date")

    def test_delete_api_feature_table_column_error_403_forbidden_invalid_user_tries_to_manage(self):
        self.tester.auth_login("miguel@admin.com", "miguel")

        self.tester.api_feature_table_column_delete_error_403_forbidden(f_table_name='layer_1002',
                                                                        column_name="start_date")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_feature_table_column_error_404_not_found(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # invalid f_table_name
        self.tester.api_feature_table_column_delete_error_404_not_found(f_table_name='addresses',
                                                                        column_name="start_date")
        # invalid column name
        self.tester.api_feature_table_column_delete_error_404_not_found(f_table_name='layer_1002',
                                                                        column_name="name")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
