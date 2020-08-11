#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path as os_path

from random import randint
from unittest import TestCase

from util.tester import UtilTester
from util.common import FILES_PATH


os_path_sep_join = os_path.sep.join


class TestAPIImport(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

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
            'properties': {'changeset_id': -1, 'layer_id': self.layer_id},
            'type': 'Changeset'
        }
        self.changeset_id = self.tester.api_changeset_create(changeset)

    def tearDown(self):
        ##################################################
        # remove the layer
        ##################################################
        # CLOSE THE CHANGESET
        close_changeset = {
            'properties': {'changeset_id': self.changeset_id, 'description': 'Import points.shp'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        # DELETE THE CHANGESET (the changeset is automatically removed when delete a layer)
        # self.tester.api_changeset_delete(changeset_id=changeset_id)

        # REMOVE THE layer AFTER THE TESTS
        self.tester.api_layer_delete(self.layer_id)

        # it is not possible to find the layer that just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_layer(expected, layer_id=self.layer_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    # import - create

    def test_post_import_shp_places_5_points_4326(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "places_5_points_4326.zip"
        with open(os_path_sep_join([FILES_PATH, file_name]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
                                              file_name=file_name, changeset_id=self.changeset_id)

    # dados_prefeitura_sp

    def test_post_import_shp_DEINFO_CENTRAIS_MECANIZADAS_5533(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "DEINFO_CENTRAIS_MECANIZADAS_5533.zip"
        file_name_path = "shp_originals/dados_prefeitura_sp/ok/" + file_name
        with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
                                              file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_LAYER_BACIA_HIDROGRAFIA_29193(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "LAYER_BACIA_HIDROGRAFIA_29193.zip"
        file_name_path = "shp_originals/dados_prefeitura_sp/ok/" + file_name
        with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
                                              file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_LAYER_CEMITERIOS_29193(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "LAYER_CEMITERIOS_29193.zip"
        file_name_path = "shp_originals/dados_prefeitura_sp/ok/" + file_name
        with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
                                              file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_LAYER_CENTRAL_COOPERATIVA_4326(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "LAYER_CENTRAL_COOPERATIVA_4326.zip"
        file_name_path = "shp_originals/dados_prefeitura_sp/ok/" + file_name
        with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
                                              file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_LAYER_DISTRITO_SP_29193(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "LAYER_DISTRITO_SP_29193.zip"
        file_name_path = "shp_originals/dados_prefeitura_sp/ok/" + file_name
        with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
                                              file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_shopping_2014_29193(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "shopping_2014_29193.zip"
        file_name_path = "shp_originals/dados_prefeitura_sp/" + file_name
        with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
                                              file_name=file_name, changeset_id=self.changeset_id)

    # Ferla's Shapefile files

    def test_post_import_shp_Area_alagada_4326(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "Area alagada_4326.zip"
        file_name_path = "shp_originals/ferla/" + file_name
        with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
                                              file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_SF_4326(self):
        file_name = "SF.zip"
        file_name_path = "shp_originals/ferla/with_myshapes_folder/" + file_name
        with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
                                              file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_2019_09_26_cn_original(self):
        file_name = "2019_09_26_cn_original.zip"
        file_name_path = "shp_originals/ferla/" + file_name
        with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
                                              file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_Sarah_Feldman_adaptada_atributos_com_acentos_4326(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "Sarah_Feldman_adaptada_atributos_com_acentos_4326.zip"
        file_name_path = "shp_originals/ferla/" + file_name
        with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
                                              file_name=file_name, changeset_id=self.changeset_id)

    # def test_post_import_shp_Sarah_Feldman_adaptada_4326_sem_acento_coluna(self):
    #     ##################################################
    #     # import the shapefile with the created layer (the feature table will be the shapefile)
    #     ##################################################
    #     file_name = "Sarah_Feldman_adaptada_4326_sem_acento_coluna.zip"
    #     file_name_path = "shp_originals/ferla/" + file_name
    #     with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
    #         binary_file_content = file.read()
    #
    #         self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
    #                                           file_name=file_name, changeset_id=self.changeset_id)

    # Cintia's Shapefile files

    def test_post_import_shp_homosp_4326(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "homosp.zip"
        file_name_path = "shp_originals/cintia/" + file_name
        with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
                                              file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_industrias_do_bom_retiro_4326(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "industrias_do_bom_retiro.zip"
        file_name_path = "shp_originals/cintia/" + file_name
        with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
                                              file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_Recenseamento_Demographico_do_Estado_de_Sao_Paulo_4326(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "Recenseamento Demographico do Estado de Sao Paulo.zip"
        file_name_path = "shp_originals/cintia/" + file_name
        with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
                                              file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_Teste_boletins_4326(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "Teste boletins.zip"
        file_name_path = "shp_originals/cintia/" + file_name
        with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
                                              file_name=file_name, changeset_id=self.changeset_id)

    # Cintia's test Shapefile files

    def test_post_import_shp_camadas_de_teste_teste_em_3857(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "teste em 3857.zip"
        file_name_path = "shp_originals/cintia/camadas_de_teste/" + file_name
        with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
                                              file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_camadas_de_teste_teste_em_4326(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "teste em 4326.zip"
        file_name_path = "shp_originals/cintia/camadas_de_teste/" + file_name
        with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
                                              file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_camadas_de_teste_teste_reprojetado_de_3857_para_4326(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "teste_reprojetado_de_3857_para_4326.zip"
        file_name_path = "shp_originals/cintia/camadas_de_teste/" + file_name
        with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
                                              file_name=file_name, changeset_id=self.changeset_id)

    # def test_post_import_shp_Area_alagada_problema(self):
    #     ##################################################
    #     # import the shapefile with the created layer (the feature table will be the shapefile)
    #     ##################################################
    #     file_name = "Area alagada_problema.zip"
    #     file_name_path = "shp_originals/ferla/" + file_name
    #     with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
    #         binary_file_content = file.read()

    #         self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
    #                                           file_name=file_name, changeset_id=self.changeset_id)


"""
class TestAPIManualTests(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        self.folder_name_shp_originals = "files/shp_originals/"
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
            'properties': {'changeset_id': -1, 'layer_id': self.layer_id},
            'type': 'Changeset'
        }
        self.changeset_id = self.tester.api_changeset_create(changeset)

    def tearDown(self):
        ##################################################
        # remove the layer
        ##################################################
        # CLOSE THE CHANGESET
        close_changeset = {
            'properties': {'changeset_id': self.changeset_id, 'description': 'Import points.shp'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        # DELETE THE CHANGESET (the changeset is automatically removed when delete a layer)
        # self.tester.api_changeset_delete(changeset_id=changeset_id)

        # REMOVE THE layer AFTER THE TESTS
        self.tester.api_layer_delete(self.layer_id)

        # it is not possible to find the layer that just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_layer(expected, layer_id=self.layer_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    # the tests under are manual tests

    # def test_post_import_shp_ref_urbana_2013(self):
    #     ##################################################
    #     # import the shapefile with the created layer (the feature table will be the shapefile)
    #     ##################################################
    #     file_name = "ref_urbana_2013.zip"
    #     with open(self.folder_name_shp_originals + 'shp_pesado/' +  file_name, mode='rb') as file:  # rb = read binary
    #         binary_file_content = file.read()
    #
    #         self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name, file_name=file_name,
    #                                           changeset_id=self.changeset_id)
    #
    # def test_post_import_shp_sp_mun(self):
    #     ##################################################
    #     # import the shapefile with the created layer (the feature table will be the shapefile)
    #     ##################################################
    #     file_name = "sp_mun.zip"
    #     with open(self.folder_name_shp_originals + 'shp_pesado/' + file_name, mode='rb') as file:  # rb = read binary
    #         binary_file_content = file.read()
    #
    #         self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name, file_name=file_name,
    #                                           changeset_id=self.changeset_id)
    #
    # def test_post_import_shp_sp_mun97_region(self):
    #     ##################################################
    #     # import the shapefile with the created layer (the feature table will be the shapefile)
    #     ##################################################
    #     file_name = "sp_mun97_region.zip"
    #     with open(self.folder_name_shp_originals + 'shp_pesado/' + file_name, mode='rb') as file:  # rb = read binary
    #         binary_file_content = file.read()
    #
    #         self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name, file_name=file_name,
    #                                           changeset_id=self.changeset_id)
    #
    # def test_post_import_shp_ugrhi5_base_cont(self):
    #     ##################################################
    #     # import the shapefile with the created layer (the feature table will be the shapefile)
    #     ##################################################
    #     file_name = "ugrhi5_base_cont.zip"
    #     with open(self.folder_name_shp_originals + 'shp_pesado/' + file_name, mode='rb') as file:  # rb = read binary
    #         binary_file_content = file.read()
    #
    #         self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name, file_name=file_name,
    #                                           changeset_id=self.changeset_id)
    #
    # def test_post_import_shp_teste_peso_file_with_98_mb(self):
    #     ##################################################
    #     # import the shapefile with the created layer (the feature table will be the shapefile)
    #     ##################################################
    #     file_name = "teste_peso.zip"
    #     with open(self.folder_name_shp_originals + 'shp_pesado/' + file_name, mode='rb') as file:  # rb = read binary
    #         binary_file_content = file.read()
    #
    #         self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name, file_name=file_name,
    #                                           changeset_id=self.changeset_id)

    # dá erro de importação na OGR relacionado a encoding, porém a OGR não retorna um status de erro para
    # o console. Portanto, o VGIMWS não consegue saber que foi um erro.
    # def test_post_import_shp_DEINFO_CORTICO_2015(self):
    #     ##################################################
    #     # import the shapefile with the created layer (the feature table will be the shapefile)
    #     ##################################################
    #     file_name = "DEINFO_CORTICO_2015.zip"
    #     file_name_path = "shp_originals/dados_prefeitura_sp/dentro_sp/" + file_name
    #     with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
    #         binary_file_content = file.read()
    #
    #         self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
    #                                           file_name=file_name,
    #                                           changeset_id=self.changeset_id)

    # a função ST_Contains diz que esse Shapefile está fora do Bounding Box de SP.
    # def test_post_import_shp_DEINFO_DECLIVIDADE(self):
    #     ##################################################
    #     # import the shapefile with the created layer (the feature table will be the shapefile)
    #     ##################################################
    #     file_name = "DEINFO_DECLIVIDADE.zip"
    #     file_name_path = "shp_originals/dados_prefeitura_sp/dentro_sp/" + file_name
    #     with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
    #         binary_file_content = file.read()
    #
    #         self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name,
    #                                           file_name=file_name,
    #                                           changeset_id=self.changeset_id)
"""


class TestAPIImportError(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        self.f_table_name = "layer_test"

        ##################################################
        # create a new layer
        ##################################################
        self.layer = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': self.f_table_name, 'name': 'Points',
                           'description': '', 'source_description': '',
                           'reference': [1050], 'keyword': [1041]}
        }
        self.layer = self.tester.api_layer_create(self.layer)
        self.layer_id = self.layer["properties"]["layer_id"]

        ##################################################
        # create a new changeset
        ##################################################
        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': self.layer_id},
            'type': 'Changeset'
        }
        self.changeset_id = self.tester.api_changeset_create(changeset)

    def tearDown(self):
        ##################################################
        # remove the layer
        ##################################################
        # CLOSE THE CHANGESET
        close_changeset = {
            'properties': {'changeset_id': self.changeset_id, 'description': 'Import'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        # REMOVE THE layer AFTER THE TESTS
        self.tester.api_layer_delete(self.layer_id)

        # it is not possible to find the layer that just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_layer(expected, layer_id=self.layer_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    # import - create error

    def test_post_import_shp_error_400_bad_request_file_name_is_not_zip(self):
        ##################################################
        # try to import the shapefile, but the zip doesn't have a shapefile
        ##################################################
        file_name = "folder_with_nothing.zip"

        with open(os_path_sep_join([FILES_PATH, file_name]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_400_bad_request(binary_file_content, f_table_name=self.f_table_name,
                                                                    file_name="folder_with_nothing",
                                                                    changeset_id=self.changeset_id)

    def test_post_import_shp_error_400_bad_request_argument_is_missing(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "points.zip"

        with open(os_path_sep_join([FILES_PATH, file_name]), mode='rb') as file:  # rb = read binary
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

    def test_post_import_shp_error_400_bad_request_f_table_name_has_special_chars_or_it_starts_with_number(self):
        ##################################################
        # try to import the shapefile, but the zip doesn't have a shapefile
        ##################################################
        file_name = "points.zip"

        list_f_table_name = [
            "*)layer", "lay+-er", "layer_(/", "837_layer", "0_layer",
            " new_layer", "new_layer ", "new layer"
        ]

        for f_table_name in list_f_table_name:
            with open(os_path_sep_join([FILES_PATH, file_name]), mode='rb') as file:  # rb = read binary
                binary_file_content = file.read()

                self.tester.api_import_shp_create_error_400_bad_request(binary_file_content, f_table_name=f_table_name,
                                                                        file_name="points",
                                                                        changeset_id=self.changeset_id)

    def test_post_import_shp_error_400_bad_request_invalid_prj_file_epsg_not_found(self):
        file_name = "places_5_points_with_bad_prj.zip"
        with open(os_path_sep_join([FILES_PATH, file_name]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_400_bad_request(binary_file_content, f_table_name=self.f_table_name,
                                                                    file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_error_400_bad_request_prj_is_empty(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "points__prj_is_empty.zip"

        with open(os_path_sep_join([FILES_PATH, file_name]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_400_bad_request(binary_file_content, f_table_name=self.f_table_name,
                                                                    file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_error_403_forbidden_invalid_user_tries_to_create_a_feature_table(self):
        f_table_name = "layer_1002"

        file_name = "points.zip"

        with open(os_path_sep_join([FILES_PATH, file_name]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_403_forbidden(binary_file_content, f_table_name=f_table_name,
                                                                  file_name=file_name,changeset_id=self.changeset_id)

    def test_post_import_shp_error_404_not_found_f_table_name_doesnt_exist(self):
        f_table_name = "address"

        file_name = "points.zip"

        with open(os_path_sep_join([FILES_PATH, file_name]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_404_not_found(binary_file_content, f_table_name=f_table_name,
                                                                  file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_error_404_not_found_not_found_shp(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "points_without_shp.zip"

        with open(os_path_sep_join([FILES_PATH, file_name]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_404_not_found(binary_file_content, f_table_name=self.f_table_name,
                                                                  file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_error_404_not_found_not_found_prj(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "points_without_prj.zip"

        with open(os_path_sep_join([FILES_PATH, file_name]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_404_not_found(binary_file_content, f_table_name=self.f_table_name,
                                                                  file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_error_404_not_found_not_found_dbf(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "points_without_dbf.zip"

        with open(os_path_sep_join([FILES_PATH, file_name]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_404_not_found(binary_file_content, f_table_name=self.f_table_name,
                                                                  file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_error_404_not_found_not_found_shx(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "points_without_shx.zip"

        with open(os_path_sep_join([FILES_PATH, file_name]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_404_not_found(binary_file_content, f_table_name=self.f_table_name,
                                                                  file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_error_409_conflict_file_is_not_a_zip_file(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        wrong_file_name = "points.zip"

        with open(os_path_sep_join([FILES_PATH, 'text.txt']), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_409_conflict(binary_file_content, f_table_name=self.f_table_name,
                                                                 file_name=wrong_file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_error_409_conflict_f_table_name_is_reserved_name(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "points.zip"
        list_invalid_f_table_name = ["abort", "access"]

        for invalid_f_table_name in list_invalid_f_table_name:
            with open(os_path_sep_join([FILES_PATH, file_name]), mode='rb') as file:  # rb = read binary
                binary_file_content = file.read()

                self.tester.api_import_shp_create_error_409_conflict(binary_file_content, file_name=file_name,
                                                                     f_table_name=invalid_f_table_name,
                                                                     changeset_id=self.changeset_id)

    def test_post_import_shp_error_409_conflict_shapefile_is_not_inside_default_city(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "points.zip"
        with open(os_path_sep_join([FILES_PATH, file_name]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_409_conflict(binary_file_content, f_table_name=self.f_table_name,
                                                                 file_name=file_name, changeset_id=self.changeset_id)

    def test_post_import_shp_error_500_internal_server_error_dbf_file_has_an_empty_column(self):
        ##################################################
        # the Shapefile has an empty column name and fiona and OGR don't understand it
        ##################################################
        file_name = "SarahFeldman_completa_arrumada__dbf_has_an_empty_column.zip"
        file_name_path = "other/" + file_name
        with open(os_path_sep_join([FILES_PATH, file_name_path]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_500_internal_server_error(binary_file_content, f_table_name=self.f_table_name,
                                                                              file_name=file_name, changeset_id=self.changeset_id)

    # def test_post_import_shp_error_500_internal_server_there_are_invalid_geometries_inside_the_shapefile(self):
    #     f_table_name = "layer_test"
    #
    #     ##################################################
    #     # create a new layer
    #     ##################################################
    #     layer = {
    #         'type': 'Layer',
    #         'properties': {'layer_id': -1, 'f_table_name': f_table_name, 'name': 'Points',
    #                        'description': '', 'source_description': '',
    #                        'reference': [1050], 'keyword': [1041]}
    #     }
    #     layer = self.tester.api_layer_create(layer)
    #     layer_id = layer["properties"]["layer_id"]
    #
    #     ##################################################
    #     # create a new changeset
    #     ##################################################
    #     changeset = {
    #         'properties': {'changeset_id': -1, 'layer_id': layer_id},
    #         'type': 'Changeset'
    #     }
    #     self.changeset_id = self.tester.api_changeset_create(changeset)
    #
    #     ##################################################
    #     # import the shapefile with the created layer (the feature table will be the shapefile)
    #     ##################################################
    #     file_name = "sp_bacia_hidrografica.zip"
    #
    #     with open(self.folder_name_shp_originals + file_name, mode='rb') as file:  # rb = read binary
    #         binary_file_content = file.read()
    #
    #         self.tester.api_import_shp_create_error_500_internal_server_error(binary_file_content,
    #                                                                           f_table_name=f_table_name,
    #                                                                           file_name=file_name,
    #                                                                           changeset_id=changeset_id)
    #
    #     ##################################################
    #     # remove the layer
    #     ##################################################
    #     # CLOSE THE CHANGESET
    #     close_changeset = {
    #         'properties': {'changeset_id': changeset_id, 'description': 'Import points.shp'},
    #         'type': 'ChangesetClose'
    #     }
    #     self.tester.api_changeset_close(close_changeset)
    #
    #     # REMOVE THE layer AFTER THE TESTS
    #     self.tester.api_layer_delete(layer_id)
    #
    #     # it is not possible to find the layer that just deleted
    #     expected = {'type': 'FeatureCollection', 'features': []}
    #     self.tester.api_layer(expected, layer_id=layer_id)


class TestAPIImportErrorWithoutLogin(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        self.f_table_name = "points"
        self.changeset_id = 1005

    # import - create error

    def test_post_import_shp_error_401_unauthorized(self):
        ##################################################
        # import the shapefile with the created layer (the feature table will be the shapefile)
        ##################################################
        file_name = "points.zip"

        with open(os_path_sep_join([FILES_PATH, file_name]), mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create_error_401_unauthorized(binary_file_content, f_table_name=self.f_table_name,
                                                                     file_name=file_name, changeset_id=self.changeset_id)


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
