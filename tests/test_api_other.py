#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import remove as remove_file

from unittest import TestCase

from util.tester import UtilTester
from util.common import FILES_PATH



class TestAPICurrentUser(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_api_user_by_token_with_login(self):
        # DO LOGIN BEFORE THE TEST
        self.tester.auth_login("rodrigo@admin.com", "rodrigo")

        # do not put the "login_date" and "created_at" attributes, because they are created dynamically
        expected_at_least = {
            'properties': {
                'username': 'rodrigo', 'is_the_admin': True, 'user_id': 1002,
                'email': 'rodrigo@admin.com', 'terms_agreed': True, 'name': 'Rodrigo',
                'is_email_valid': True, 'receive_notification_by_email': True
            },
            'type': 'User'
        }

        self.tester.api_user_by_token(expected_at_least)

        # DO LOGOUT AFTER THE TEST
        self.tester.auth_logout()


# VALIDATE EMAIL

class TestAPIValidateEmail(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_api_validate_email(self):
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxMDA1fQ.XbibygDhgaF0x3w50wI8UWfK8u1I2vrMlfPBa5y-Z4o'
        user_id = 1005

        # a user is with a invalidated email
        user = self.tester.api_user(user_id=user_id)
        self.assertEqual(user["features"][0]["properties"]["is_email_valid"], False)

        # so the user validate his/her email
        self.tester.api_validate_email(token)

        # now the user is with the validated email
        user = self.tester.api_user(user_id=user_id)
        self.assertEqual(user["features"][0]["properties"]["is_email_valid"], True)

        # change the is_email_valid to False again, for it doesn't break the tests
        self.tester.api_is_email_valid(user_id=user_id, is_email_valid=False)

        user = self.tester.api_user(user_id=user_id)
        self.assertEqual(user["features"][0]["properties"]["is_email_valid"], False)


class TestAPIValidateEmailErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_api_validate_email_400_bad_request(self):
        # try to validate the email
        self.tester.api_validate_email_400_bad_request('eyJhbGciOiJIVCJ9.eyJ1c2VyMDAzfQ.IsLw6ZQh-UoPWEKc8Cj5q8')

        # try to validate the email
        self.tester.api_validate_email_400_bad_request('eyJhbGciOiJIVCJ91c2VyMDAzfQ.IsLw6ZQh-UoPWEKc8Cj5q8')

        # try to validate the email
        self.tester.api_validate_email_400_bad_request('eyJhbGciOiJIc2VyMDAzw6ZQh-UoPWEKc8Cj5q8')

    def test_api_validate_email_404_not_found(self):
        # try to validate the email with user 999
        self.tester.api_validate_email_404_not_found('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo5OTl9.fJh2x9cThRhYytoz7vrzkgCe8nHjk2_4NhgtV-PJpgU')

        # try to validate the email with user 999
        self.tester.api_validate_email_404_not_found('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo5OTB9.VR66H2KA0V2gpZQdu6UbfM4koRmSUx7yCVvfQe6IOCk')


# MASK

class TestAPIMask(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # mask - get

    def test_get_api_mask_return_all_masks(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'mask_id': 1001, 'mask': 'YYYY-MM-DD'},
                    'type': 'Mask'
                },
                {
                    'properties': {'mask_id': 1002, 'mask': 'YYYY-MM'},
                    'type': 'Mask'
                },
                {
                    'properties': {'mask_id': 1003, 'mask': 'YYYY'},
                    'type': 'Mask'
                }
            ]
        }

        self.tester.api_mask(expected)

    def test_get_api_mask_return_mask_by_mask_id(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'properties': {'mask_id': 1001, 'mask': 'YYYY-MM-DD'},
                    'type': 'Mask'
                },
            ]
        }

        self.tester.api_mask(expected, mask_id="1001")

    def test_get_api_mask_return_zero_resources(self):
        expected = {'type': 'FeatureCollection', 'features': []}

        self.tester.api_mask(expected, mask_id="999")
        self.tester.api_mask(expected, mask_id="998")


class TestAPIMaskErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    # mask errors - get

    def test_get_api_mask_error_400_bad_request(self):
        self.tester.api_mask_error_400_bad_request(mask_id="abc")
        self.tester.api_mask_error_400_bad_request(mask_id=0)
        self.tester.api_mask_error_400_bad_request(mask_id=-1)
        self.tester.api_mask_error_400_bad_request(mask_id="-1")
        self.tester.api_mask_error_400_bad_request(mask_id="0")


# CONVERT GEOJSON TO SHAPEFILE

