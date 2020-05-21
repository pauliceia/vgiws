#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy
from unittest import TestCase

from util.tester import UtilTester


# https://realpython.com/blog/python/testing-third-party-apis-with-mocks/

class TestAPIFeature(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # feature - get

    def test_get_api_feature_return_all_features_by_f_table_name(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'end_date': '1869-12-31 00:00:00', 'version': 1, 'address': 'R. São José',
                                   'id': 1001, 'start_date': '1869-01-01 00:00:00', 'changeset_id': 1001},
                    'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
                    'type': 'Feature'
                },
                {
                    'properties': {'end_date': '1869-12-31 00:00:00', 'version': 1, 'address': 'R. Marechal Deodoro',
                                   'id': 1002, 'start_date': '1869-01-01 00:00:00', 'changeset_id': 1001},
                    'geometry': {'coordinates': [[-46.6498716962487, -23.5482894062877]], 'type': 'MultiPoint'},
                    'type': 'Feature'
                },
                {
                    'properties': {'end_date': '1875-12-31 00:00:00', 'version': 1, 'address': None, 'id': 1003,
                                   'start_date': '1875-01-01 00:00:00', 'changeset_id': 1001},
                    'geometry': {'coordinates': [[-46.6468896156385, -23.5494865576549]], 'type': 'MultiPoint'},
                    'type': 'Feature'
                }
            ]
        }

        self.tester.api_feature(expected, f_table_name="layer_1001")

        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'start_date': '1930-01-01 00:00:00', 'version': 1, 'name': 'rua boa vista',
                                   'id': 1001, 'changeset_id': 1003, 'end_date': '1940-12-31 00:00:00'},
                    'type': 'Feature',
                    'geometry': {
                        'coordinates': [[[-46.6237603488114, -23.5533938154249], [-46.6235408108831, -23.5522660084575], [-46.6233933273529, -23.5516456142714], [-46.623209681096, -23.5507601376416], [-46.622973981047, -23.5496552515087], [-46.6236497790913, -23.5484119132552]]],
                        'type': 'MultiLineString'
                    }
                },
                {
                    'properties': {'start_date': '1920-01-01 00:00:00', 'version': 1, 'name': 'rua tres de dezembro',
                                   'id': 1002, 'changeset_id': 1003, 'end_date': '1930-12-31 00:00:00'},
                    'type': 'Feature',
                    'geometry': {
                        'coordinates': [[[-46.6353540826681, -23.5450950669741], [-46.63471434053, -23.5454695514008], [-46.6343109517528, -23.5458044203441]]],
                        'type': 'MultiLineString'
                    }
                },
                {
                    'properties': {'start_date': '1930-01-01 00:00:00', 'version': 1, 'name': None, 'id': 1003,
                                   'changeset_id': 1003, 'end_date': '1930-12-31 00:00:00'},
                    'type': 'Feature',
                    'geometry': {
                        'coordinates': [[[-46.6289810574309, -23.542735394758], [-46.6267724837701, -23.5427585091922]]],
                        'type': 'MultiLineString'
                    }
                }
            ]
        }

        self.tester.api_feature(expected, f_table_name="layer_1003")

        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'MultiPolygon',
                        'coordinates': [[[[-46.6536941024203, -23.5446440934747], [-46.6536987312376, -23.5446514885665], [-46.6531421851224, -23.5427759121502], [-46.6531368207044, -23.5426136385048], [-46.6536941024203, -23.5446440934747]]]]
                    },
                    'properties': {'start_date': '1920-01', 'changeset_id': 1005, 'version': 1, 'end_date': '1940-12',
                                   'id': 1001, 'name': "Sant'Anna's Hospital"}
                },
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'MultiPolygon',
                        'coordinates': [[[[-46.6531368207044, -23.5426136385048], [-46.6526581134833, -23.5401195274321], [-46.6526581134833, -23.5401195274321], [-46.6535666865397, -23.5322186250535], [-46.6531368207044, -23.5426136385048]]]]
                    },
                    'properties': {'start_date': '1920-01', 'changeset_id': 1005, 'version': 1, 'end_date': '1940-12',
                                   'id': 1002, 'name': "Holy Mary's Hospital"}
                }
            ]
        }

        self.tester.api_feature(expected, f_table_name="layer_1005")

    def test_get_api_feature_return_all_features_by_f_table_name_and_feature_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'end_date': '1869-12-31 00:00:00', 'version': 1, 'address': 'R. São José',
                                   'id': 1001, 'start_date': '1869-01-01 00:00:00', 'changeset_id': 1001},
                    'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
                    'type': 'Feature'
                }
            ]
        }

        self.tester.api_feature(expected, f_table_name="layer_1001", feature_id="1001")

        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'start_date': '1920-01-01 00:00:00', 'version': 1, 'name': 'rua tres de dezembro',
                                   'id': 1002, 'changeset_id': 1003, 'end_date': '1930-12-31 00:00:00'},
                    'type': 'Feature',
                    'geometry': {
                        'coordinates': [[[-46.6353540826681, -23.5450950669741], [-46.63471434053, -23.5454695514008], [-46.6343109517528, -23.5458044203441]]],
                        'type': 'MultiLineString'
                    }
                }
            ]
        }

        self.tester.api_feature(expected, f_table_name="layer_1003", feature_id="1002")

        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'geometry': {
                        'type': 'MultiPolygon',
                        'coordinates': [[[[-46.6531368207044, -23.5426136385048], [-46.6526581134833, -23.5401195274321], [-46.6526581134833, -23.5401195274321], [-46.6535666865397, -23.5322186250535], [-46.6531368207044, -23.5426136385048]]]]
                    },
                    'properties': {'start_date': '1920-01', 'changeset_id': 1005, 'version': 1, 'end_date': '1940-12',
                                   'id': 1002, 'name': "Holy Mary's Hospital"}
                }
            ]
        }

        self.tester.api_feature(expected, f_table_name="layer_1005", feature_id="1002")

    def test_get_api_feature_return_zero_resources(self):
        expected = {'type': 'FeatureCollection', 'features': []}

        self.tester.api_feature(expected, f_table_name="layer_1001", feature_id="999")
        self.tester.api_feature(expected, f_table_name="layer_1003", feature_id="998")
        self.tester.api_feature(expected, f_table_name="layer_1005", feature_id="997")

        self.tester.api_feature_error_404_not_found(f_table_name="layer_999")
        self.tester.api_feature_error_404_not_found(f_table_name="layer_998")

    # feature - create, update and delete

    def test_api_feature_create_update_and_delete_point(self):
        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        ##################################################
        # create a changeset to create a feature
        ##################################################
        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': 1002},
            'type': 'Changeset'
        }
        changeset_id = self.tester.api_changeset_create(changeset)

        ##################################################
        # create a feature with user miguel
        ##################################################
        f_table_name = "layer_1002"

        feature = {
            'f_table_name': f_table_name,
            'properties': {'id': -1, 'start_date': '1870-01-01 00:00:00', 'end_date': '1870-12-31 00:00:00',
                           'version': 1, 'address': 'R. São José', 'changeset_id': changeset_id},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        feature = self.tester.api_feature_create(feature)

        feature_id = feature["properties"]["id"]

        ##################################################
        # update the feature with user
        ##################################################
        feature["properties"]["address"] = 'Rua São José Dormindo'
        self.tester.api_feature_update(feature)

        ##################################################
        # check if the resource was modified
        ##################################################
        feature["properties"]["version"] += 1  # increment 1 in the version (new version of the feature)
        expected_resource = {'type': 'FeatureCollection', 'features': [feature]}
        self.tester.api_feature(expected_at_least=expected_resource, f_table_name=f_table_name, feature_id=feature_id)

        ##################################################
        # remove the feature
        ##################################################
        self.tester.api_feature_delete(f_table_name=f_table_name, feature_id=feature_id, changeset_id=changeset_id)

        # it is not possible to find the resource that just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_feature(expected, f_table_name=f_table_name, feature_id=feature_id)

        # check if in the version table has 3 records (original, updated and removed)
        expected = {
            'features': [
                # the original version (inserted)
                {
                    'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
                    'properties': {
                        'address': 'R. São José', 'version': 1, 'id': feature_id, 'is_removed': False,
                        'changeset_id': changeset_id, 'end_date': '1870-12-31 00:00:00',
                        'start_date': '1870-01-01 00:00:00'
                    },
                    'type': 'Feature'
                },
                # the updated version
                {
                    'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
                    'properties': {
                        'address': 'Rua São José Dormindo', 'version': 2, 'id': feature_id, 'is_removed': False,
                        'changeset_id': changeset_id, 'end_date': '1870-12-31 00:00:00',
                        'start_date': '1870-01-01 00:00:00'
                    },
                    'type': 'Feature'
                },
                # the deleted version
                {
                    'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
                    'properties': {
                        'address': 'Rua São José Dormindo', 'version': 3, 'id': feature_id, 'is_removed': True,
                        'changeset_id': changeset_id, 'end_date': '1870-12-31 00:00:00',
                        'start_date': '1870-01-01 00:00:00'
                    },
                    'type': 'Feature'
                }
            ],
            'type': 'FeatureCollection'
        }
        self.tester.api_feature(expected=expected, f_table_name="version_" + f_table_name, feature_id=feature_id)

        ##################################################
        # CLOSE THE CHANGESET
        ##################################################
        close_changeset = {
            'properties': {'changeset_id': changeset_id, 'description': 'Inserting feature in layer_1003'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        ##################################################
        # login with admin to delete the changesets
        self.tester.auth_logout()
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # DELETE THE CHANGESET
        self.tester.api_changeset_delete(changeset_id=changeset_id)

        ##################################################

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_api_feature_create_update_and_delete_line(self):
        # DO LOGIN
        self.tester.auth_login("fernanda@admin.com", "fernanda")

        ##################################################
        # create a changeset to create a feature
        ##################################################
        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': 1003},
            'type': 'Changeset'
        }
        changeset_id = self.tester.api_changeset_create(changeset)

        ##################################################
        # create a feature with user miguel
        ##################################################
        f_table_name = "layer_1003"

        feature = {
            'f_table_name': f_table_name,
            'properties': {'start_date': '1920-01-01 00:00:00', 'version': 1, 'name': 'rua tres de dezembro',
                           'changeset_id': changeset_id, 'end_date': '1930-12-31 00:00:00'},
            'type': 'Feature',
            'geometry': {
                'coordinates': [[[-46.6353540826681, -23.5450950669741], [-46.6343109517528, -23.5458044203441]]],
                'type': 'MultiLineString'
            }
        }
        feature = self.tester.api_feature_create(feature)

        feature_id = feature["properties"]["id"]

        ##################################################
        # update the feature with user
        ##################################################
        feature["properties"]["name"] = 'Rua treze de dezembro'
        self.tester.api_feature_update(feature)

        ##################################################
        # check if the resource was modified
        ##################################################
        feature["properties"]["version"] += 1  # increment 1 in the version (new version of the feature)
        expected_resource = {'type': 'FeatureCollection', 'features': [feature]}
        self.tester.api_feature(expected_at_least=expected_resource, f_table_name=f_table_name, feature_id=feature_id)

        ##################################################
        # remove the feature
        ##################################################
        self.tester.api_feature_delete(f_table_name=f_table_name, feature_id=feature_id, changeset_id=changeset_id)

        # it is not possible to find the resource that just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_feature(expected, f_table_name=f_table_name, feature_id=feature_id)

        # check if in the version table has 3 records (original, updated and removed)
        expected = {
            'features': [
                {
                    'geometry': {'coordinates': [[[-46.6353540826681, -23.5450950669741],
                                                  [-46.6343109517528, -23.5458044203441]]], 'type': 'MultiLineString'},
                    'type': 'Feature',
                    'properties': {
                        'is_removed': False, 'changeset_id': changeset_id, 'id': feature_id, 'version': 1,
                        'end_date': '1930-12-31 00:00:00', 'start_date': '1920-01-01 00:00:00',
                        'name': 'rua tres de dezembro'
                    }
                },
                {
                    'geometry': {'coordinates': [[[-46.6353540826681, -23.5450950669741],
                                                  [-46.6343109517528, -23.5458044203441]]], 'type': 'MultiLineString'},
                    'type': 'Feature',
                    'properties': {
                        'is_removed': False, 'changeset_id': changeset_id, 'id': feature_id, 'version': 2,
                        'end_date': '1930-12-31 00:00:00', 'start_date': '1920-01-01 00:00:00',
                        'name': 'Rua treze de dezembro'
                    }
                },
                {
                    'geometry': {'coordinates': [[[-46.6353540826681, -23.5450950669741],
                                                  [-46.6343109517528, -23.5458044203441]]], 'type': 'MultiLineString'},
                    'type': 'Feature',
                    'properties': {
                        'is_removed': True, 'changeset_id': changeset_id, 'id': feature_id, 'version': 3,
                        'end_date': '1930-12-31 00:00:00', 'start_date': '1920-01-01 00:00:00',
                        'name': 'Rua treze de dezembro'
                    }
                }
            ],
            'type': 'FeatureCollection'
        }
        self.tester.api_feature(expected=expected, f_table_name="version_" + f_table_name, feature_id=feature_id)

        ##################################################
        # CLOSE THE CHANGESET
        ##################################################
        close_changeset = {
            'properties': {'changeset_id': changeset_id, 'description': 'Inserting feature in layer_1003'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        ##################################################
        # login with admin to delete the changesets
        self.tester.auth_logout()
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # DELETE THE CHANGESET
        self.tester.api_changeset_delete(changeset_id=changeset_id)

        ####################################################################################################

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_api_feature_create_update_and_delete_polygon__create_with_optional_values(self):
        # DO LOGIN
        self.tester.auth_login("ana@admin.com", "ana")

        ##################################################
        # create a changeset to create a feature
        ##################################################
        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': 1006},
            'type': 'Changeset'
        }
        changeset_id = self.tester.api_changeset_create(changeset)

        ##################################################
        # create a feature with user miguel
        ##################################################
        f_table_name = "layer_1006"

        feature = {
            'f_table_name': f_table_name,
            'properties': {'id': -1, 'start_date': 1870, 'end_date': None, 'version': 1,
                           'name': '', 'changeset_id': changeset_id},
            'geometry': {
                "type": "MultiPolygon",
                "coordinates": [[[[-46.6323, -23.5316], [-46.6375, -23.5290], [-46.6323, -23.5316]]]],
            },
            'type': 'Feature'
        }
        feature = self.tester.api_feature_create(feature)

        feature_id = feature["properties"]["id"]

        ##################################################
        # update the feature with user
        ##################################################
        feature["properties"]["name"] = 'Hospital Rosa dos Santos'
        self.tester.api_feature_update(feature)

        ##################################################
        # check if the resource was modified
        ##################################################
        feature["properties"]["version"] += 1  # increment 1 in the version (new version of the feature)
        expected_resource = {'type': 'FeatureCollection', 'features': [feature]}
        self.tester.api_feature(expected_at_least=expected_resource, f_table_name=f_table_name, feature_id=feature_id)

        ##################################################
        # remove the feature
        ##################################################
        self.tester.api_feature_delete(f_table_name=f_table_name, feature_id=feature_id, changeset_id=changeset_id)

        # it is not possible to find the resource that just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_feature(expected, f_table_name=f_table_name, feature_id=feature_id)

        # check if in the version table has 3 records (original, updated and removed)
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {
                        'id': feature_id, 'is_removed': False, 'version': 1, 'changeset_id': changeset_id,
                        'start_date': 1870, 'name': '', 'end_date': None
                    },
                    'geometry': {'coordinates': [[[[-46.6323, -23.5316], [-46.6375, -23.529], [-46.6323, -23.5316]]]],
                                 'type': 'MultiPolygon'},
                    'type': 'Feature'
                },
                {
                    'properties': {
                        'id': feature_id, 'is_removed': False, 'version': 2, 'changeset_id': changeset_id,
                        'start_date': 1870, 'name': 'Hospital Rosa dos Santos', 'end_date': None
                    },
                    'geometry': {'coordinates': [[[[-46.6323, -23.5316], [-46.6375, -23.529], [-46.6323, -23.5316]]]],
                                 'type': 'MultiPolygon'},
                    'type': 'Feature'
                },
                {
                    'properties': {
                        'id': feature_id, 'is_removed': True, 'version': 3, 'changeset_id': changeset_id,
                        'start_date': 1870, 'name': 'Hospital Rosa dos Santos', 'end_date': None
                    },
                    'geometry': {'coordinates': [[[[-46.6323, -23.5316], [-46.6375, -23.529], [-46.6323, -23.5316]]]],
                                 'type': 'MultiPolygon'},
                    'type': 'Feature'
                }
            ]
        }
        self.tester.api_feature(expected=expected, f_table_name="version_" + f_table_name, feature_id=feature_id)

        ##################################################
        # CLOSE THE CHANGESET
        ##################################################
        close_changeset = {
            'properties': {'changeset_id': changeset_id, 'description': 'Inserting feature in layer_1006'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        ####################################################################################################
        # login with admin to delete the changesets
        self.tester.auth_logout()
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # DELETE THE CHANGESET
        self.tester.api_changeset_delete(changeset_id=changeset_id)

        ####################################################################################################

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_api_feature_create_update_and_delete_point_one_changeset_for_each_action(self):
        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        ##################################################
        # create a changeset to each action related to the feature
        ##################################################
        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': 1002},
            'type': 'Changeset'
        }
        changeset_id_insert = self.tester.api_changeset_create(changeset)

        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': 1002},
            'type': 'Changeset'
        }
        changeset_id_update = self.tester.api_changeset_create(changeset)

        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': 1002},
            'type': 'Changeset'
        }
        changeset_id_delete = self.tester.api_changeset_create(changeset)

        ##################################################
        # create a feature with user miguel
        ##################################################
        f_table_name = "layer_1002"

        feature = {
            'f_table_name': f_table_name,
            'properties': {'id': -1, 'start_date': '1870-01-01 00:00:00', 'end_date': '1870-12-31 00:00:00',
                           'version': 1, 'address': 'R. São José', 'changeset_id': changeset_id_insert},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        feature = self.tester.api_feature_create(feature)

        feature_id = feature["properties"]["id"]

        ####################################################################################################
        # update the feature with user
        ##################################################
        feature["properties"]["address"] = 'Rua São José Dormindo'
        feature["properties"]["changeset_id"] = changeset_id_update
        self.tester.api_feature_update(feature)

        ##################################################
        # check if the resource was modified
        ##################################################
        feature["properties"]["version"] += 1  # increment 1 in the version (new version of the feature)
        expected_resource = {'type': 'FeatureCollection', 'features': [feature]}
        self.tester.api_feature(expected_at_least=expected_resource, f_table_name=f_table_name, feature_id=feature_id)

        ##################################################
        # remove the feature
        ##################################################
        self.tester.api_feature_delete(f_table_name=f_table_name, feature_id=feature_id, changeset_id=changeset_id_delete)

        # it is not possible to find the resource that just deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.tester.api_feature(expected, f_table_name=f_table_name, feature_id=feature_id)

        # self.maxDiff = None

        # check if in the version table has 3 records (original, updated and removed)
        expected = {
            'features': [
                # the original version (inserted)
                {
                    'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
                    'properties': {
                        'address': 'R. São José', 'version': 1, 'id': feature_id, 'is_removed': False,
                        'changeset_id': changeset_id_insert, 'end_date': '1870-12-31 00:00:00',
                        'start_date': '1870-01-01 00:00:00'
                    },
                    'type': 'Feature'
                },
                # the updated version
                {
                    'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
                    'properties': {
                        'address': 'Rua São José Dormindo', 'version': 2, 'id': feature_id, 'is_removed': False,
                        'changeset_id': changeset_id_update, 'end_date': '1870-12-31 00:00:00',
                        'start_date': '1870-01-01 00:00:00'
                    },
                    'type': 'Feature'
                },
                # the deleted version
                {
                    'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
                    'properties': {
                        'address': 'Rua São José Dormindo', 'version': 3, 'id': feature_id, 'is_removed': True,
                        'changeset_id': changeset_id_delete, 'end_date': '1870-12-31 00:00:00',
                        'start_date': '1870-01-01 00:00:00'
                    },
                    'type': 'Feature'
                }
            ],
            'type': 'FeatureCollection'
        }
        self.tester.api_feature(expected=expected, f_table_name="version_" + f_table_name, feature_id=feature_id)

        ##################################################
        # CLOSE THE CHANGESETS
        ##################################################
        close_changeset = {
            'properties': {'changeset_id': changeset_id_insert, 'description': 'Inserting feature in layer_1002'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        close_changeset = {
            'properties': {'changeset_id': changeset_id_update, 'description': 'Updating feature in layer_1002'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        close_changeset = {
            'properties': {'changeset_id': changeset_id_delete, 'description': 'Deleting feature in layer_1002'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        ####################################################################################################
        # login with admin to delete the changesets
        self.tester.auth_logout()
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # DELETE THE CHANGESETS
        self.tester.api_changeset_delete(changeset_id=changeset_id_insert)

        self.tester.api_changeset_delete(changeset_id=changeset_id_update)

        self.tester.api_changeset_delete(changeset_id=changeset_id_delete)

        ####################################################################################################

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


class TestAPIFeatureError(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # feature errors - get

    def test_get_api_feature_error_400_bad_request(self):
        self.tester.api_feature_error_400_bad_request(f_table_name="layer_1001", feature_id="abc")
        self.tester.api_feature_error_400_bad_request(f_table_name="layer_1001", feature_id=0)
        self.tester.api_feature_error_400_bad_request(f_table_name="layer_1001", feature_id=-1)
        self.tester.api_feature_error_400_bad_request(f_table_name="layer_1001", feature_id="-1")
        self.tester.api_feature_error_400_bad_request(f_table_name="layer_1001", feature_id="0")

        self.tester.api_feature_error_400_bad_request(feature_id="abc")
        self.tester.api_feature_error_400_bad_request(feature_id=0)
        self.tester.api_feature_error_400_bad_request(feature_id=-1)
        self.tester.api_feature_error_400_bad_request(feature_id="-1")
        self.tester.api_feature_error_400_bad_request(feature_id="0")

    # feature errors - create

    def test_post_api_feature_create_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        # try to create a layer (without f_table_name)
        resource = {
            'properties': {'id': -1, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': 1014},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_create_error_400_bad_request(resource)

        # try to create a layer (without properties)
        resource = {
            'f_table_name': 'layer_1002',
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_create_error_400_bad_request(resource)

        # try to create a layer (without geometry)
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': -1, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': 1014},
            'type': 'Feature'
        }
        self.tester.api_feature_create_error_400_bad_request(resource)

        # try to create a layer (without start_date)
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': -1, 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': 1014},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_create_error_400_bad_request(resource)

        # try to create a layer (without address)
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': -1, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'changeset_id': 1014},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_create_error_400_bad_request(resource)

        # try to create a layer (without changeset_id)
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': -1, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José'},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_feature_create_error_400_bad_request_invalid_geometry(self):
        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        # try to create a layer with an invalid geometry
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': -1, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': 1014},
            'geometry': {'coordinates': [-46.6375790530164, -23.5290461960682], 'type': 'Point'},
            'type': 'Feature'
        }
        self.tester.api_feature_create_error_400_bad_request(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_feature_create_error_401_unauthorized_user_is_not_logged(self):
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': -1, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': 1001},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_create_error_401_unauthorized(resource)

    def test_post_api_feature_create_error_403_forbidden_invalid_user_tries_to_manage(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        # try to create a layer (without f_table_name)
        resource = {
            'f_table_name': 'layer_1001',
            'properties': {'id': -1, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': 1001},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_create_error_403_forbidden(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_feature_create_error_403_forbidden_user_did_not_create_the_changeset(self):
        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        # try to create a layer (without f_table_name)
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': -1, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': 1001},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_create_error_403_forbidden(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_feature_create_error_404_not_found_changeset_id(self):
        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        # try to create a layer (without f_table_name)
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': -1, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': 999},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_create_error_404_not_found(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_feature_create_error_409_conflict_changeset_was_already_closed(self):
        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': -1, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': 1002},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_create_error_409_conflict(resource)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_post_api_feature_create_error_404_not_found_f_table_name(self):
        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        ##################################################
        # create a changeset to create a feature
        ##################################################
        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': 1002},
            'type': 'Changeset'
        }
        changeset_id = self.tester.api_changeset_create(changeset)

        # try to create a layer with invalid f_table_name
        resource = {
            'f_table_name': 'layer_100X',
            'properties': {'id': -1, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': changeset_id},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_create_error_404_not_found(resource, string_to_compare_error="Not found layer")

        ##################################################
        # CLOSE THE CHANGESET
        close_changeset = {
            'properties': {'changeset_id': changeset_id, 'description': 'Updating feature in layer_1002'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        ####################################################################################################
        # login with admin to delete the changesets
        self.tester.auth_logout()
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # DELETE THE CHANGESET
        self.tester.api_changeset_delete(changeset_id=changeset_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    # feature errors - update

    def test_put_api_feature_error_400_bad_request_attribute_in_JSON_is_missing(self):
        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        # try to create a layer (without f_table_name)
        resource = {
            'properties': {'id': -1, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': 1014},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_update_error_400_bad_request(resource, string_to_compare_error="Some attribute in the JSON")

        # try to create a layer (without properties)
        resource = {
            'f_table_name': 'layer_1002',
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_update_error_400_bad_request(resource, string_to_compare_error="Some attribute in the JSON")

        # try to create a layer (without geometry)
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': 1006, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': 1014},
            'type': 'Feature'
        }
        self.tester.api_feature_update_error_400_bad_request(resource, string_to_compare_error="Some attribute in the JSON")

        # try to create a layer (without start_date)
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': 1006, 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': 1014},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_update_error_400_bad_request(resource, string_to_compare_error="Some attribute in the JSON")

        # try to create a layer (without address)
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': 1006, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'changeset_id': 1014},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_update_error_400_bad_request(resource, string_to_compare_error="Some attribute in the JSON")

        # try to create a layer (without changeset_id)
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': 1006, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José'},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_update_error_400_bad_request(resource, string_to_compare_error="Some attribute in the JSON")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_feature_error_400_bad_request_invalid_geometry(self):
        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        ##################################################
        # create a changeset to create a feature
        ##################################################
        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': 1002},
            'type': 'Changeset'
        }
        changeset_id = self.tester.api_changeset_create(changeset)

        ##################################################
        # try to update a layer with an invalid geometry
        ##################################################
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': 1006, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': changeset_id},
            'geometry': {'coordinates': [-46.6375790530164, -23.5290461960682], 'type': 'Point'},
            'type': 'Feature'
        }
        self.tester.api_feature_update_error_400_bad_request(resource, string_to_compare_error="One specified attribute")

        ##################################################
        # CLOSE THE CHANGESET
        close_changeset = {
            'properties': {'changeset_id': changeset_id, 'description': 'Updating feature in layer_1002'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        ##################################################
        # login with admin to delete the changesets
        self.tester.auth_logout()
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # DELETE THE CHANGESET
        self.tester.api_changeset_delete(changeset_id=changeset_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_feature_error_400_bad_request_invalid_feature_id(self):
        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        ##################################################
        # create a changeset to create a feature
        ##################################################
        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': 1002},
            'type': 'Changeset'
        }
        changeset_id = self.tester.api_changeset_create(changeset)

        ##################################################
        # try to update a layer with an invalid geometry
        ##################################################
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': -1, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': changeset_id},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_update_error_400_bad_request(resource, string_to_compare_error="Invalid feature id")

        ##################################################
        # CLOSE THE CHANGESET
        close_changeset = {
            'properties': {'changeset_id': changeset_id, 'description': 'Updating feature in layer_1002'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        ##################################################
        # login with admin to delete the changesets
        self.tester.auth_logout()
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # DELETE THE CHANGESET
        self.tester.api_changeset_delete(changeset_id=changeset_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_feature_error_401_unauthorized_user_is_not_logged(self):
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': 1006, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': 1014},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_update_error_401_unauthorized(resource)

    def test_put_api_feature_error_403_forbidden_invalid_user_tries_to_manage(self):
        # DO LOGIN
        self.tester.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # create a changeset to create a feature
        ##################################################
        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': 1002},
            'type': 'Changeset'
        }
        changeset_id = self.tester.api_changeset_create(changeset)

        ####################################################################################################
        # miguel tries to update one feature that doesn't belong to him
        ##################################################
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': 1006, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': changeset_id},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_update_error_403_forbidden(resource, string_to_compare_error="Just the collaborator")

        ##################################################
        # CLOSE THE CHANGESET
        close_changeset = {
            'properties': {'changeset_id': changeset_id, 'description': 'Updating feature in layer_1002'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        ####################################################################################################
        # login with admin to delete the changesets
        self.tester.auth_logout()
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # DELETE THE CHANGESET
        self.tester.api_changeset_delete(changeset_id=changeset_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_feature_error_403_forbidden_user_did_not_create_the_changeset(self):
        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        # try to create a layer
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': 1006, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': 1001},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_update_error_403_forbidden(resource, string_to_compare_error="was not created by current")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_feature_error_404_not_found_feature_id(self):
        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        ##################################################
        # create a changeset to create a feature
        ##################################################
        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': 1002},
            'type': 'Changeset'
        }
        changeset_id = self.tester.api_changeset_create(changeset)

        ####################################################################################################
        # rafael tries to update one feature that doesn't exist
        ##################################################
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': 999, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': changeset_id},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_update_error_404_not_found(resource, string_to_compare_error="Not found feature")

        ##################################################
        # CLOSE THE CHANGESET
        close_changeset = {
            'properties': {'changeset_id': changeset_id, 'description': 'Updating feature in layer_1002'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        ####################################################################################################
        # login with admin to delete the changesets
        self.tester.auth_logout()
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # DELETE THE CHANGESET
        self.tester.api_changeset_delete(changeset_id=changeset_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_feature_error_404_not_found_changeset_id(self):
        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        ####################################################################################################
        # rafael tries to update one feature that doesn't exist
        ##################################################
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': 1006, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': 999},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_update_error_404_not_found(resource, string_to_compare_error="Not found the changeset")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_feature_error_404_not_found_f_table_name(self):
        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        ##################################################
        # create a changeset to create a feature
        ##################################################
        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': 1002},
            'type': 'Changeset'
        }
        changeset_id = self.tester.api_changeset_create(changeset)

        ##################################################
        # rafael tries to update one feature with invalid f_table_name
        ##################################################
        resource = {
            'f_table_name': 'layer_100X',
            'properties': {'id': 1006, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': changeset_id},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_update_error_404_not_found(resource, string_to_compare_error="Not found layer")

        ##################################################
        # CLOSE THE CHANGESET
        close_changeset = {
            'properties': {'changeset_id': changeset_id, 'description': 'Updating feature in layer_1002'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        ####################################################################################################
        # login with admin to delete the changesets
        self.tester.auth_logout()
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # DELETE THE CHANGESET
        self.tester.api_changeset_delete(changeset_id=changeset_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_feature_error_409_conflict_changeset_was_already_closed(self):
        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        ##################################################
        # rafael tries to update one feature with invalid changeset
        ##################################################
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': 1006, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 1,
                           'address': 'R. São José', 'changeset_id': 1002},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_update_error_409_conflict(resource, string_to_compare_error="was already closed at")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_put_api_feature_error_409_conflict_invalid_version(self):
        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        ##################################################
        # create a changeset to create a feature
        ##################################################
        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': 1002},
            'type': 'Changeset'
        }
        changeset_id = self.tester.api_changeset_create(changeset)

        ##################################################
        # rafael tries to update one feature with invalid version
        ##################################################
        resource = {
            'f_table_name': 'layer_1002',
            'properties': {'id': 1006, 'start_date': '1870-01-01', 'end_date': '1870-12-31', 'version': 5,
                           'address': 'R. São José', 'changeset_id': changeset_id},
            'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
            'type': 'Feature'
        }
        self.tester.api_feature_update_error_409_conflict(resource, string_to_compare_error="Invalid version attribute")

        ##################################################
        # CLOSE THE CHANGESET
        close_changeset = {
            'properties': {'changeset_id': changeset_id, 'description': 'Updating feature in layer_1002'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        ####################################################################################################
        # login with admin to delete the changesets
        self.tester.auth_logout()
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # DELETE THE CHANGESET
        self.tester.api_changeset_delete(changeset_id=changeset_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    # feature errors - delete

    def test_delete_api_feature_error_400_bad_request(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        self.tester.api_feature_delete_error_400_bad_request(f_table_name="layer_1002", feature_id="abc", changeset_id=1014)
        self.tester.api_feature_delete_error_400_bad_request(f_table_name="layer_1002", feature_id=0, changeset_id=1014)
        self.tester.api_feature_delete_error_400_bad_request(f_table_name="layer_1002", feature_id=-1, changeset_id=1014)
        self.tester.api_feature_delete_error_400_bad_request(f_table_name="layer_1002", feature_id="-1", changeset_id=1014)
        self.tester.api_feature_delete_error_400_bad_request(f_table_name="layer_1002", feature_id="0", changeset_id=1014)

        self.tester.api_feature_delete_error_400_bad_request(f_table_name="layer_1002", feature_id=1001, changeset_id="abc")
        self.tester.api_feature_delete_error_400_bad_request(f_table_name="layer_1002", feature_id=1001, changeset_id=0)
        self.tester.api_feature_delete_error_400_bad_request(f_table_name="layer_1002", feature_id=1001, changeset_id=-1)
        self.tester.api_feature_delete_error_400_bad_request(f_table_name="layer_1002", feature_id=1001, changeset_id="-1")
        self.tester.api_feature_delete_error_400_bad_request(f_table_name="layer_1002", feature_id=1001, changeset_id="0")

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_feature_error_401_unauthorized_user_is_not_logged(self):
        self.tester.api_feature_delete_error_401_unauthorized(f_table_name="layer_1001", feature_id="abc", changeset_id=1001)
        self.tester.api_feature_delete_error_401_unauthorized(f_table_name="layer_1001", feature_id=0, changeset_id=1001)
        self.tester.api_feature_delete_error_401_unauthorized(f_table_name="layer_1001", feature_id=-1, changeset_id=1001)
        self.tester.api_feature_delete_error_401_unauthorized(f_table_name="layer_1001", feature_id="-1", changeset_id=1001)
        self.tester.api_feature_delete_error_401_unauthorized(f_table_name="layer_1001", feature_id="0", changeset_id=1001)
        self.tester.api_feature_delete_error_401_unauthorized(f_table_name="layer_1001", feature_id="1001", changeset_id=1001)

    def test_delete_api_feature_error_403_forbidden_invalid_user_tries_to_manage(self):
        self.tester.auth_login("rafael@admin.com", "rafael")

        ########################################
        # try to delete the feature with user miguel
        ########################################
        # TRY TO REMOVE THE LAYER
        self.tester.api_feature_delete_error_403_forbidden(f_table_name="layer_1001", feature_id="1001", changeset_id=1014)

        # logout with user rodrigo
        self.tester.auth_logout()

    def test_delete_api_feature_error_403_forbidden_user_did_not_create_the_changeset(self):
        self.tester.auth_login("miguel@admin.com", "miguel")

        ########################################
        # try to delete the feature with user miguel
        ########################################
        # TRY TO REMOVE THE LAYER
        self.tester.api_feature_delete_error_403_forbidden(f_table_name="layer_1001", feature_id="1001", changeset_id=1002)

        # logout with user rodrigo
        self.tester.auth_logout()

    def test_delete_api_feature_error_404_not_found_feature_id_or_changeset_id(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        self.tester.api_feature_delete_error_404_not_found(f_table_name="layer_1002", feature_id="999", changeset_id=1014)
        self.tester.api_feature_delete_error_404_not_found(f_table_name="layer_1002", feature_id="998", changeset_id=1014)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_feature_error_404_not_found_f_table_name(self):
        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        ##################################################
        # create a changeset to create a feature
        ##################################################
        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': 1002},
            'type': 'Changeset'
        }
        changeset_id = self.tester.api_changeset_create(changeset)

        # try to delete a feature with an invalid f_table_name
        self.tester.api_feature_delete_error_404_not_found(f_table_name="layer_100X", feature_id="1006",
                                                           changeset_id=changeset_id)

        ##################################################
        # CLOSE THE CHANGESET
        close_changeset = {
            'properties': {'changeset_id': changeset_id, 'description': 'Updating feature in layer_1002'},
            'type': 'ChangesetClose'
        }
        self.tester.api_changeset_close(close_changeset)

        ####################################################################################################
        # login with admin to delete the changesets
        self.tester.auth_logout()
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # DELETE THE CHANGESET
        self.tester.api_changeset_delete(changeset_id=changeset_id)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()

    def test_delete_api_feature_error_409_conflict_changeset_was_already_closed(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        # DO LOGIN
        self.tester.auth_login("rafael@admin.com", "rafael")

        self.tester.api_feature_delete_error_409_conflict(f_table_name="layer_1002", feature_id="1001", changeset_id=1002)
        self.tester.api_feature_delete_error_409_conflict(f_table_name="layer_1002", feature_id="1001", changeset_id=1002)

        # DO LOGOUT AFTER THE TESTS
        self.tester.auth_logout()


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
