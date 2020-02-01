#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import path as sys_path
from os import path as os_path
from unittest import TestCase, main

# Get the main folder (vgiws)
PROJECT_PATH = os_path.sep.join(os_path.abspath(__file__).split(os_path.sep)[:-3])
# Put the project path in sys path to use the folders (modules, settings, etc) as modules
sys_path.append(os_path.abspath(PROJECT_PATH))

from tests.util.tester import UtilTester
from models.db_connection import PGSQLConnection


def remove_comments_from_sql_file(sql_file):
    lines = sql_file.split("\n")
    lines_copy = list(lines)  # create a copy to iterate inside it

    # iterate reversed
    for i in range(len(lines_copy) - 1, -1, -1):
        line = lines_copy[i]

        # if there is a comment in line, so remove it in original line
        if "--" in line:
            del lines[i]

        # if there is nothing in line, so remove it in original line
        if "" == line:
            del lines[i]

    sql_file = "\n".join(lines)

    return sql_file


def remove_special_characters(text):
    # remove special character
    text = text.replace("\ufeff", "")
    text = text.replace("\n\n\n", "").replace("\n\n", "")

    return text


def arrange_the_relationship_of_feature_tables():
    __PATH_SQL_RELATIONSHIP_FILE__ = PROJECT_PATH + "/files/db/sql/secreto/05_arrange_relationship_production_values.sql"

    PGSQLConn = PGSQLConnection.get_instance(False, True)

    with open(__PATH_SQL_RELATIONSHIP_FILE__, 'r') as relationship_file:
        relationship_file = relationship_file.read()

        relationship_file = remove_comments_from_sql_file(relationship_file)
        relationship_file = remove_special_characters(relationship_file)

        PGSQLConn.execute(relationship_file, is_transaction=True)

        PGSQLConn.commit()

    # close DB
    # PGSQLConn.close()


