#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create controllers.
"""

from os import makedirs
from os.path import exists
from subprocess import check_call, CalledProcessError
from zipfile import ZipFile
from tornado.web import HTTPError

from ..base import BaseHandlerLayer, BaseHandlerUserLayer, auth_non_browser_based  #, BaseHandlerChangeset
from settings.settings import __TEMP_FOLDER__


def exist_shapefile_inside_zip(zip_reference):
    list_file_names_of_zip = zip_reference.namelist()

    for file_name_in_zip in list_file_names_of_zip:
        # if exist a SHP file inside the zip, return true
        if file_name_in_zip.endswith(".shp"):
            return True

    return False


# LAYER

class APILayer(BaseHandlerLayer):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/layer/?(?P<param>[A-Za-z0-9-]+)?/",
            r"/api/layer/?(?P<param>[A-Za-z0-9-]+)?"]

    def get(self, param=None):
        # self.get_method_api_layer()
        self.get_method_api_feature()

    @auth_non_browser_based
    def put(self, param=None):
        # self.put_method_api_layer(param)
        self.put_method_api_feature(param)

    @auth_non_browser_based
    def delete(self, param=None):
        self.delete_method_api_feature(param)


class APIUserLayer(BaseHandlerUserLayer):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/user_layer/?(?P<param>[A-Za-z0-9-]+)?/",
            r"/api/user_layer/?(?P<param>[A-Za-z0-9-]+)?"]

    def get(self, param=None):
        self.get_method_api_feature()

    @auth_non_browser_based
    def put(self, param=None):
        self.put_method_api_feature(param)

    @auth_non_browser_based
    def delete(self, param=None):
        self.delete_method_api_feature(param)


class APIImport(BaseHandlerLayer):

    # A list of URLs that can be use for the HTTP methods
    urls = [r"/api/import/?(?P<param>[A-Za-z0-9-]+)?/",
            # r"/api/import/?(?P<param>[A-Za-z0-9-]+)?"
            ]

    # def get(self, param=None):
    #     # self.get_method_api_layer()
    #     self.get_method_api_feature()

    @auth_non_browser_based
    def post(self, param=None):
        if param == "shp":
            self.import_shp()
        else:
            raise HTTPError(404, "Not found a route with the parameter: " + str(param))

    # @auth_non_browser_based
    # def delete(self, param=None):
    #     self.delete_method_api_feature(param)

    # def options(self, param=None):
    #     super().options()

    def save_binary_file_in_folder(self, binary_file, folder_with_file_name):
        """
        :param binary_file: a file in binary
        :param folder_with_file_name: file name of the zip with the path (e.g. /tmp/vgiws/points.zip)
        :return:
        """
        # save the zip with the shp inside the temp folder
        output_file = open(folder_with_file_name, 'wb')  # wb - write binary
        output_file.write(binary_file)
        output_file.close()

    def extract_zip_in_folder(self, folder_with_file_name, folder_to_extract_zip):
        """
        :param folder_with_file_name: file name of the zip with the path (e.g. /tmp/vgiws/points.zip)
        :param folder_to_extract_zip: folder where will extract the zip (e.g. /tmp/vgiws/points)
        :return:
        """
        # extract the zip in a folder
        with ZipFile(folder_with_file_name, "r") as zip_reference:

            # if exist one shapefile inside the zip, so extract the zip, else raise an exception
            if exist_shapefile_inside_zip(zip_reference):
                zip_reference.extractall(folder_to_extract_zip)
            else:
                raise HTTPError(400, "Invalid ZIP! It is necessary to exist a ShapeFile (.shp) inside de ZIP.")

    def import_shp_file_into_postgis(self, f_table_name, shape_file_name, folder_to_extract_zip):
        """
        :param f_table_name: name of the feature table that will be created
        :param folder_to_extract_zip: folder where will extract the zip (e.g. /tmp/vgiws/points)
        :return:
        """

        __DB_CONNECTION__ = self.PGSQLConn.get_db_connection()

        postgresql_connection = '"host=' + __DB_CONNECTION__["HOSTNAME"] + ' dbname=' + __DB_CONNECTION__["DATABASE"] + \
                                ' user=' + __DB_CONNECTION__["USERNAME"] + ' password=' + __DB_CONNECTION__[
                                    "PASSWORD"] + '"'
        try:
            command_to_import_shp_into_postgis = 'ogr2ogr -append -f "PostgreSQL" PG:' + postgresql_connection + ' ' + shape_file_name + \
                                                 ' -nln ' + f_table_name + ' -skipfailures'

            # call a process to execute the command to import the SHP into the PostGIS
            check_call(command_to_import_shp_into_postgis, cwd=folder_to_extract_zip, shell=True)

        except CalledProcessError as error:
            raise HTTPError(500, "Problem when import a resource. Please, contact the administrator.")

    def import_shp(self):
        arguments = self.get_aguments()

        # remove the extension of the file name (e.g. points)
        FILE_NAME_WITHOUT_EXTENSION = arguments["file_name"].replace(".zip", "")

        # layers = self.PGSQLConn.get_layers(f_table_name=FILE_NAME_WITHOUT_EXTENSION)
        # print("\nlayers: ", layers, "\n")
        # TODO: verificar se a já nao existe f_table_name no DB

        # if do not exist the temp folder, create it
        if not exists(__TEMP_FOLDER__):
            makedirs(__TEMP_FOLDER__)

        # the file needs to be in a zip file
        if not arguments["file_name"].endswith(".zip"):
            raise HTTPError(400, "Invalid file name: " + str(arguments["file_name"]))

        # file name of the zip (e.g. /tmp/vgiws/points.zip)
        ZIP_FILE_NAME = __TEMP_FOLDER__ + arguments["file_name"]
        # folder where will extract the zip (e.g. /tmp/vgiws/points)
        EXTRACTED_ZIP_FOLDER_NAME = __TEMP_FOLDER__ + FILE_NAME_WITHOUT_EXTENSION
        # name of the SHP file in folder (e.g. /tmp/vgiws/points/points.shp)
        SHP_FILE_NAME = FILE_NAME_WITHOUT_EXTENSION + ".shp"

        # get the binary file in body of the request
        binary_file = self.request.body

        self.save_binary_file_in_folder(binary_file, ZIP_FILE_NAME)

        self.extract_zip_in_folder(ZIP_FILE_NAME, EXTRACTED_ZIP_FOLDER_NAME)

        self.import_shp_file_into_postgis(arguments["f_table_name"], SHP_FILE_NAME, EXTRACTED_ZIP_FOLDER_NAME)




# FEATURE TABLE


# class APIFeatureTable(BaseHandlerFeatureTable):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/feature_table/?(?P<param>[A-Za-z0-9-]+)?/",
#             r"/api/feature_table/?(?P<param>[A-Za-z0-9-]+)?"]
#
#     # def get(self, param=None):
#     #     # self.get_method_api_layer()
#     #     self.get_method_api_feature()
#
#     @auth_non_browser_based
#     def put(self, param=None):
#         # self.put_method_api_layer(param)
#         self._create_feature()
#
#     # @auth_non_browser_based
#     # def delete(self, param=None):
#     #     self.delete_method_api_feature(param)
#
#     # def options(self, param=None):
#     #     super().options()



# CHANGESET

# class APIChangeset(BaseHandlerChangeset):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/changeset/?(?P<param>[A-Za-z0-9-]+)?/?(?P<param2>[A-Za-z0-9-]+)?"]
#
#     def get(self, param=None, param2=None):
#         self.get_method_api_feature()
#         # self.get_method_api_changeset()
#
#     @auth_non_browser_based
#     def put(self, param=None, param2=None):
#         # self.put_method_api_changeset(param, param2)
#         self.put_method_api_feature(param, param2)
#
#     @auth_non_browser_based
#     def delete(self, param=None, param2=None):
#         # self.delete_method_api_changeset(param)
#         self.delete_method_api_feature(param)


# NOTIFICATION

# class APINotification(BaseHandlerNotification):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/notification/?(?P<param>[A-Za-z0-9-]+)?/",
#             r"/api/notification/?(?P<param>[A-Za-z0-9-]+)?"]
#
#     def get(self, param=None):
#         self.get_method_api_feature()
#
#     @auth_non_browser_based
#     def put(self, param=None):
#         self.put_method_api_feature(param)
#
#     @auth_non_browser_based
#     def delete(self, param=None):
#         self.delete_method_api_feature(param)
