#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/


class TestAPIIntegration(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_api_integration(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        f_table_name = "addresses_1930"

        ##################################################
        # create a layer
        ##################################################
        layer = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': f_table_name, 'name': 'Addresses in 1930',
                           'description': '', 'source_description': '',
                           'reference': [], 'keyword': []}
        }
        layer = self.tester.api_layer_create(layer)

        ##################################################
        # create the feature_table for the layer above
        ##################################################
        feature_table = {
            'type': 'FeatureTable',
            'f_table_name': f_table_name,
            'properties': {'id': 'integer', 'geom': 'geometry', 'version': 'integer', 'changeset_id': 'integer',
                           'start_date': 'timestamp without time zone', 'end_date': 'timestamp without time zone',
                           'address': 'text'},
            'geometry': {
                'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
                'type': 'MULTIPOINT'
            }
        }

        self.tester.api_feature_table_create(feature_table)

        ##################################################
        # create the time columns for the layer above
        ##################################################
        temporal_columns = {
            'properties': {'f_table_name': f_table_name, 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                           'end_date_column_name': 'end_date', 'start_date_column_name': 'start_date',
                           'start_date_mask_id': 1001, 'end_date_mask_id': 1001},
            'type': 'TemporalColumns'
        }

        self.tester.api_temporal_columns_create(temporal_columns)

        ##################################################
        # update the layer
        ##################################################
        layer["properties"]["name"] = "Some addresses"
        layer["properties"]["description"] = "Addresses"
        layer["properties"]["reference"] = [1050, 1052]
        layer["properties"]["keyword"] = [1001, 1041]
        self.tester.api_layer_update(layer)

        ##################################################
        # verify if the layer, feature table and the temporal columns were modified
        ##################################################
        expected_layer = {'type': 'FeatureCollection', 'features': [layer]}
        self.tester.api_layer(expected_at_least=expected_layer, f_table_name=f_table_name)

        expected_feature_table = {'type': 'FeatureCollection', 'features': [feature_table]}
        self.tester.api_feature_table(expected_feature_table, f_table_name=f_table_name)

        expected_temporal_columns = {'type': 'FeatureCollection', 'features': [temporal_columns]}
        self.tester.api_temporal_columns(expected_temporal_columns, f_table_name=f_table_name)

        ##################################################
        # delete the layer
        ##################################################
        # get the id of layer to SEARCH AND REMOVE it
        layer_id = layer["properties"]["layer_id"]

        # REMOVE THE layer AFTER THE TESTS
        self.tester.api_layer_delete(layer_id)

        # it is not possible to find the layer that just deleted
        self.tester.api_layer_error_404_not_found(layer_id=layer_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