class UploadOldDBInNewDB(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN PAULICEIA
        self.tester.auth_login("<MY EMAIL HERE>", "<MY PASSWORD HERE>")

        ####################################################################################################
        # prepare to add the places_pilot_area
        ####################################################################################################

        self.f_table_name_places = "places_pilot_area"

        ##################################################
        # create a new layer
        ##################################################
        layer_places = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': self.f_table_name_places, 'name': 'Places Pilot Area',
                           'description': '', 'source_description': '',
                           'reference': [], 'keyword': [1041]}
        }
        layer_places = self.tester.api_layer_create(layer_places)
        self.layer_id_places = layer_places["properties"]["layer_id"]

        ##################################################
        # create a new changeset
        ##################################################
        changeset_places = {
            'properties': {'changeset_id': -1, 'layer_id': self.layer_id_places},
            'type': 'Changeset'
        }
        changeset_places = self.tester.api_changeset_create(changeset_places)
        self.changeset_id_places = changeset_places["properties"]["changeset_id"]

        ####################################################################################################
        # prepare to add the places_pilot_area
        ####################################################################################################

        self.f_table_name_streets = "streets_pilot_area"

        ##################################################
        # create a new layer
        ##################################################
        layer_streets = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': self.f_table_name_streets, 'name': 'Streets Pilot Area',
                           'description': '', 'source_description': '',
                           'reference': [], 'keyword': [1040]}
        }
        layer_streets = self.tester.api_layer_create(layer_streets)
        self.layer_id_streets = layer_streets["properties"]["layer_id"]

        ##################################################
        # create a new changeset
        ##################################################
        changeset_streets = {
            'properties': {'changeset_id': -1, 'layer_id': self.layer_id_streets},
            'type': 'Changeset'
        }
        changeset_streets = self.tester.api_changeset_create(changeset_streets)
        self.changeset_id_streets = changeset_streets["properties"]["changeset_id"]

        ####################################################################################################
        # prepare to add the places_pilot_area_02
        ####################################################################################################

        self.f_table_name_places_pilot_area_02 = "places_pilot_area2"

        ##################################################
        # create a new layer
        ##################################################
        layer_places_pilot_area_02 = {
            'type': 'Layer',
            'properties': {'layer_id': -1, 'f_table_name': self.f_table_name_places_pilot_area_02,
                           'name': 'Places Pilot Area 02', 'description': '', 'source_description': '',
                           'reference': [], 'keyword': [1041]}
        }
        layer_places_pilot_area_02 = self.tester.api_layer_create(layer_places_pilot_area_02)
        self.layer_id_places_pilot_area_02 = layer_places_pilot_area_02["properties"]["layer_id"]

        ##################################################
        # create a new changeset
        ##################################################
        changeset_places_pilot_area_02 = {
            'properties': {'changeset_id': -1, 'layer_id': self.layer_id_places_pilot_area_02},
            'type': 'Changeset'
        }
        changeset_places_pilot_area_02 = self.tester.api_changeset_create(changeset_places_pilot_area_02)
        self.changeset_id_places_pilot_area_02 = changeset_places_pilot_area_02["properties"]["changeset_id"]

    def tearDown(self):
        # close the changesets
        close_changeset = {
            'properties': {'changeset_id': self.changeset_id_places, 'description': 'importing places...'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        close_changeset = {
            'properties': {'changeset_id': self.changeset_id_streets, 'description': 'importing streets...'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        close_changeset = {
            'properties': {'changeset_id': self.changeset_id_places_pilot_area_02, 'description': 'importing places 2...'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

        arrange_the_relationship_of_feature_tables()

    # import - create

    def test_post_import_shp(self):
        epsg = 4326

        ####################################################################################################
        # import the places_pilot_area
        ##################################################
        with open(PROJECT_PATH+"/files/production/places_pilot_area.zip", mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name_places,
                                              file_name="places_pilot_area.zip",
                                              changeset_id=self.changeset_id_places, epsg=epsg)

        ##################################################
        # create the time columns for the layer above
        ##################################################
        temporal_columns_places = {
            'properties': {
                'f_table_name': self.f_table_name_places,
                'start_date': '1868-01-01', 'end_date': '1940-12-31',
                'start_date_column_name': 'first_year', 'end_date_column_name': 'last_year',
                'start_date_mask_id': 3, 'end_date_mask_id': 3},
            'type': 'TemporalColumns'
        }

        self.tester.api_temporal_columns_create(temporal_columns_places)

        ##################################################
        # add users as collaborator of the layer
        ##################################################
        for index in range(1, 15):
            if index == 3:  # user 3 has already added as user creator, so it is not needed to add it again
                continue
            user_layer = {
                'properties': {'user_id': index, 'layer_id': self.layer_id_places, 'is_the_creator': False},
                'type': 'UserLayer'
            }
            self.tester.api_user_layer_create(user_layer)

        # add the user rodrigo as collaborator
        user_layer = {
            'properties': {'user_id': 1000000000, 'layer_id': self.layer_id_places, 'is_the_creator': False},
            'type': 'UserLayer'
        }
        self.tester.api_user_layer_create(user_layer)

        ####################################################################################################
        # import the streets_pilot_area
        ##################################################
        with open(PROJECT_PATH+"/files/production/streets_pilot_area.zip", mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name_streets,
                                              file_name="streets_pilot_area.zip",
                                              changeset_id=self.changeset_id_streets, epsg=epsg)

        ##################################################
        # create the time columns for the layer above
        ##################################################
        temporal_columns_streets = {
            'properties': {
                'f_table_name': self.f_table_name_streets,
                'start_date': '1868-01-01', 'end_date': '1940-12-31',
                'start_date_column_name': 'first_year', 'end_date_column_name': 'last_year',
                'start_date_mask_id': 3, 'end_date_mask_id': 3},
            'type': 'TemporalColumns'
        }

        self.tester.api_temporal_columns_create(temporal_columns_streets)

        ##################################################
        # add users as collaborator of the layer
        ##################################################
        for index in range(1, 15):
            if index == 3:  # user 3 has already added as user creator, so it is not needed to add it again
                continue
            user_layer = {
                'properties': {'user_id': index, 'layer_id': self.layer_id_streets, 'is_the_creator': False},
                'type': 'UserLayer'
            }
            self.tester.api_user_layer_create(user_layer)

        # add the user rodrigo as collaborator
        user_layer = {
            'properties': {'user_id': 1000000000, 'layer_id': self.layer_id_streets, 'is_the_creator': False},
            'type': 'UserLayer'
        }
        self.tester.api_user_layer_create(user_layer)

        ####################################################################################################
        # import the places_pilot_area_02
        ##################################################
        with open(PROJECT_PATH + "/files/production/places_pilot_area_02.zip", mode='rb') as file:  # rb = read binary
            binary_file_content = file.read()

            self.tester.api_import_shp_create(binary_file_content, f_table_name=self.f_table_name_places_pilot_area_02,
                                              file_name="places_zero.zip",
                                              changeset_id=self.changeset_id_places_pilot_area_02, epsg=epsg)

        ##################################################
        # create the time columns for the layer above
        ##################################################
        temporal_columns_places_zero = {
            'properties': {
                'f_table_name': self.f_table_name_places_pilot_area_02,
                'start_date': '1868-01-01', 'end_date': '1940-12-31',
                'start_date_column_name': 'first_year', 'end_date_column_name': 'last_year',
                'start_date_mask_id': 3, 'end_date_mask_id': 3},
            'type': 'TemporalColumns'
        }

        self.tester.api_temporal_columns_create(temporal_columns_places_zero)

        ##################################################
        # add users as collaborator of the layer
        ##################################################
        for index in range(1, 15):
            if index == 3:  # user 3 has already added as user creator, so it is not needed to add it again
                continue
            user_layer = {
                'properties': {'user_id': index, 'layer_id': self.layer_id_places_pilot_area_02, 'is_the_creator': False},
                'type': 'UserLayer'
            }
            self.tester.api_user_layer_create(user_layer)

        # add the user rodrigo as collaborator
        user_layer = {
            'properties': {'user_id': 1000000000, 'layer_id': self.layer_id_places_pilot_area_02, 'is_the_creator': False},
            'type': 'UserLayer'
        }
        self.tester.api_user_layer_create(user_layer)


if __name__ == '__main__':
    main()
