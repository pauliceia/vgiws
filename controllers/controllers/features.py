#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create controllers.
"""

import os
import zipfile

from ..base import BaseHandlerLayer, auth_non_browser_based  #, BaseHandlerChangeset
from tornado.web import HTTPError


# USER IN GROUP

# class APIUserGroup(BaseHandlerUserGroup):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/user_group/?(?P<param>[A-Za-z0-9-]+)?/",
#             r"/api/user_group/?(?P<param>[A-Za-z0-9-]+)?"]
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


# GROUP

# class APIGroup(BaseHandlerGroup):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/group/?(?P<param>[A-Za-z0-9-]+)?/",
#             r"/api/group/?(?P<param>[A-Za-z0-9-]+)?"]
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


# PROJECT

# class APIProject(BaseHandlerProject):
#
#     # A list of URLs that can be use for the HTTP methods
#     urls = [r"/api/project/?(?P<param>[A-Za-z0-9-]+)?/",
#             r"/api/project/?(?P<param>[A-Za-z0-9-]+)?"]
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

    # def options(self, param=None):
    #     super().options()


TEMP_FOLDER = "/tmp/vgiws/"



def exist_shapefile_inside_zip(zip_reference):
    list_file_names_of_zip = zip_reference.namelist()

    for file_name_in_zip in list_file_names_of_zip:
        # if exist a SHP file inside the zip, return true
        if file_name_in_zip.endswith(".shp"):
            return True

    return False


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
        arguments = self.get_aguments()

        # print("arguments: ", arguments["f_table_name"])
        # print("arguments: ", arguments["file_name"])

        if param == "shp":
            # if do not exist the temp folder, create it
            if not os.path.exists(TEMP_FOLDER):
                os.makedirs(TEMP_FOLDER)

            # the file needs to be in a zip file
            if not arguments["file_name"].endswith(".zip"):
                raise HTTPError(400, "Invalid file name: " + str(arguments["file_name"]))

            # file name of the zip (e.g. /tmp/vgiws/points.zip)
            ZIP_FILE_NAME = TEMP_FOLDER + arguments["file_name"]
            # remove the extension of the file name (e.g. points)
            FILE_NAME_WITHOUT_EXTENSION = arguments["file_name"].replace(".zip", "")
            # folder where will extract the zip (e.g. /tmp/vgiws/points)
            EXTRACTED_ZIP_FOLDER_NAME = TEMP_FOLDER + FILE_NAME_WITHOUT_EXTENSION
            # name of the SHP file in folder (e.g. /tmp/vgiws/points/points.shp)
            SHP_FILE_NAME = EXTRACTED_ZIP_FOLDER_NAME + FILE_NAME_WITHOUT_EXTENSION + ".shp"

            # get the file
            binary_file = self.request.body

            # save the zip with the shp inside the temp folder
            output_file = open(ZIP_FILE_NAME, 'wb')  # wb - write binary
            output_file.write(binary_file)
            output_file.close()

            # extract the zip in a folder
            with zipfile.ZipFile(ZIP_FILE_NAME, "r") as zip_reference:

                # if exist one shapefile inside the zip, so extract the zip, else raise an exception
                if exist_shapefile_inside_zip(zip_reference):
                    zip_reference.extractall(EXTRACTED_ZIP_FOLDER_NAME)
                else:
                    raise HTTPError(400, "Invalid ZIP! It is necessary to exist a ShapeFile (.shp) inside de ZIP")

        else:
            raise HTTPError(404, "Invalid parameter: " + str(param))

    # @auth_non_browser_based
    # def delete(self, param=None):
    #     self.delete_method_api_feature(param)

    # def options(self, param=None):
    #     super().options()

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
