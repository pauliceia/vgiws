#!/usr/bin/env python
# -*- coding: utf-8 -*-


from unittest import TestCase
from util.tester import UtilTester


class TestAPIImport(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        self.folder_name = "files/"

    # import - create

    def test_post_import_shp(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        f_table_name = "points"

        ##################################################
        # create a new layer
        ##################################################
        resource = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': f_table_name, 'name': 'Addresses in 1930',
                           'description': '', 'source_description': '',
                           'reference': [1050], 'keyword': [1041]}
        }
        resource = self.tester.api_layer_create(resource, is_to_create_feature_table=False)

        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "points.zip"
        with open(self.folder_name + file_name, mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=f_table_name, file_name=file_name)

        ##################################################
        # remove the layer
        ##################################################
        # get the id of layer to REMOVE it
        resource_id = resource["properties"]["layer_id"]

        # REMOVE THE layer AFTER THE TESTS
        self.tester.api_layer_delete(resource_id)

        # it is not possible to find the layer that just deleted
        self.tester.api_layer_error_404_not_found(layer_id=resource_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPIImportError(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        self.folder_name = "files/"

    # import - create

    def test_post_import_shp_error_400_bad_request_zip_without_shapefile(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        f_table_name = "folder_with_nothing"

        ##################################################
        # create a new layer
        ##################################################
        resource = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': f_table_name, 'name': 'Addresses in 1930',
                           'description': '', 'source_description': '',
                           'reference': [1050], 'keyword': [1041]}
        }
        resource = self.tester.api_layer_create(resource, is_to_create_feature_table=False)

        ##################################################
        # try to import the shapefile, but the zip doesn't have a shapefile
        ##################################################
        file_name = "folder_with_nothing.zip"
        with open(self.folder_name + file_name, mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_400_bad_request(binary_file_content, f_table_name=f_table_name, 
                                                                    file_name=file_name)

        ##################################################
        # remove the layer
        ##################################################
        # get the id of layer to REMOVE it
        resource_id = resource["properties"]["layer_id"]

        # REMOVE THE layer AFTER THE TESTS
        self.tester.api_layer_delete(resource_id)

        # it is not possible to find the layer that just deleted
        self.tester.api_layer_error_404_not_found(layer_id=resource_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_import_shp_error_400_bad_request_file_name_is_not_zip(self):
        # DO LOGIN
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        f_table_name = "folder_with_nothing"

        ##################################################
        # create a new layer
        ##################################################
        resource = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': f_table_name, 'name': 'Addresses in 1930',
                           'description': '', 'source_description': '',
                           'reference': [1050], 'keyword': [1041]}
        }
        resource = self.tester.api_layer_create(resource, is_to_create_feature_table=False)

        ##################################################
        # try to import the shapefile, but the zip doesn't have a shapefile
        ##################################################
        file_name = "folder_with_nothing.zip"
        with open(self.folder_name + file_name, mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_400_bad_request(binary_file_content, f_table_name=f_table_name,
                                                                    file_name="folder_with_nothing")

        ##################################################
        # remove the layer
        ##################################################
        # get the id of layer to REMOVE it
        resource_id = resource["properties"]["layer_id"]

        # REMOVE THE layer AFTER THE TESTS
        self.tester.api_layer_delete(resource_id)

        # it is not possible to find the layer that just deleted
        self.tester.api_layer_error_404_not_found(layer_id=resource_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
