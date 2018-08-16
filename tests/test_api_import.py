#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint

from unittest import TestCase
from util.tester import UtilTester


class TestAPIImport(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        self.folder_name = "files/"
        self.folder_name_shp_originais = "files/shp_originais/"
        self.f_table_name = "points_" + str(randint(0, 100))

        ##################################################
        # create a new layer
        ##################################################
        layer = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': self.f_table_name, 'name': 'Points',
                           'description': '', 'source_description': '',
                           'reference': [1050], 'keyword': [1041]}
        }
        layer = self.tester.api_layer_create(layer)
        self.layer_id = layer["properties"]["layer_id"]

        ##################################################
        # create a new changeset
        ##################################################
        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': self.layer_id, 'description': 'Import points.shp'},
            'type': 'Changeset'
        }
        changeset = self.tester.api_changeset_create(changeset)
        self.changeset_id = changeset["properties"]["changeset_id"]

    def tearDown(self):
        ##################################################
        # remove the layer
        ##################################################
        # CLOSE THE CHANGESET
        self.tester.api_changeset_close(changeset_id=self.changeset_id)

        # DELETE THE CHANGESET (the changeset is automatically removed when delete a layer)
        # self.tester.api_changeset_delete(changeset_id=changeset_id)

        # REMOVE THE layer AFTER THE TESTS
        self.tester.api_layer_delete(self.layer_id)

        # it is not possible to find the layer that just deleted
        self.tester.api_layer_error_404_not_found(layer_id=self.layer_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    # import - create

    def test_post_import_shp_point(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "points.zip"
        with open(self.folder_name + file_name, mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name, file_name=file_name,
                                              changeset_id=self.changeset_id)

    # the tests under are with shapefile from internet

    def test_post_import_shp_asb_cemiterio(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "asb_cemiterio.zip"
        with open(self.folder_name_shp_originais + file_name, mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name, file_name=file_name,
                                              changeset_id=self.changeset_id)

    def test_post_import_shp_asb_dep_abast_agua(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "asb_dep_abast_agua.zip"
        with open(self.folder_name_shp_originais + file_name, mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name, file_name=file_name,
                                              changeset_id=self.changeset_id)

    """
    # the tests under are manual tests
        
    def test_post_import_shp_ref_urbana_2013(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "ref_urbana_2013.zip"
        with open(self.folder_name_shp_originais + 'shp_pesado/' +  file_name, mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name, file_name=file_name,
                                              changeset_id=self.changeset_id)
    
    def test_post_import_shp_sp_mun(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "sp_mun.zip"
        with open(self.folder_name_shp_originais + 'shp_pesado/' + file_name, mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name, file_name=file_name,
                                              changeset_id=self.changeset_id)
    
    def test_post_import_shp_sp_mun97_region(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "sp_mun97_region.zip"
        with open(self.folder_name_shp_originais + 'shp_pesado/' + file_name, mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name, file_name=file_name,
                                              changeset_id=self.changeset_id)
    
    def test_post_import_shp_ugrhi5_base_cont(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "ugrhi5_base_cont.zip"
        with open(self.folder_name_shp_originais + 'shp_pesado/' + file_name, mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name, file_name=file_name,
                                              changeset_id=self.changeset_id)
    
    def test_post_import_shp_teste_peso_file_with_98_mb(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "teste_peso.zip"
        with open(self.folder_name_shp_originais + 'shp_pesado/' + 'shp_pesado/' + file_name, mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name, file_name=file_name,
                                              changeset_id=self.changeset_id)
    """


class TestAPIImportError(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        self.folder_name = "files/"
        self.f_table_name = "layer_1003"
        self.changeset_id = 1005

    def tearDown(self):
        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    # import - create error

    def test_post_import_shp_error_400_bad_request_zip_without_shapefile(self):
        ##################################################
        # try to import the shapefile, but the zip doesn't have a shapefile
        ##################################################
        file_name = "folder_with_nothing.zip"

        with open(self.folder_name + file_name, mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_400_bad_request(binary_file_content, f_table_name=self.f_table_name,
                                                                    file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_error_400_bad_request_file_name_is_not_zip(self):
        ##################################################
        # try to import the shapefile, but the zip doesn't have a shapefile
        ##################################################
        file_name = "folder_with_nothing.zip"

        with open(self.folder_name + file_name, mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_400_bad_request(binary_file_content, f_table_name=self.f_table_name,
                                                                    file_name="folder_with_nothing",
                                                                    changeset_id=self.changeset_id)

    def test_post_import_shp_error_400_bad_request_argument_is_missing(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "points.zip"

        with open(self.folder_name + file_name, mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            # try to import without binary_file_content
            self.tester.api_import_shp_create_error_400_bad_request("", f_table_name=self.f_table_name,
                                                                    file_name=file_name, changeset_id=self.changeset_id)

            # try to import without f_table_name
            self.tester.api_import_shp_create_error_400_bad_request(binary_file_content,
                                                                    file_name=file_name, changeset_id=self.changeset_id)

            # try to import without file_name
            self.tester.api_import_shp_create_error_400_bad_request(binary_file_content, f_table_name=self.f_table_name,
                                                                    changeset_id=self.changeset_id)

            # try to import without changeset_id
            self.tester.api_import_shp_create_error_400_bad_request(binary_file_content, f_table_name=self.f_table_name,
                                                                    file_name=file_name)

    def test_post_import_shp_error_403_forbidden_invalid_user_tries_to_create_a_feature_table(self):
        self.f_table_name = "layer_1002"

        file_name = "points.zip"

        with open(self.folder_name + file_name, mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_403_forbidden(binary_file_content, f_table_name=self.f_table_name,
                                                                  file_name=file_name,changeset_id=self.changeset_id)

    def test_post_import_shp_error_404_not_found_f_table_name_doesnt_exist(self):
        self.f_table_name = "address"

        file_name = "points.zip"

        with open(self.folder_name + file_name, mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_404_not_found(binary_file_content, f_table_name=self.f_table_name,
                                                                  file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_error_409_conflict_file_is_not_a_zip_file(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        wrong_file_name = "points.zip"

        with open(self.folder_name + 'text.txt', mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_409_conflict(binary_file_content, f_table_name=self.f_table_name,
                                                                 file_name=wrong_file_name, changeset_id=self.changeset_id)
    
    def test_post_import_shp_error_500_internal_server_error_OGR_was_not_able_to_import(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "shopping_2014.zip"

        with open(self.folder_name + 'shp_originais/' + file_name, mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_500_internal_server_error(binary_file_content, f_table_name=self.f_table_name,
                                                                              file_name=file_name, changeset_id=self.changeset_id)


class TestAPIImportErrorWithoutLogin(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        self.folder_name = "files/"
        self.f_table_name = "points"
        self.changeset_id = 1005

    # import - create error

    def test_post_import_shp_error_401_unauthorized(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "points.zip"

        with open(self.folder_name + file_name, mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_401_unauthorized(binary_file_content, f_table_name=self.f_table_name,
                                                                     file_name=file_name, changeset_id=self.changeset_id)


# It is not necessary to pyt the main() of unittest here,
# because this file will be call by run_tests.py