class TestAPIConvertGeoJSONToShapefile(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        self.folder_name = "{}/geojson/".format(FILES_PATH)

    # import - create

    def test_post_convert_geojson_to_shapefile_mini_geojson(self):
        ##################################################
        # convert a geojson to a shapefile
        ##################################################
        file_name = "test_geojson_01.geojson"

        file_name_with_folder = self.folder_name + file_name

        with open(file_name_with_folder, mode='rb') as file:  # rb = read binary
            binary_file_geojson = file.read()

            binary_file_zip = self.tester.api_post_convert_geojson_to_shapefile(binary_file_geojson, file_name=file_name)

            zip_file_name_with_folder = file_name_with_folder.replace(".geojson", ".zip")

            output_file = open(zip_file_name_with_folder, 'wb')  # wb - write binary
            output_file.write(binary_file_zip)
            output_file.close()

            remove_file(zip_file_name_with_folder)

    def test_post_convert_geojson_to_shapefile_gabriels_geojson(self):
        ##################################################
        # convert a geojson to a shapefile
        ##################################################
        file_name = "test_gabriels_geojson.geojson"

        file_name_with_folder = self.folder_name + file_name

        with open(file_name_with_folder, mode='rb') as file:  # rb = read binary
            binary_file_geojson = file.read()

            binary_file_zip = self.tester.api_post_convert_geojson_to_shapefile(binary_file_geojson, file_name=file_name)

            zip_file_name_with_folder = file_name_with_folder.replace(".geojson", ".zip")

            output_file = open(zip_file_name_with_folder, 'wb')  # wb - write binary
            output_file.write(binary_file_zip)
            output_file.close()

            remove_file(zip_file_name_with_folder)


class TestAPIConvertGeoJSONToShapefileErrors(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

        self.folder_name = "{}/geojson/".format(FILES_PATH)

    # import - create

    def test_post_import_shp_error_400_bad_request_it_is_necessary_to_pass_the_file_name_in_request(self):
        ##################################################
        # convert a geojson to a shapefile
        ##################################################
        file_name = "test_geojson_01.geojson"

        file_name_with_folder = self.folder_name + file_name

        with open(file_name_with_folder, mode='rb') as file:  # rb = read binary
            binary_file_geojson = file.read()

            self.tester.api_post_convert_geojson_to_shapefile_400_bad_request(binary_file_geojson)

    def test_post_import_shp_error_400_bad_request_it_is_invalid_file_name(self):
        ##################################################
        # convert a geojson to a shapefile
        ##################################################
        file_name = "test_geojson_01.geojson"

        file_name_with_folder = self.folder_name + file_name

        with open(file_name_with_folder, mode='rb') as file:  # rb = read binary
            binary_file_geojson = file.read()

            self.tester.api_post_convert_geojson_to_shapefile_400_bad_request(binary_file_geojson, file_name="aa/ass")

            self.tester.api_post_convert_geojson_to_shapefile_400_bad_request(binary_file_geojson, file_name="aa\\ass")

    def test_post_import_shp_error_400_bad_request_empty_file(self):
        ##################################################
        # convert a geojson to a shapefile
        ##################################################
        file_name = "test_geojson_01.geojson"

        self.tester.api_post_convert_geojson_to_shapefile_400_bad_request('', file_name=file_name)
        self.tester.api_post_convert_geojson_to_shapefile_400_bad_request(b'', file_name=file_name)

    def test_post_import_shp_error_400_bad_request_it_is_invalid_file_name_it_is_not_geojson(self):
        ##################################################
        # convert a geojson to a shapefile
        ##################################################
        file_name = "test_geojson_01.geojson"

        file_name_with_folder = self.folder_name + file_name

        with open(file_name_with_folder, mode='rb') as file:  # rb = read binary
            binary_file_geojson = file.read()

            self.tester.api_post_convert_geojson_to_shapefile_400_bad_request(binary_file_geojson,
                                                                              file_name="test_geojson_01")

    def test_post_import_shp_error_500_internal_server_error_invalid_geojson_binary_file(self):
        ##################################################
        # convert a geojson to a shapefile
        ##################################################
        file_name = "test_invalid_geojson.geojson"

        file_name_with_folder = self.folder_name + file_name

        with open(file_name_with_folder, mode='rb') as file:  # rb = read binary
            binary_file_geojson = file.read()

            self.tester.api_post_convert_geojson_to_shapefile_500_internal_server_error(binary_file_geojson,
                                                                                        file_name=file_name)


"""
class TestAPICapabilities(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_api_capabilities(self):
        expected = {
            "version": "0.0.4",
            "status": {"postgresql": "online"}
        }

        self.tester.api_capabilities(expected)


class TestAPICurrentUserError(TestCase):

    def setUp(self):
        # create a tester passing the unittest self
        self.tester = UtilTester(self)

    def test_api_user_by_token_invalid_token(self):
        # do not put the "login_date" and "created_at" attributes, because they are created dynamically
        invalid_authorization = "29uj29uç0suk2"

        self.tester.api_user_by_token_400_bad_request(invalid_authorization)

    def test_api_user_by_token_without_login(self):
        self.tester.api_user_by_token_401_unauthorized()
"""

# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
