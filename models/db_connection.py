#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Create a file named:
    vgi_ws_pauliceia/settings/db_settings.py

    With the follow content:

    __PGSQL_CONNECTION_SETTINGS__ = {
        "HOSTNAME": "HOSTNAME",
        "USERNAME": "USERNAME",
        "PASSWORD": "PASSWORD",
        "DATABASE": "DATABASE",
        "PORT": 5432
    }

    This __PGSQL_CONNECTION_SETTINGS__ dictionary is the connection with PostgreSQL
"""

from abc import ABCMeta
from requests import Session
from requests.exceptions import ConnectionError
from copy import deepcopy
from json import dumps

from tornado.web import HTTPError

from psycopg2 import connect, DatabaseError, ProgrammingError, Error
from psycopg2.extras import RealDictCursor

from modules.design_pattern import Singleton

from settings.db_settings import __PGSQL_CONNECTION_SETTINGS__, __DEBUG_PGSQL_CONNECTION_SETTINGS__, \
                                    __GEOSERVER_CONNECTION_SETTINGS__, __DEBUG_GEOSERVER_CONNECTION_SETTINGS__, \
                                    __GEOSERVER_REST_CONNECTION_SETTINGS__
from settings.settings import __SPATIAL_BB__

from .util import *


def run_if_can_publish_layers_in_geoserver(method):

    def wrapper(self, *args, **kwargs):
        if self.PUBLISH_LAYERS_IN_GEOSERVER:
            method(self, *args, **kwargs)

    return wrapper


def validate_feature_json(feature_json):
    properties = feature_json["properties"]
    # tags = feature_json["tags"]

    # if tags if not instance of dict, raise exception
    # if not isinstance(tags, dict):
    #     raise HTTPError(400, "The 'tags' attribute must be a JSON, it is " + str(type(tags)))

    if not isinstance(properties, dict):
        raise HTTPError(400, "The 'properties' attribute must be a JSON, it is " + str(type(properties)))


class BaseDBConnection(metaclass=ABCMeta):

    def __init__(self):
        self.__DB_STATUS__ = False

    def set_connection_status(self, status=True):
        self.__DB_STATUS__ = status

    def get_connection_status(self, readable=False):
        if readable:
            return "online" if self.__DB_STATUS__ else "offline"

        return self.__DB_STATUS__


@Singleton
class PGSQLConnection:

    def __init__(self, debug_mode, publish_layers_in_geoserver):
        self.DEBUG_MODE = debug_mode
        self.PUBLISH_LAYERS_IN_GEOSERVER = publish_layers_in_geoserver

        if self.DEBUG_MODE:
            # self.__connect__(__DEBUG_PGSQL_CONNECTION_SETTINGS__)
            self.__DB_CONNECTION__ = __DEBUG_PGSQL_CONNECTION_SETTINGS__
            self.__GEOSERVER_CONNECTION__ = __DEBUG_GEOSERVER_CONNECTION_SETTINGS__
        else:
            # self.__connect__(__PGSQL_CONNECTION_SETTINGS__)
            self.__DB_CONNECTION__ = __PGSQL_CONNECTION_SETTINGS__
            self.__GEOSERVER_CONNECTION__ = __GEOSERVER_CONNECTION_SETTINGS__

        self.__GEOSERVER_REST_CONNECTION_SETTINGS__ = __GEOSERVER_REST_CONNECTION_SETTINGS__

        # create a browser simulator to connect with geoserver
        self.__SESSION__ = Session()
        self.__URL_GEOSERVER_REST__ = "http://{0}:{1}".format(self.__GEOSERVER_REST_CONNECTION_SETTINGS__["HOSTNAME"],
                                                              self.__GEOSERVER_REST_CONNECTION_SETTINGS__["PORT"])

    def __connect__(self, __connection_settings__):
        """
        Do the DB connection with the '__pgsql_connection_settings__'
        :param __connection_settings__: the connection settings of PostgreSQL.
        It can be for the normal DB or test DB
        :return:
        """
        try:
            self.__PGSQL_CONNECTION__ = connect(host=__connection_settings__["HOSTNAME"],
                                                port=__connection_settings__["PORT"],
                                                user=__connection_settings__["USERNAME"],
                                                password=__connection_settings__["PASSWORD"],
                                                dbname=__connection_settings__["DATABASE"])

            # cursor_factory=RealDictCursor means that the "row" of the table will be
            # represented by a dictionary in python
            self.__PGSQL_CURSOR__ = self.__PGSQL_CONNECTION__.cursor(cursor_factory=RealDictCursor)

            self.set_connection_status(status=True)
        except (DatabaseError, Exception) as error:
            print("PostgreSQL's connection was failed! \n")
            print("Error: ", error)
            print("Closing web service!")
            self.set_connection_status(status=False)
            exit(1)

    # status

    def get_connection_status(self, readable=False):
        if readable:
            return "online" if self.__DB_STATUS__ else "offline"

        return self.__DB_STATUS__

    def set_connection_status(self, status=True):
        self.__DB_STATUS__ = status

    def get_db_connection(self):
        return deepcopy(self.__DB_CONNECTION__)

    # "overwriting" some DB methods

    def close(self):
        """
        Close the PostgreSQL DB connection
        :return:
        """

        # send the modifications to DB, before to close the connection
        self.commit()

        # close the connection
        self.__PGSQL_CONNECTION__.close()

    def commit(self):
        """
            Just do the COMMIT operator in DB
        """

        self.__PGSQL_CONNECTION__.commit()

    def rollback(self):
        """
            Just do the ROLLBACK operator in DB
        """

        self.__PGSQL_CONNECTION__.rollback()

    def execute(self, query, is_transaction=False, is_sql_file=False):
        # open database connection
        self.__connect__(self.__DB_CONNECTION__)

        try:
            self.__PGSQL_CURSOR__.execute(query)

            # if query is a transaction statement, then commit the changes
            if is_transaction:
                self.commit()

            if is_sql_file:
                return None

            query = query.lower()

            try:
                # if this query was a SELECT clause
                if 'select' in query:
                    return self.__PGSQL_CURSOR__.fetchone()

                # if this query was a INSERT clause
                if 'insert' in query:
                    # id_in_a_dict = self.__PGSQL_CURSOR__.fetchone()

                    # # get the only one key inside the returned dict
                    # key = list(id_in_a_dict.keys())[0]

                    # # return the id of the inserted resource
                    # return id_in_a_dict[key]

                    return self.__PGSQL_CURSOR__.fetchone()

                # if this query was a UPDATE/DELETE clause
                elif 'update' in query or 'delete' in query:
                    return self.__PGSQL_CURSOR__.rowcount

                else:
                    return None
            except ProgrammingError:
                    return None

        except ProgrammingError as error:
            self.rollback()
            print('An error occurred during query execution: ', error)
            raise error

        # finally is always executed (both at try and except)
        finally:
            self.close()

    ################################################################################
    # GEOSERVER
    ################################################################################

    @run_if_can_publish_layers_in_geoserver
    def get_layers_from_geoserver(self):
        try:
            response = self.__SESSION__.get(self.__URL_GEOSERVER_REST__ + '/layers/{0}/{1}'.format(self.__GEOSERVER_CONNECTION__["WORKSPACE"],
                                                                                                   self.__GEOSERVER_CONNECTION__["DATASTORE"]))
        except ConnectionError as error:
            raise HTTPError(500, "It was not possible to connect with the geoserver-rest \n\n" + str(error))

        if response.status_code == 404:
            raise HTTPError(404, str(response))
        elif response.status_code == 500:
            raise HTTPError(500, str(response))

    @run_if_can_publish_layers_in_geoserver
    def publish_feature_table_in_geoserver(self, f_table_name, EPSG):
        request_body = {
            "workspace": self.__GEOSERVER_CONNECTION__["WORKSPACE"],
            "datastore": self.__GEOSERVER_CONNECTION__["DATASTORE"],
            "layer": f_table_name,
            "description": "Description",
            "projection": "EPSG: " + str(EPSG)
        }

        try:
            response = self.__SESSION__.post(self.__URL_GEOSERVER_REST__ + '/layer/publish', data=request_body)
        except ConnectionError as error:
            raise HTTPError(500, "It was not possible to connect with the geoserver-rest \n\n" + str(error))

        if response.status_code == 404:
            raise HTTPError(404, str(response.text))
        elif response.status_code == 500:
            raise HTTPError(500, str(response.text))

    @run_if_can_publish_layers_in_geoserver
    def unpublish_feature_table_in_geoserver(self, f_table_name):
        try:
            response = self.__SESSION__.delete(self.__URL_GEOSERVER_REST__ + '/layer/remove/{0}/{1}/{2}'.format(self.__GEOSERVER_CONNECTION__["WORKSPACE"],
                                                                                                                self.__GEOSERVER_CONNECTION__["DATASTORE"],
                                                                                                                f_table_name))
        except ConnectionError as error:
            raise HTTPError(500, "It was not possible to connect with the geoserver-rest \n\n" + str(error))

        if response.status_code == 404:
            raise HTTPError(404, str(response.text))
        elif response.status_code == 500:
            raise HTTPError(500, str(response.text))

    ################################################################################
    # USER
    ################################################################################

    def get_users(self, user_id=None, username=None, name=None, email=None, password=None):
        # the id have to be a int
        if is_a_invalid_id(user_id):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_user_table(user_id=user_id, username=username, name=name,
                                           email=email, password=password)

        # CREATE THE QUERY AND EXECUTE IT
        query = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'User',
                    'properties', json_build_object(
                        'user_id',        user_id,
                        'email',          email,
                        'username',       username,
                        'name',           name,
                        'created_at',     to_char(created_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'is_email_valid', is_email_valid,
                        'terms_agreed',   terms_agreed,
                        'login_date',     login_date,
                        'is_the_admin',   is_the_admin,
                        'receive_notification_by_email',   receive_notification_by_email,
                        'picture',        picture,
                        'social_id',      social_id,
                        'social_account', social_account
                    )
                ))
            ) AS row_to_json
            FROM
            {0}
        """.format(subquery)

        results_of_query = self.execute(query)

        ######################################################################
        # POST-PROCESSING
        ######################################################################

        # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
        if "row_to_json" in results_of_query:
            results_of_query = results_of_query["row_to_json"]

        # if there is not feature, returns an empty list
        if results_of_query["features"] is None:
            results_of_query["features"] = []

        return results_of_query

    def create_user(self, resource_json, verified_social_login_email=False):
        p = resource_json["properties"]

        # TODO: temporarily all users will be registered with is_email_valid=True.
        #       after it returns to normal, undo the changes
        # if verified_social_login_email:
        #     p["is_email_valid"] = True
        # else:
        #     p["is_email_valid"] = False
        p["is_email_valid"] = True

        if "picture" not in p:
            p["picture"] = ""
        if "social_id" not in p:
            p["social_id"] = ""
        if "social_account" not in p:
            p["social_account"] = ""

        query = """
            INSERT INTO pauliceia_user (email, username, name, password, created_at,
                                        terms_agreed, receive_notification_by_email, is_email_valid,
                                        picture, social_id, social_account)
            VALUES ('{0}', '{1}', '{2}', '{3}', LOCALTIMESTAMP, {4}, {5}, {6}, '{7}', '{8}', '{9}')
            RETURNING user_id;
        """.format(p["email"], p["username"], p["name"], p["password"],
                   p["terms_agreed"], p["receive_notification_by_email"], p["is_email_valid"],
                   p["picture"], p["social_id"], p["social_account"])

        return self.execute(query, is_transaction=True)

    def update_user_email_is_valid(self, user_id, is_email_valid=True):
        query = """
            UPDATE pauliceia_user SET is_email_valid = {1}
            WHERE user_id = {0};
        """.format(user_id, is_email_valid)

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    def update_user_password(self, user_id, new_password):
        query = """
            UPDATE pauliceia_user SET password = '{1}'
            WHERE user_id = {0};
        """.format(user_id, new_password)

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    def update_user(self, resource_json, user_id):
        p = resource_json["properties"]

        query = """
            UPDATE pauliceia_user SET email = '{1}', username = '{2}', name = '{3}',
                                        terms_agreed = {4}, receive_notification_by_email = {5}
            WHERE user_id = {0};
        """.format(p["user_id"], p["email"], p["username"], p["name"],
                   p["terms_agreed"], p["receive_notification_by_email"])

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    def delete_user(self, feature_id):
        if is_a_invalid_id(feature_id):
            raise HTTPError(400, "Invalid parameter.")

        query = """
            DELETE FROM pauliceia_user WHERE user_id={0};
        """.format(feature_id)

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    ################################################################################
    # CURATOR
    ################################################################################

    def get_curators(self, user_id=None, keyword_id=None, region=None):
        # the id have to be a int
        if is_a_invalid_id(user_id) or is_a_invalid_id(keyword_id):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_curator_table(user_id=user_id, keyword_id=keyword_id, region=region)

        # CREATE THE QUERY AND EXECUTE IT
        query = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'Curator',
                    'properties', json_build_object(
                        'user_id',     user_id,
                        'keyword_id',  keyword_id,
                        'region',      region,
                        'created_at',  to_char(created_at, 'YYYY-MM-DD HH24:MI:SS')
                    )
                ))
            ) AS row_to_json
            FROM
            {0}
        """.format(subquery)

        results_of_query = self.execute(query)

        ######################################################################
        # POST-PROCESSING
        ######################################################################

        # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
        if "row_to_json" in results_of_query:
            results_of_query = results_of_query["row_to_json"]

        # if there is not feature, returns an empty list
        if results_of_query["features"] is None:
            results_of_query["features"] = []

        return results_of_query

    def create_curator(self, resource_json, user_id):
        p = resource_json["properties"]

        query = """
            INSERT INTO curator (user_id, keyword_id, region, created_at)
            VALUES ({0}, {1}, LOWER('{2}'), LOCALTIMESTAMP);
        """.format(p["user_id"], p["keyword_id"], p["region"])

        self.execute(query, is_transaction=True)

    def update_curator(self, resource_json, user_id):
        p = resource_json["properties"]

        query = """
            UPDATE curator SET region = LOWER('{2}')
            WHERE user_id = {0} AND keyword_id = {1};
        """.format(p["user_id"], p["keyword_id"], p["region"])

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    def delete_curator(self, user_id=None, keyword_id=None):
        if is_a_invalid_id(user_id) or is_a_invalid_id(keyword_id):
            raise HTTPError(400, "Invalid parameter.")

        # delete the curator
        if user_id is None:
            query = """
                DELETE FROM curator WHERE keyword_id = {0};
            """.format(keyword_id)
        elif keyword_id is None:
            query = """
                DELETE FROM curator WHERE user_id = {0};
            """.format(user_id)
        else:
            query = """
                DELETE FROM curator WHERE user_id = {0} AND keyword_id = {1};
            """.format(user_id, keyword_id)

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    ################################################################################
    # LAYER
    ################################################################################

    def get_layers(self, layer_id=None, f_table_name=None, is_published=None, keyword_id=None):
        # the id have to be a int
        if is_a_invalid_id(layer_id) or is_a_invalid_id(keyword_id):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_layer_table(layer_id=layer_id, f_table_name=f_table_name,
                                            is_published=is_published, keyword_id=keyword_id)

        # CREATE THE QUERY AND EXECUTE IT
        query = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'Layer',
                    'properties', json_build_object(
                        'layer_id',             layer_id,
                        'f_table_name',         f_table_name,
                        'name',                 name,
                        'description',          description,
                        'source_description',   source_description,
                        'created_at',           to_char(created_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'reference',            reference_.jsontags,
                        'keyword',              keyword.jsontags
                    )
                ))
            ) AS row_to_json
            FROM
            {0}
            CROSS JOIN LATERAL (
                -- (3) get the references of some resource on JSON format
                SELECT json_agg(reference_id) AS jsontags
                FROM
                (
                    -- (2) get the references of some resource
                    SELECT reference_id
                    FROM layer_reference
                    WHERE layer_id = layer.layer_id
                    ORDER BY reference_id
                ) subquery
            ) AS reference_
            CROSS JOIN LATERAL (
                -- (3) get the keywords of some resource on JSON format
                SELECT json_agg(keyword_id) AS jsontags
                FROM
                (
                    -- (2) get the keywords of some resource
                    SELECT keyword_id
                    FROM layer_keyword
                    WHERE layer_id = layer.layer_id
                    ORDER BY keyword_id
                ) subquery
            ) AS keyword
        """.format(subquery)

        results_of_query = self.execute(query)

        ######################################################################
        # POST-PROCESSING
        ######################################################################

        # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
        if "row_to_json" in results_of_query:
            results_of_query = results_of_query["row_to_json"]

        # if there is not feature, returns an empty layer
        if results_of_query["features"] is None:
            results_of_query["features"] = []

        return results_of_query

    def add_layer_in_db(self, properties):
        p = properties

        query = """
            INSERT INTO layer (f_table_name, name, description, source_description, created_at)
            VALUES ('{0}', '{1}', '{2}', '{3}', LOCALTIMESTAMP) RETURNING layer_id;
        """.format(p["f_table_name"], p["name"], p["description"], p["source_description"])

        return self.execute(query, is_transaction=True)

    def create_layer(self, resource_json, user_id):
        ##################################################
        # pre-processing
        ##################################################
        validate_feature_json(resource_json)

        properties = resource_json["properties"]

        # just can add reference/keyword that is a list
        if (not isinstance(properties["reference"], list)) or (not isinstance(properties["keyword"], list)):
            raise HTTPError(400, "The parameters reference and keyword need to be a list.")

        ##################################################
        # add the layer in db
        ##################################################
        id_in_json = self.add_layer_in_db(properties)

        ##################################################
        # add the list of reference in layer
        ##################################################
        for reference_id in properties["reference"]:
            layer_keyword_json = {
                "properties": {"layer_id": id_in_json["layer_id"], "reference_id": reference_id},
                'type': 'LayerReference'
            }
            self.create_layer_reference(layer_keyword_json)

        ##################################################
        # add the list of keyword in layer
        ##################################################
        for keyword_id in properties["keyword"]:
            layer_keyword_json = {
                "properties": {"layer_id": id_in_json["layer_id"], "keyword_id": keyword_id},
                'type': 'LayerKeyword'
            }
            self.create_layer_keyword(layer_keyword_json)

        ##################################################
        # add the user as creator user
        ##################################################
        user_layer_json = {
            'properties': {'is_the_creator': True, 'user_id': user_id, 'layer_id': id_in_json["layer_id"]},
            'type': 'UserLayer'
        }
        self.create_user_layer(user_layer_json, user_id)

        return id_in_json

    def update_table_name(self, old_table_name, new_table_name):
        query = """
            ALTER TABLE IF EXISTS {0}
            RENAME TO {1};
        """.format(old_table_name, new_table_name)

        self.execute(query, is_transaction=True)

    def update_layer_in_db(self, properties):
        p = properties

        query = """
            UPDATE layer SET name = '{1}', description = '{2}', source_description = '{3}'
            WHERE layer_id = {0};
        """.format(p["layer_id"], p["name"], p["description"], p["source_description"])

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    def update_layer(self, resource_json, user_id):
        ##################################################
        # pre-processing
        ##################################################
        new_layer_properties = resource_json["properties"]

        # just can add reference/keyword that is a list
        if (not isinstance(new_layer_properties["reference"], list)) or (not isinstance(new_layer_properties["keyword"], list)):
            raise HTTPError(400, "The parameters reference and keyword need to be a list.")

        # check if the references exist in the database before updating the layer
        for reference_id in new_layer_properties['reference']:
            reference = self.get_references(reference_id)
            if not reference['features']:
                raise HTTPError(404, "Not found the reference `{0}`.".format(reference_id))

        # check if the keywords exist in the database before updating the layer
        for keyword_id in new_layer_properties['keyword']:
            keyword = self.get_keywords(keyword_id)
            if not keyword['features']:
                raise HTTPError(404, "Not found the keyword `{0}`.".format(keyword_id))

        # get the old layer properties
        old_layer_properties = self.get_layers(layer_id=new_layer_properties["layer_id"])["features"][0]["properties"]

        ##################################################
        # update the layer in db
        ##################################################
        self.update_layer_in_db(new_layer_properties)

        ##################################################
        # remove the references and keywords from layer
        ##################################################
        try:
            self.delete_layer_reference(layer_id=new_layer_properties["layer_id"])
        except HTTPError as error:
            if error.status_code != 404:
                raise error
            # else:
            # error 404 is expected, because when update a layer, may exist a layer without reference

        try:
            self.delete_layer_keyword(layer_id=new_layer_properties["layer_id"])
        except HTTPError as error:
            if error.status_code != 404:
                raise error
            # else:
            # error 404 is expected, because when update a layer, may exist a layer without keyword

        ##################################################
        # add the list of references in layer
        ##################################################
        for reference_id in new_layer_properties["reference"]:
            layer_keyword_json = {
                "properties": {"layer_id": new_layer_properties["layer_id"], "reference_id": reference_id},
                'type': 'LayerReference'
            }
            self.create_layer_reference(layer_keyword_json)

        ##################################################
        # add the list of keywords in layer
        ##################################################
        for keyword_id in new_layer_properties["keyword"]:
            layer_keyword_json = {
                "properties": {"layer_id": new_layer_properties["layer_id"], "keyword_id": keyword_id},
                'type': 'LayerKeyword'
            }
            self.create_layer_keyword(layer_keyword_json)

        ##################################################
        # if the table_name was changed, so update the feature table name, version the f_table_name of temporal columns
        ##################################################
        # if old_layer_properties["f_table_name"] != new_layer_properties["f_table_name"]:
        #     # update the feature table
        #     self.update_table_name(old_layer_properties["f_table_name"], new_layer_properties["f_table_name"])
        #     # update the version feature table
        #     self.update_table_name("version_" + old_layer_properties["f_table_name"], "version_" + new_layer_properties["f_table_name"])
        #     # update the temporal columns
        #     self.update_temporal_columns_f_table_name(old_layer_properties["f_table_name"], new_layer_properties["f_table_name"])

    def delete_layer_dependencies(self, layer_id):
        # get the layer information before to remove the layer
        layer = self.get_layers(layer_id=layer_id)

        if not layer["features"]:  # if list is empty
            raise HTTPError(404, "Not found the layer `{0}`.".format(layer_id))

        f_table_name = layer["features"][0]["properties"]["f_table_name"]

        # 1) delete all users from layer
        self.delete_user_layer(layer_id=layer_id)

        try:
            # 2) delete all keywords from layer
            self.delete_layer_keyword(layer_id=layer_id)
        except HTTPError as error:
            if error.status_code != 404:
                raise error
            # else:
            # error 404 is expected, because when delete a layer, may exist a layer without keyword

        try:
            # 3) delete all references from layer
            self.delete_layer_reference(layer_id=layer_id)
        except HTTPError as error:
            if error.status_code != 404:
                raise error
            # else:
            # error 404 is expected, because when delete a layer, may exist a layer without reference

        try:
            # 4) delete all changesets from layer
            self.delete_changeset(layer_id=layer_id)
        except HTTPError as error:
            if error.status_code != 404:
                raise error
            # else:
            # error 404 is expected, because when delete a layer, may exist a layer without changeset

        try:
            # 5) delete the temporal metadata
            self.delete_temporal_columns(f_table_name)
        except HTTPError as error:
            if error.status_code != 404:
                raise error
            # else:
            # error 404 is expected, because when delete a layer, may exist a layer without time columns

        try:
            self.delete_feature_table(f_table_name)
        except ProgrammingError as error:
            raise HTTPError(500, str(error))

    def delete_layer(self, layer_id):
        if is_a_invalid_id(layer_id):
            raise HTTPError(400, "Invalid parameter.")

        # delete layer dependencies
        self.delete_layer_dependencies(layer_id)

        # delete the layer
        query = """
            DELETE FROM layer WHERE layer_id={0};
        """.format(layer_id)

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    ################################################################################
    # FEATURE TABLE
    ################################################################################

    def get_feature_table(self, f_table_name=None):
        subquery = get_subquery_feature_table(f_table_name=f_table_name)

        # CREATE THE QUERY AND EXECUTE IT
        query = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',        'FeatureTable',
                    'properties',   dict,
                    'f_table_name', f_table_name,
                    'geometry',  json_build_object(
                        'type',      type,
                        'crs',  json_build_object(
                            'type',      'name',
                            'properties', json_build_object('name', 'EPSG:' || srid)
                        )
                    )
                ))
            ) AS row_to_json
            FROM
            {0}
        """.format(subquery)

        results_of_query = self.execute(query)

        ######################################################################
        # POST-PROCESSING
        ######################################################################

        # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
        if "row_to_json" in results_of_query:
            results_of_query = results_of_query["row_to_json"]

        # if there is not feature, returns an empty list
        if results_of_query["features"] is None:
            results_of_query["features"] = []

        return results_of_query

    def create_feature_table(self,  resource_json, user_id):
        f_table_name = resource_json["f_table_name"]
        geometry_type = resource_json["geometry"]["type"]
        EPSG = resource_json["geometry"]["crs"]["properties"]["name"].split(":")[1]
        properties = resource_json["properties"]

        # get the attributes of the feature table
        properties_string = ""
        for property in properties:
            properties_string += property + " " + properties[property] + ", \n"

        tables_to_create = [f_table_name, "version_{0}".format(f_table_name)]

        for table_to_create in tables_to_create:
            # create the feature table
            query = """
                CREATE TABLE {0} (
                  id SERIAL,
                  geom GEOMETRY({1}, {2}) NOT NULL,
                  {3}
                  version INT NOT NULL DEFAULT 1,
                  changeset_id INT NOT NULL,
                  PRIMARY KEY (id),
                  CONSTRAINT constraint_changeset_id
                    FOREIGN KEY (changeset_id)
                    REFERENCES changeset (changeset_id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
                );
            """.format(table_to_create, geometry_type, EPSG, properties_string)

            self.execute(query, is_transaction=True)

        # add the is_removed column in version feature table
        version_table = tables_to_create[1]

        query = """
            ALTER TABLE {0}
            ADD COLUMN is_removed BOOLEAN DEFAULT FALSE;
        """.format(version_table)

        self.execute(query, is_transaction=True)

        # publish the features tables/layers in geoserver
        self.publish_feature_table_in_geoserver(f_table_name, EPSG)

    # def update_feature_table(self,  resource_json, user_id):
    #     f_table_name = resource_json["f_table_name"]
    #     geometry_type = resource_json["geometry"]["type"]
    #     EPSG = resource_json["geometry"]["crs"]["properties"]["name"].split(":")[1]
    #     properties = resource_json["properties"]

    #     # properties = remove_unnecessary_properties(properties)

    #     # get the attributes of the feature table
    #     properties_string = ""
    #     for property in properties:
    #         properties_string += property + " " + properties[property] + ", \n"

    #     tables_to_create = [f_table_name, "version_{0}".format(f_table_name)]

    #     for table_to_create in tables_to_create:
    #         # create the feature table
    #         query = """
    #             CREATE TABLE {0} (
    #               id SERIAL,
    #               geom GEOMETRY({1}, {2}) NOT NULL,
    #               {3}
    #               version INT NOT NULL DEFAULT 1,
    #               changeset_id INT NOT NULL,
    #               PRIMARY KEY (id),
    #               CONSTRAINT constraint_changeset_id
    #                 FOREIGN KEY (changeset_id)
    #                 REFERENCES changeset (changeset_id)
    #                 ON DELETE CASCADE
    #                 ON UPDATE CASCADE
    #             );
    #         """.format(table_to_create, geometry_type, EPSG, properties_string)

    #         self.execute(query, is_transaction=True)

    #     # publish the features tables/layers in geoserver
    #     self.publish_feature_table_in_geoserver(f_table_name, EPSG)

    def delete_feature_table(self, f_table_name):
        tables_to_drop = [f_table_name, "version_{0}".format(f_table_name)]

        for table_to_drop in tables_to_drop:
            # delete the feature table
            query = """
                DROP TABLE IF EXISTS {0} CASCADE ;
            """.format(table_to_drop)

            self.execute(query, is_transaction=True)

        try:
            # unpublish the features table in geoserver
            self.unpublish_feature_table_in_geoserver(f_table_name)
        except HTTPError as error:
            if error.status_code != 404:
                raise error

    ################################################################################
    # FEATURE TABLE COLUMN
    ################################################################################

    def create_feature_table_column(self, resource_json):
        query = """
            ALTER TABLE {0}
            ADD COLUMN {1} {2};
        """.format(resource_json["f_table_name"], resource_json["column_name"], resource_json["column_type"])

        self.execute(query, is_transaction=True)

    def delete_feature_table_column(self, f_table_name, column_name):
        if column_name in ["id", "geom", "changeset_id", "version"]:
            raise HTTPError(400, "Invalid parameter.")

        query = """
            ALTER TABLE {0}
            DROP COLUMN {1} CASCADE;
        """.format(f_table_name, column_name)

        self.execute(query, is_transaction=True)

    ################################################################################
    # TEMPORAL COLUMNS
    ################################################################################

    def get_temporal_columns(self, f_table_name=None, start_date=None, end_date=None, start_date_gte=None, end_date_lte=None):
        # the id have to be a int
        # if is_a_invalid_id(user_id) or is_a_invalid_id(keyword_id):
        #     raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_temporal_columns_table(f_table_name=f_table_name, start_date=start_date, end_date=end_date,
                                                       start_date_gte=start_date_gte, end_date_lte=end_date_lte)

        # CREATE THE QUERY AND EXECUTE IT
        query = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'TemporalColumns',
                    'properties', json_build_object(
                        'f_table_name',            f_table_name,
                        'start_date_column_name',  start_date_column_name,
                        'end_date_column_name',    end_date_column_name,
                        'start_date',              to_char(start_date, 'YYYY-MM-DD'),
                        'end_date',                to_char(end_date, 'YYYY-MM-DD'),
                        'start_date_mask_id',      start_date_mask_id,
                        'end_date_mask_id',        end_date_mask_id
                    )
                ))
            ) AS row_to_json
            FROM
            {0}
        """.format(subquery)

        results_of_query = self.execute(query)

        ######################################################################
        # POST-PROCESSING
        ######################################################################

        # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
        if "row_to_json" in results_of_query:
            results_of_query = results_of_query["row_to_json"]

        # if there is not feature, return an empty list
        if results_of_query["features"] is None:
            results_of_query["features"] = []

        return results_of_query

    def create_temporal_columns(self, resource_json, user_id):
        p = resource_json["properties"]

        p["start_date_column_name"] = p["start_date_column_name"] if p["start_date_column_name"] is not None else ""
        p["end_date_column_name"] = p["end_date_column_name"] if p["end_date_column_name"] is not None else ""

        p["start_date_mask_id"] = p["start_date_mask_id"] if p["start_date_mask_id"] is not None else "NULL"
        p["end_date_mask_id"] = p["end_date_mask_id"] if p["end_date_mask_id"] is not None else "NULL"

        query = """
            INSERT INTO temporal_columns (f_table_name, start_date_column_name, end_date_column_name,
                                          start_date, end_date, start_date_mask_id, end_date_mask_id)
            VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', {5}, {6});
        """.format(p["f_table_name"], p["start_date_column_name"], p["end_date_column_name"],
                   p["start_date"], p["end_date"], p["start_date_mask_id"], p["end_date_mask_id"])

        self.execute(query, is_transaction=True)

    def update_temporal_columns_f_table_name(self, old_f_table_name, new_f_table_name):
        query = """
            UPDATE temporal_columns SET f_table_name='{1}'
            WHERE f_table_name = '{0}';
        """.format(old_f_table_name, new_f_table_name)

        self.execute(query, is_transaction=True)

    def update_temporal_columns(self, resource_json, user_id):
        p = resource_json["properties"]

        if p["start_date_mask_id"] is None:
            p["start_date_mask_id"] = "NULL"

        if p["end_date_mask_id"] is None:
            p["end_date_mask_id"] = "NULL"

        query = """
            UPDATE temporal_columns SET start_date_column_name='{1}', end_date_column_name='{2}', start_date='{3}', end_date='{4}',
                                        start_date_mask_id={5}, end_date_mask_id={6}
            WHERE f_table_name = '{0}';
        """.format(p["f_table_name"], p["start_date_column_name"], p["end_date_column_name"], p["start_date"], p["end_date"],
                   p["start_date_mask_id"], p["end_date_mask_id"])

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    def delete_temporal_columns(self, f_table_name):
        # if is_a_invalid_id(user_id) or is_a_invalid_id(keyword_id):
        #     raise HTTPError(400, "Invalid parameter.")

        # delete the temporal_columns
        query = """
            DELETE FROM temporal_columns WHERE f_table_name = '{0}';
        """.format(f_table_name)

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    ################################################################################
    # USER_LAYER
    ################################################################################

    def get_user_layers(self, layer_id=None, user_id=None, is_the_creator=None):
        # the id has to be an int
        # if is_the_creator is not None and is not instance of boolean, so is invalid
        if is_a_invalid_id(layer_id) or is_a_invalid_id(user_id) or \
                (is_the_creator is not None and not isinstance(is_the_creator, bool)):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_user_layer_table(layer_id=layer_id, user_id=user_id,
                                                 is_the_creator=is_the_creator)

        # CREATE THE QUERY AND EXECUTE IT
        query = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'UserLayer',
                    'properties', json_build_object(
                        'layer_id',        layer_id,
                        'user_id',         user_id,
                        'created_at',      to_char(created_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'is_the_creator',  is_the_creator
                    )
                ))
            ) AS row_to_json
            FROM
            {0}
        """.format(subquery)

        results_of_query = self.execute(query)

        ######################################################################
        # POST-PROCESSING
        ######################################################################

        # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
        if "row_to_json" in results_of_query:
            results_of_query = results_of_query["row_to_json"]

        # if there is not feature, return an empty list
        if results_of_query["features"] is None:
            results_of_query["features"] = []

        return results_of_query

    def create_user_layer(self, resource_json, user_id):
        p = resource_json["properties"]

        query = """
            INSERT INTO user_layer (layer_id, user_id, created_at, is_the_creator)
            VALUES ({0}, {1}, LOCALTIMESTAMP, {2});
        """.format(p["layer_id"], p["user_id"], p["is_the_creator"])

        self.execute(query, is_transaction=True)

        ##################################################
        # do the user follows the layer
        ##################################################
        try:
            layer_follower = {
                'properties': {'layer_id': p["layer_id"]},
                'type': 'LayerFollower'
            }
            self.create_layer_follower(layer_follower, p["user_id"])
        except Error as error:
            self.rollback()  # do a rollback to comeback in a safe state of DB
            # I expect a 23505, if a user already follows a layer, he keeps to follow
            if error.pgcode != "23505":  # 23505 - unique_violation
                raise error

    def delete_user_layer(self, user_id=None, layer_id=None):
        ##################################################
        # do the user follows the layer
        ##################################################
        try:
            self.delete_layer_follower(layer_id=layer_id, user_id=user_id)
        except HTTPError as error:
            # if the error is different of 404, raise a exception..., because I except a 404
            if error.status_code != 404:
                raise error
            else:
                pass

        # delete the user from a layer
        if is_a_invalid_id(user_id) or is_a_invalid_id(layer_id):
            raise HTTPError(400, "Invalid parameter.")

        if user_id is None:
            query = """
                DELETE FROM user_layer WHERE layer_id={0};
            """.format(layer_id)
        elif layer_id is None:
            query = """
                DELETE FROM user_layer WHERE user_id={0};
            """.format(user_id)
        else:
            query = """
                DELETE FROM user_layer WHERE user_id={0} AND layer_id={1};
            """.format(user_id, layer_id)

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    ################################################################################
    # REFERENCE
    ################################################################################

    def get_references(self, reference_id=None, user_id_creator=None, description=None):
        # the id have to be a int
        if is_a_invalid_id(reference_id) or is_a_invalid_id(user_id_creator):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_reference_table(reference_id=reference_id, description=description,
                                                user_id_creator=user_id_creator)

        # CREATE THE QUERY AND EXECUTE IT
        query = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'Reference',
                    'properties', json_build_object(
                        'reference_id',     reference_id,
                        'description',      description,
                        'user_id_creator',  user_id_creator
                    )
                ))
            ) AS row_to_json
            FROM
            {0}
        """.format(subquery)

        results_of_query = self.execute(query)

        ######################################################################
        # POST-PROCESSING
        ######################################################################

        # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
        if "row_to_json" in results_of_query:
            results_of_query = results_of_query["row_to_json"]

        # if there is not feature, returns an empty list
        if results_of_query["features"] is None:
            results_of_query["features"] = []

        return results_of_query

    def create_reference(self, resource_json, user_id):
        # put the current user id as the creator of the reference
        resource_json["properties"]["user_id"] = user_id

        p = resource_json["properties"]

        query = """
            INSERT INTO reference (description, user_id_creator)
            VALUES ('{0}', {1}) RETURNING reference_id;
        """.format(p["description"], p["user_id"])

        return self.execute(query, is_transaction=True)

    def update_reference(self, resource_json, user_id):
        p = resource_json["properties"]

        query = """
            UPDATE reference SET description = '{1}'
            WHERE reference_id={0};
        """.format(p["reference_id"], p["description"])

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    def delete_reference(self, resource_id):
        if is_a_invalid_id(resource_id):
            raise HTTPError(400, "Invalid parameter.")

        # delete the reference
        query = """
            DELETE FROM reference WHERE reference_id={0};
        """.format(resource_id)

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    ################################################################################
    # LAYER REFERENCE
    ################################################################################

    def get_layer_reference(self, layer_id=None, reference_id=None):
        if is_a_invalid_id(layer_id) or is_a_invalid_id(reference_id):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_layer_reference_table(layer_id=layer_id, reference_id=reference_id)

        # CREATE THE QUERY AND EXECUTE IT
        query_text = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'LayerReference',
                    'properties', json_build_object(
                        'layer_id',        layer_id,
                        'reference_id',    reference_id
                    )
                ))
            ) AS row_to_json
            FROM
            {0}
        """.format(subquery)

        results_of_query = self.execute(query_text)

        ######################################################################
        # POST-PROCESSING
        ######################################################################

        # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
        if "row_to_json" in results_of_query:
            results_of_query = results_of_query["row_to_json"]

        # if there is not feature
        if results_of_query["features"] is None:
            raise HTTPError(404, "Not found any resource.")

        return results_of_query

    def create_layer_reference(self, resource_json):
        p = resource_json["properties"]

        query = """
            INSERT INTO layer_reference (layer_id, reference_id)
            VALUES ({0}, {1});
        """.format(p["layer_id"], p["reference_id"])

        self.execute(query, is_transaction=True)

    def delete_layer_reference(self, layer_id=None, reference_id=None):
        if is_a_invalid_id(layer_id) or is_a_invalid_id(reference_id):
            raise HTTPError(400, "Invalid parameter.")

        if layer_id is not None and reference_id is None:
            query = """
                DELETE FROM layer_reference WHERE layer_id={0};
            """.format(layer_id)
        elif reference_id is not None and layer_id is None:
            query = """
                DELETE FROM layer_reference WHERE reference_id={0};
            """.format(reference_id)
        else:
            query = """
                DELETE FROM layer_reference WHERE layer_id={0} AND reference_id={1};
            """.format(layer_id, reference_id)

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    ################################################################################
    # KEYWORD
    ################################################################################

    def get_keywords(self, keyword_id=None, name=None, user_id_creator=None):
        # the id have to be a int
        if is_a_invalid_id(keyword_id) or is_a_invalid_id(user_id_creator):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_keyword_table(keyword_id=keyword_id, name=name, user_id_creator=user_id_creator)

        # CREATE THE QUERY AND EXECUTE IT
        query = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'Keyword',
                    'properties', json_build_object(
                        'keyword_id',      keyword_id,
                        'name',            name,
                        'user_id_creator', user_id_creator,
                        'created_at',      to_char(created_at, 'YYYY-MM-DD HH24:MI:SS')
                    )
                ))
            ) AS row_to_json
            FROM
            {0}
        """.format(subquery)

        results_of_query = self.execute(query)

        ######################################################################
        # POST-PROCESSING
        ######################################################################

        # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
        if "row_to_json" in results_of_query:
            results_of_query = results_of_query["row_to_json"]

        # if there is not feature, returns an empty list
        if results_of_query["features"] is None:
            results_of_query["features"] = []

        return results_of_query

    def create_keyword(self, resource_json, user_id):
        # put the current user id as the creator of the keyword
        resource_json["properties"]["user_id_creator"] = user_id

        p = resource_json["properties"]

        query = """
            INSERT INTO keyword (name, user_id_creator, created_at)
            VALUES ('{0}', {1}, LOCALTIMESTAMP) RETURNING keyword_id;
        """.format(p["name"], p["user_id_creator"])

        return self.execute(query, is_transaction=True)

    def update_keyword(self, resource_json, user_id):
        p = resource_json["properties"]

        query = """
            UPDATE keyword SET name = '{1}'
            WHERE keyword_id={0};
        """.format(p["keyword_id"], p["name"])

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    def delete_keyword(self, resource_id):
        if is_a_invalid_id(resource_id):
            raise HTTPError(400, "Invalid parameter.")

        # delete the reference
        query = """
            DELETE FROM keyword WHERE keyword_id={0};
        """.format(resource_id)

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    ################################################################################
    # LAYER KEYWORD
    ################################################################################

    # def get_layer_keywords(self, layer_id=None, user_id=None, is_the_creator=None):
    #     # the id has to be an int
    #     # if is_the_creator is not None and is not instance of boolean, so is invalid
    #     if is_a_invalid_id(layer_id) or is_a_invalid_id(user_id) or \
    #             (is_the_creator is not None and not isinstance(is_the_creator, bool)):
    #         raise HTTPError(400, "Invalid parameter.")
    #
    #     subquery = get_subquery_user_layer_table(layer_id=layer_id, user_id=user_id,
    #                                              is_the_creator=is_the_creator)
    #
    #     # CREATE THE QUERY AND EXECUTE IT
    #     query_text = """
    #         SELECT jsonb_build_object(
    #             'type', 'FeatureCollection',
    #             'features',   jsonb_agg(jsonb_build_object(
    #                 'type',       'UserLayer',
    #                 'properties', json_build_object(
    #                     'layer_id',        layer_id,
    #                     'user_id',         user_id,
    #                     'created_at',      to_char(created_at, 'YYYY-MM-DD HH24:MI:SS'),
    #                     'is_the_creator',  is_the_creator
    #                 )
    #             ))
    #         ) AS row_to_json
    #         FROM
    #         {0}
    #     """.format(subquery)
    #
    #     # do the query in database
    #     self.__PGSQL_CURSOR__.execute(query_text)
    #
    #     # get the result of query
    #     results_of_query = self.__PGSQL_CURSOR__.fetchone()
    #
    #     ######################################################################
    #     # POST-PROCESSING
    #     ######################################################################
    #
    #     # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
    #     if "row_to_json" in results_of_query:
    #         results_of_query = results_of_query["row_to_json"]
    #
    #     # if there is not feature
    #     if results_of_query["features"] is None:
    #         raise HTTPError(404, "Not found any resource.")
    #
    #     return results_of_query

    def create_layer_keyword(self, resource_json):
        p = resource_json["properties"]

        query = """
            INSERT INTO layer_keyword (layer_id, keyword_id)
            VALUES ({0}, {1});
        """.format(p["layer_id"], p["keyword_id"])

        self.execute(query, is_transaction=True)

    def delete_layer_keyword(self, layer_id=None, keyword_id=None):
        if is_a_invalid_id(layer_id) or is_a_invalid_id(keyword_id):
            raise HTTPError(400, "Invalid parameter.")

        if keyword_id is None:
            query = """
                DELETE FROM layer_keyword WHERE layer_id={0};
            """.format(layer_id)
        else:
            query = """
                DELETE FROM layer_keyword WHERE layer_id={0} AND keyword_id={1};
            """.format(layer_id, keyword_id)

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    ################################################################################
    # CHANGESET
    ################################################################################

    def get_changesets(self, changeset_id=None, layer_id=None, user_id_creator=None, open=None, closed=None):
        # the id have to be a int
        if is_a_invalid_id(changeset_id) or is_a_invalid_id(user_id_creator):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_changeset_table(changeset_id=changeset_id, layer_id=layer_id,
                                                user_id_creator=user_id_creator, open=open, closed=closed)

        # CREATE THE QUERY AND EXECUTE IT
        query = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'Changeset',
                    'properties', json_build_object(
                        'changeset_id',    changeset_id,
                        'description',     description,
                        'created_at',      to_char(created_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'closed_at',       to_char(closed_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'layer_id',        layer_id,
                        'user_id_creator', user_id_creator
                    )
                ))
            ) AS row_to_json
            FROM
            {0}
        """.format(subquery)

        # get the result of query
        results_of_query = self.execute(query)

        ######################################################################
        # POST-PROCESSING
        ######################################################################

        # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
        if "row_to_json" in results_of_query:
            results_of_query = results_of_query["row_to_json"]

        # if there is not feature, put an empty list
        if results_of_query["features"] is None:
            results_of_query["features"] = []

        return results_of_query

    def create_changeset(self, resource_json, user_id):
        # put the current user id as the creator of the keyword
        resource_json["properties"]["user_id_creator"] = user_id

        p = resource_json["properties"]

        query = """
            INSERT INTO changeset (created_at, layer_id, user_id_creator)
            VALUES (LOCALTIMESTAMP, {0}, {1}) RETURNING changeset_id;
        """.format(p["layer_id"], p["user_id_creator"])

        # get the result of query
        return self.execute(query, is_transaction=True)

    def close_changeset(self, resource_json, current_user_id):
        changeset_id = resource_json["properties"]["changeset_id"]

        if is_a_invalid_id(changeset_id):
            raise HTTPError(400, "Invalid parameter.")

        # check if the changeset is closed or not, if it is closed, raise 409 exception
        list_changesets = self.get_changesets(changeset_id=changeset_id)

        # if the list is empty, so raise an exception
        if not list_changesets['features']:
            raise HTTPError(404, "Not found the changeset `{0}`.".format(changeset_id))

        closed_at = list_changesets['features'][0]['properties']['closed_at']
        if closed_at is not None:
            raise HTTPError(409, "Changeset `{0}` has already been closed at `{1}`.".format(changeset_id, closed_at))

        # check if the user created the changeset
        user_id_creator = list_changesets['features'][0]['properties']['user_id_creator']
        if user_id_creator != current_user_id:
            raise HTTPError(409, "The user `{0}` didn't create the changeset `{1}`.".format(current_user_id, changeset_id))

        description = resource_json["properties"]["description"]
        query = """
            UPDATE changeset SET closed_at=LOCALTIMESTAMP, description='{1}'
            WHERE changeset_id={0};
        """.format(changeset_id, description)

        self.execute(query, is_transaction=True)

    def delete_changeset(self, changeset_id=None, layer_id=None):
        if is_a_invalid_id(changeset_id) or is_a_invalid_id(layer_id):
            raise HTTPError(400, "Invalid parameter.")

        if changeset_id is not None:
            # delete the reference
            query = """
                DELETE FROM changeset WHERE changeset_id={0};
            """.format(changeset_id)
        elif layer_id is not None:
            # delete the reference
            query = """
                DELETE FROM changeset WHERE layer_id={0};
            """.format(layer_id)
        else:
            raise HTTPError(400, "Invalid parameter.")

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    ################################################################################
    # NOTIFICATION
    ################################################################################

    def get_notification(self, notification_id=None, is_denunciation=None, user_id_creator=None,
                         layer_id=None, keyword_id=None, notification_id_parent=None):
        # the id have to be a int
        if is_a_invalid_id(notification_id) or is_a_invalid_id(user_id_creator) or is_a_invalid_id(layer_id) or \
                is_a_invalid_id(keyword_id) or is_a_invalid_id(notification_id_parent):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_notification_table(notification_id=notification_id, is_denunciation=is_denunciation,
                                                   user_id_creator=user_id_creator, layer_id=layer_id,
                                                   keyword_id=keyword_id, notification_id_parent=notification_id_parent)

        # CREATE THE QUERY AND EXECUTE IT
        query = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'Notification',
                    'properties', json_build_object(
                        'notification_id',     notification_id,
                        'description',      description,
                        'created_at',   to_char(created_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'is_denunciation',  is_denunciation,
                        'user_id_creator',     user_id_creator,
                        'layer_id',      layer_id,
                        'keyword_id',  keyword_id,
                        'notification_id_parent',  notification_id_parent
                    )
                ))
            ) AS row_to_json
            FROM
            {0}
        """.format(subquery)

        results_of_query = self.execute(query)

        ######################################################################
        # POST-PROCESSING
        ######################################################################

        # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
        if "row_to_json" in results_of_query:
            results_of_query = results_of_query["row_to_json"]

        # if there is not feature, returns an empty list
        if results_of_query["features"] is None:
            results_of_query["features"] = []

        return results_of_query

    def create_notification(self, resource_json, user_id):
        p = resource_json["properties"]

        # put the current user id as the creator of the reference
        p["user_id_creator"] = user_id

        if p["layer_id"] is None:
            p["layer_id"] = "NULL"

        if p["keyword_id"] is None:
            p["keyword_id"] = "NULL"

        if p["notification_id_parent"] is None:
            p["notification_id_parent"] = "NULL"

        query = """
            INSERT INTO notification (description, created_at, is_denunciation, user_id_creator,
                                      layer_id, keyword_id, notification_id_parent)
            VALUES ('{0}', LOCALTIMESTAMP, {1}, {2}, {3}, {4}, {5}) RETURNING notification_id;
        """.format(p["description"], p["is_denunciation"], p["user_id_creator"], p["layer_id"],
                   p["keyword_id"], p["notification_id_parent"])

        return self.execute(query, is_transaction=True)

    def update_notification(self, resource_json, user_id):
        p = resource_json["properties"]

        if p["layer_id"] is None:
            p["layer_id"] = "NULL"

        if p["keyword_id"] is None:
            p["keyword_id"] = "NULL"

        if p["notification_id_parent"] is None:
            p["notification_id_parent"] = "NULL"

        query = """
            UPDATE notification SET description = '{1}', layer_id = {2}, keyword_id = {3}, notification_id_parent = {4}
            WHERE notification_id={0};
        """.format(p["notification_id"], p["description"], p["layer_id"], p["keyword_id"], p["notification_id_parent"])

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    def delete_notification(self, notification_id):
        if is_a_invalid_id(notification_id):
            raise HTTPError(400, "Invalid parameter.")

        # delete the reference
        query = """
            DELETE FROM notification WHERE notification_id={0};
        """.format(notification_id)

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    def get_notification_related_to_user(self, user_id=None):
        # the id have to be a int
        if is_a_invalid_id(user_id):
            raise HTTPError(400, "Invalid parameter.")

        # if the code don't find the user, raise a 404 exception
        user = self.get_users(user_id=user_id)
        if not user["features"]:  # if the list is empty
            raise HTTPError(404, "Not found the user {0}.".format(user_id))

        subquery = get_subquery_notification_table_related_to_user(user_id=user_id)

        # CREATE THE QUERY AND EXECUTE IT
        query = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'Notification',
                    'properties', json_build_object(
                        'notification_id', notification_id,
                        'description',     description,
                        'created_at',      to_char(created_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'is_denunciation', is_denunciation,
                        'user_id_creator', user_id_creator,
                        'layer_id',        layer_id,
                        'keyword_id',      keyword_id,
                        'notification_id_parent',  notification_id_parent
                    )
                ))
            ) AS row_to_json
            FROM
            {0}
        """.format(subquery)

        results_of_query = self.execute(query)

        ######################################################################
        # POST-PROCESSING
        ######################################################################

        # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
        if "row_to_json" in results_of_query:
            results_of_query = results_of_query["row_to_json"]

        # if there is not feature, returns an empty list
        if results_of_query["features"] is None:
            results_of_query["features"] = []

        return results_of_query

    ################################################################################
    # IMPORT
    ################################################################################

    def create_new_table_with_the_schema_of_old_table(self, new_table_name, old_table_name):
        query = """
            CREATE TABLE {0} ( like {1} including all )
        """.format(new_table_name, old_table_name)

        self.execute(query, is_transaction=True)

    def add_version_column_in_table(self, table_name):
        query = """
            ALTER TABLE {0}
            ADD COLUMN version INT NOT NULL DEFAULT 1
        """.format(table_name)

        self.execute(query, is_transaction=True)

    def add_changeset_id_column_in_table(self, table_name):
        # create the column
        query = """
            ALTER TABLE {0} ADD COLUMN changeset_id INT
        """.format(table_name)

        self.execute(query, is_transaction=True)

        query = """
            ALTER TABLE {0}
            ADD CONSTRAINT constraint_changeset_id
            FOREIGN KEY (changeset_id)
                REFERENCES changeset (changeset_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        """.format(table_name)

        self.execute(query, is_transaction=True)

    def update_feature_table_setting_in_all_records_a_version(self, f_table_name, version):
        # create the column
        query = """
            UPDATE {0} SET version = {1};
        """.format(f_table_name, version)

        self.execute(query, is_transaction=True)

    def update_feature_table_setting_in_all_records_a_changeset_id(self, f_table_name, changeset_id):
        # create the column
        query = """
            UPDATE {0} SET changeset_id = {1};
        """.format(f_table_name, changeset_id)

        self.execute(query, is_transaction=True)

    # def check_if_the_inserted_shapefile_is_inside_the_spatial_bounding_box(self, f_table_name):
    #
    #     # 1 - make the geometries valid
    #     query_text = """
    #         UPDATE {0} SET geom = ST_MakeValid(geom)
    #         WHERE NOT ST_IsValid(geom);
    #     """.format(f_table_name)
    #
    #     # do the query in database
    #     self.__PGSQL_CURSOR__.execute(query_text)
    #
    #     # 2 - check if the shapefile is inside the default city
    #     # query_text = """
    #     #     -- SELECT ST_Contains(bb_default_city.geom, union_f_table.geom) as row_to_json
    #     #     SELECT ST_Contains(bb_default_city.geom, ST_MakeValid(union_f_table.geom)) as row_to_json
    #     #     -- SELECT ST_Intersects(union_f_table.geom, bb_default_city.geom) as row_to_json
    #     #     -- SELECT ST_Within(ST_Buffer(union_f_table.geom, 0), bb_default_city.geom) as row_to_json
    #     #     -- SELECT ST_Within(union_f_table.geom, bb_default_city.geom) as row_to_json
    #     #     FROM
    #     #     (
    #     #         -- get the union of a feature table (shapefile)
    #     #         SELECT ST_Transform(ST_Union(geom), 4326) as geom FROM {0}
    #     #     ) union_f_table,
    #     #     (
    #     #         -- create a bounding box of the default city (by default is SP city)
    #     #         SELECT  ST_Transform(
    #     #             ST_MakeEnvelope (
    #     #                 {1}, {2},
    #     #                 {3}, {4},
    #     #                 {5}
    #     #             )
    #     #         , 4326) as geom
    #     #     ) bb_default_city;
    #     # """.format(f_table_name, __SPATIAL_BB__["xmin"], __SPATIAL_BB__["ymin"],
    #     #                          __SPATIAL_BB__["xmax"], __SPATIAL_BB__["ymax"], __SPATIAL_BB__["EPSG"])
    #
    #     # do the clean db add the function verify_if_geometry_is_inside_other_geometry automatically
    #     query_text = """
    #         SELECT verify_if_geometry_is_inside_other_geometry('{0}', {1}, {2}, {3}, {4}, {5})
    #     """.format(f_table_name, __SPATIAL_BB__["xmin"], __SPATIAL_BB__["ymin"],
    #                __SPATIAL_BB__["xmax"], __SPATIAL_BB__["ymax"], __SPATIAL_BB__["EPSG"])
    #
    #     # print(query_text)
    #
    #     # do the query in database
    #     self.__PGSQL_CURSOR__.execute(query_text)
    #
    #     # get the result of query
    #     is_shapefile_inside_default_city = self.__PGSQL_CURSOR__.fetchone()
    #
    #     if "row_to_json" in is_shapefile_inside_default_city:
    #         is_shapefile_inside_default_city = is_shapefile_inside_default_city["row_to_json"]
    #
    #     return is_shapefile_inside_default_city

    def bounding_box_of_shapefile_intersects_with_bounding_box_of_default_city(self, shapefile_bounds, shapefile_epsg):

        min_x, min_y, max_x, max_y = shapefile_bounds

        # check if the shapefile intersects with the default city
        query = """
            SELECT ST_Intersects(
                -- create a bounding box of the shapefile
                ST_Transform(ST_MakeEnvelope(
                    {0}, {1}, {2}, {3}, {4}
                ), 4326),
                -- create a bounding box of the default city (by default is SP city)
                ST_Transform(ST_MakeEnvelope(
                    {5}, {6}, {7}, {8}, {9}
                ), 4326)
            ) as row_to_json
        """.format(min_x, min_y, max_x, max_y, shapefile_epsg,
                   __SPATIAL_BB__["xmin"], __SPATIAL_BB__["ymin"],
                   __SPATIAL_BB__["xmax"], __SPATIAL_BB__["ymax"], __SPATIAL_BB__["EPSG"])

        is_shapefile_intersects_default_city = self.execute(query)

        if "row_to_json" in is_shapefile_intersects_default_city:
            is_shapefile_intersects_default_city = is_shapefile_intersects_default_city["row_to_json"]

        return is_shapefile_intersects_default_city

    ################################################################################
    # LAYER FOLLOWERS
    ################################################################################

    def get_layer_follower(self, layer_id=None, user_id=None):
        # the id have to be a int
        if is_a_invalid_id(layer_id) or is_a_invalid_id(user_id):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_layer_follower_table(layer_id=layer_id, user_id=user_id)

        # CREATE THE QUERY AND EXECUTE IT
        query = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'LayerFollower',
                    'properties', json_build_object(
                        'layer_id',     layer_id,
                        'user_id',      user_id,
                        'created_at',   to_char(created_at, 'YYYY-MM-DD HH24:MI:SS')
                    )
                ))
            ) AS row_to_json
            FROM
            {0}
        """.format(subquery)

        results_of_query = self.execute(query)

        ######################################################################
        # POST-PROCESSING
        ######################################################################

        # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
        if "row_to_json" in results_of_query:
            results_of_query = results_of_query["row_to_json"]

        # if there is not feature, return an empty list
        if results_of_query["features"] is None:
            results_of_query["features"] = []

        return results_of_query

    def create_layer_follower(self, resource_json, user_id):
        # put the current user id as the creator of the reference
        resource_json["properties"]["user_id"] = user_id

        p = resource_json["properties"]

        query = """
            INSERT INTO layer_followers (layer_id, user_id, created_at)
            VALUES ({0}, {1}, LOCALTIMESTAMP);
        """.format(p["layer_id"], p["user_id"])

        self.execute(query, is_transaction=True)

    def delete_layer_follower(self, layer_id=None, user_id=None):
        if is_a_invalid_id(layer_id) or is_a_invalid_id(user_id):
            raise HTTPError(400, "Invalid parameter.")

        if user_id is None:
            query = """
                DELETE FROM layer_followers WHERE layer_id={0};
            """.format(layer_id)
        elif layer_id is None:
            query = """
                DELETE FROM layer_followers WHERE user_id={0};
            """.format(user_id)
        else:
            query = """
                DELETE FROM layer_followers WHERE user_id={0} AND layer_id={1};
            """.format(user_id, layer_id)

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    ################################################################################
    # MASK
    ################################################################################

    def get_mask(self, mask_id=None):
        # the id have to be a int
        if is_a_invalid_id(mask_id):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_mask_table(mask_id=mask_id)

        # CREATE THE QUERY AND EXECUTE IT
        query = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'Mask',
                    'properties',  json_build_object(
                        'mask_id', mask_id,
                        'mask',    mask
                    )
                ))
            ) AS row_to_json
            FROM
            {0}
        """.format(subquery)

        results_of_query = self.execute(query)

        ######################################################################
        # POST-PROCESSING
        ######################################################################

        # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
        if "row_to_json" in results_of_query:
            results_of_query = results_of_query["row_to_json"]

        # if there is not feature, return an empty list
        if results_of_query["features"] is None:
            results_of_query["features"] = []

        return results_of_query

    ################################################################################
    # FEATURE
    ################################################################################

    def check_if_the_properties_are_valid(self, f_table_name, properties):
        list_of_column_name_with_type = self.get_columns_from_table(f_table_name)

        # if one column of the feature table is not specified in properties, so it is an invalid GeoJSON
        for column_name_with_type in list_of_column_name_with_type:
            # we can ignore the "geom" column, because it is not specified in properties
            if column_name_with_type["column_name"] == "geom":
                continue

            # if pass the "id", we can ignore
            if column_name_with_type["column_name"] == "id":
                continue

            # if pass the "is_removed", we can ignore
            if column_name_with_type["column_name"] == "is_removed":
                continue

            if not column_name_with_type["column_name"] in properties:
                raise HTTPError(400, "Some attribute in the JSON is missing. Look at the feature table structure! (error: " +
                                str(column_name_with_type["column_name"]) + " is missing).")

    def get_srid_from_table_name(self, table_name):
        query = """
            SELECT srid FROM geometry_columns WHERE f_table_name='{0}';
        """.format(table_name)

        result = self.execute(query)

        return result["srid"]

    def get_insert_statement_from_geojson(self, resource_json, remove_id_and_version_from_properties=True):
        column_names = []
        values = []

        properties = resource_json["properties"]
        f_table_name = resource_json["f_table_name"]

        self.check_if_the_properties_are_valid(f_table_name, properties)

        # it is not possible to set the id and version when create the feature in feature table,
        # however, it is possible to add these fields when we add the feature in the version table
        if remove_id_and_version_from_properties:
            if "id" in properties:
                del properties["id"]
            if "version" in properties:
                del properties["version"]

        for property_ in properties:
            if isinstance(properties[property_], int) or isinstance(properties[property_], float):
                value = str(properties[property_])
            elif isinstance(properties[property_], str):
                value = "'" + str(properties[property_]) + "'"
            elif properties[property_] is None:
                value = "NULL"
            else:
                raise HTTPError(500, "Invalid field of feature (" + property_ + ": " + str(properties[property_]) + ")."
                                + "Please contact the administrator.")

            column_names.append(property_)
            values.append(value)

        srid = self.get_srid_from_table_name(f_table_name)

        # put the GEOM attribute
        column_names.append("geom")
        values.append("ST_SetSRID(ST_GeomFromGeoJSON('" + str(dumps(resource_json["geometry"])) + "'), " + str(srid) + ")")

        column_names = ", ".join(column_names)
        values = ", ".join(values)

        insert_statement = """
            INSERT INTO {0} ({1}) VALUES ({2}) RETURNING id;
        """.format(f_table_name, column_names, values)

        return insert_statement

    def get_update_statement_from_geojson(self, resource_json):
        column_names = []
        values = []

        properties = resource_json["properties"]
        f_table_name = resource_json["f_table_name"]

        self.check_if_the_properties_are_valid(f_table_name, properties)

        # increment 1 in version attribute, to indicate the new version
        properties["version"] += 1

        # get the feature_id to use in the WHERE clause of UPDATE
        feature_id = properties["id"]

        # remove the unnecessary field (we don't update the id)
        del properties["id"]

        for property_ in properties:
            if isinstance(properties[property_], int) or isinstance(properties[property_], float):
                value = str(properties[property_])
            elif isinstance(properties[property_], str):
                value = "'" + str(properties[property_]) + "'"
            elif properties[property_] is None:
                value = "NULL"
            else:
                raise HTTPError(500, "Invalid field of feature (" + property_ + ": " + str(properties[property_]) + ")."
                                + "Please contact the administrator.")

            column_names.append(property_)
            values.append(value)

        srid = self.get_srid_from_table_name(f_table_name)

        # put the GEOM attribute
        column_names.append("geom")
        values.append("ST_SetSRID(ST_GeomFromGeoJSON('" + str(dumps(resource_json["geometry"])) + "'), " + str(srid) + ")")

        ##################################################

        fields_to_update = []
        for column_name, value in zip(column_names, values):
            fields_to_update.append(column_name + " = " + str(value))

        fields_to_update = ", ".join(fields_to_update)

        update_statement = """
            UPDATE {0} SET {1} WHERE id={2};
        """.format(f_table_name, fields_to_update, feature_id)

        return update_statement

    def get_columns_from_table_formatted(self, list_of_column_name_with_type):
        column_names = []

        for column_name_with_type in list_of_column_name_with_type:
            if "geometry" in column_name_with_type["type"]:
                continue  # if it is geom, so ignore
            elif "timestamp" in column_name_with_type["type"]:
                string = "'" + column_name_with_type["column_name"] + "', to_char(" + column_name_with_type["column_name"] + ", 'YYYY-MM-DD HH24:MI:SS')"
            else:
                string = "'" + column_name_with_type["column_name"] + "', " + column_name_with_type["column_name"]

            column_names.append(string)

        column_names = ", ".join(column_names)

        return column_names

    def get_columns_from_table(self, table_name):
        query = """
            SELECT jsonb_agg(json_build_object('column_name', column_name::TEXT, 'type', udt_name::regtype::TEXT)) as row_to_json
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = '{0}';
        """.format(table_name)

        results_of_query = self.execute(query)

        ######################################################################
        # POST-PROCESSING
        ######################################################################

        # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
        if "row_to_json" in results_of_query:
            results_of_query = results_of_query["row_to_json"]

        # if there is not feature
        if results_of_query is None:
            raise HTTPError(404, "Not found the table_name {0}.".format(table_name))

        return results_of_query

    def get_feature(self, f_table_name, feature_id=None):
        # the id have to be a int
        if is_a_invalid_id(feature_id):
            raise HTTPError(400, "Invalid parameter.")

        columns_of_table = self.get_columns_from_table(f_table_name)
        columns_of_table_string = self.get_columns_from_table_formatted(columns_of_table)

        subquery = get_subquery_feature(f_table_name, feature_id, columns_of_table)

        # # CREATE THE QUERY AND EXECUTE IT
        # query_text = """
        #     SELECT jsonb_build_object(
        #         'type', 'FeatureCollection',
        #         'features',   jsonb_agg(jsonb_build_object(
        #             'type',       'Feature',
        #             'geometry',   ST_AsGeoJSON(geom)::json,
        #             'properties', to_jsonb(feature) - 'geom'
        #         ))
        #     ) AS row_to_json
        #     FROM
        #     {0}
        # """.format(subquery)

        query = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'Feature',
                    'geometry',   ST_AsGeoJSON(geom)::json,
                    'properties', json_build_object(
                        {1}
                    )
                ))
            ) AS row_to_json
            FROM
            {0}
        """.format(subquery, columns_of_table_string)

        results_of_query = self.execute(query)

        ######################################################################
        # POST-PROCESSING
        ######################################################################

        # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
        if "row_to_json" in results_of_query:
            results_of_query = results_of_query["row_to_json"]

        # if there is not feature, returns an empty list
        if results_of_query["features"] is None:
            results_of_query["features"] = []

        return results_of_query

    def create_feature(self, resource_json, current_user_id, remove_id_and_version_from_properties=True):
        query = self.get_insert_statement_from_geojson(resource_json,
                                                            remove_id_and_version_from_properties=remove_id_and_version_from_properties)

        return self.execute(query, is_transaction=True)

    def update_feature(self, resource_json, current_user_id):
        ##################################################
        # get the feature before of deleting it
        ##################################################
        f_table_name = resource_json["f_table_name"]
        feature_id = resource_json["properties"]["id"]

        old_feature = {"features": []}

        try:
            old_feature = self.get_feature(f_table_name, feature_id=feature_id)
        except HTTPError as error:
            if error.status_code == 400:
                raise HTTPError(400, "Invalid feature id " + str(feature_id) + ".")

        if not old_feature["features"]:  # if list is empty
            raise HTTPError(404, "Not found feature {0}.".format(feature_id))

        old_feature = old_feature["features"][0]

        # if the version attribute is different from the new and old feature, raise an exception
        if old_feature["properties"]["version"] != resource_json["properties"]["version"]:
            raise HTTPError(409, "Invalid version attribute. (version: {0})".format(resource_json["properties"]["version"]))

        ##################################################
        # create the update statement
        ##################################################
        query = self.get_update_statement_from_geojson(resource_json)

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

        ##################################################
        # add the version_feature_table name in resource json
        # and insert the feature inside the version_feature_table name
        ##################################################
        old_feature["f_table_name"] = "version_" + f_table_name
        self.create_feature(old_feature, current_user_id)

    def delete_feature(self, f_table_name, feature_id, changeset_id, current_user_id):
        if is_a_invalid_id(feature_id) or is_a_invalid_id(changeset_id):
            raise HTTPError(400, "Invalid parameter.")

        ##################################################
        # get the feature before of deleting it
        ##################################################
        feature = self.get_feature(f_table_name, feature_id=feature_id)
        if not feature["features"]:  # if list is empty
            raise HTTPError(404, "Not found feature {0}.".format(feature_id))

        ##################################################
        # try to delete the feature from feature table
        ##################################################
        query = """
            DELETE FROM {0} WHERE id={1};
        """.format(f_table_name, feature_id)

        rows_affected = self.execute(query, is_transaction=True)

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

        ##################################################
        # add the version_feature_table name in resource json and the changeset id
        # and insert the feature inside the version_feature_table name
        ##################################################
        feature = feature["features"][0]

        # add the old version of the feature in the version table
        feature["f_table_name"] = "version_" + f_table_name
        self.create_feature(feature, current_user_id, remove_id_and_version_from_properties=False)

        # add the deleted version of the feature in the version table
        feature["f_table_name"] = "version_" + f_table_name
        feature["properties"]["version"] += 1  # increment 1 to add new version on version table
        feature["properties"]["changeset_id"] = int(changeset_id)
        feature["properties"]["is_removed"] = True
        self.create_feature(feature, current_user_id, remove_id_and_version_from_properties=False)

    ################################################################################
    # METHODS
    ################################################################################

    def get_table_names_that_already_exist_in_db(self):
        query = """
            SELECT jsonb_agg(table_name) AS row_to_json
            FROM information_schema.tables WHERE table_schema = 'public';
        """

        results_of_query = self.execute(query)

        ######################################################################
        # POST-PROCESSING
        ######################################################################

        # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
        if "row_to_json" in results_of_query:
            results_of_query = results_of_query["row_to_json"]

        return results_of_query

    def get_reserved_words_of_postgresql(self):
        query = """
            SELECT jsonb_agg(word) AS row_to_json
            FROM pg_get_keywords();
        """

        results_of_query = self.execute(query)

        ######################################################################
        # POST-PROCESSING
        ######################################################################

        # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
        if "row_to_json" in results_of_query:
            results_of_query = results_of_query["row_to_json"]

        return results_of_query

    def drop_table_by_name(self, table_name):
        query = """
            DROP TABLE IF EXISTS {0};
        """.format(table_name)

        self.execute(query, is_transaction=True)

    def get_table_schema_from_table_in_list(self, table_schema, table_name):
        query = """
            SELECT json_agg(column_name) AS row_to_json
            FROM
            (
                -- (2) get the column names of the table
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema = '{0}' AND table_name = '{1}'
                ORDER BY column_name
            ) subquery;
        """.format(table_schema, table_name)

        results_of_query = self.execute(query)

        ######################################################################
        # POST-PROCESSING
        ######################################################################

        # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
        if "row_to_json" in results_of_query:
            results_of_query = results_of_query["row_to_json"]

        # if there is not feature
        if results_of_query is None:
            raise HTTPError(404, "Not found the table_name {0}.".format(table_name))

        return results_of_query

    ################################################################################
    # ELEMENT
    ################################################################################

    # get elements

    # def get_elements(self, element, **arguments):
    #     if not are_arguments_valid_to_get_elements(**arguments):
    #         raise HTTPError(400, "Invalid parameter.")
    #
    #     return self.get_elements_geojson(element, **arguments)
    #
    # def get_elements_geojson(self, element, element_id=None, user_id=None, layer_id=None,
    #                          changeset_id=None):
    #
    #     subquery_current_element_table = get_subquery_current_element_table(element,
    #                                                                         element_id=element_id,
    #                                                                         user_id=user_id,
    #                                                                         layer_id=layer_id,
    #                                                                         changeset_id=changeset_id)
    #
    #     query_text = """
    #         SELECT jsonb_build_object(
    #             'type',       'FeatureCollection',
    #             'crs',  json_build_object(
    #                 'type',      'name',
    #                 'properties', json_build_object(
    #                     'name', 'EPSG:4326'
    #                 )
    #             ),
    #             'features',   jsonb_agg(jsonb_build_object(
    #                 'type',       'Feature',
    #                 'geometry',   ST_AsGeoJSON(geom)::jsonb,
    #                 'properties', json_build_object(
    #                     'id',               id,
    #                     'visible',          visible,
    #                     'version',          version,
    #                     'fk_changeset_id',  fk_changeset_id
    #                 ),
    #                 'tags',       tags
    #             ))
    #         ) AS row_to_json
    #         FROM
    #         {0}
    #     """.format(subquery_current_element_table)
    #
    #     # query_text = """
    #     #             SELECT jsonb_build_object(
    #     #                 'type',       'FeatureCollection',
    #     #                 'crs',  json_build_object(
    #     #                     'type',      'name',
    #     #                     'properties', json_build_object(
    #     #                         'name', 'EPSG:4326'
    #     #                     )
    #     #                 ),
    #     #                 'features',   jsonb_agg(jsonb_build_object(
    #     #                     'type',       'Feature',
    #     #                     'geometry',   ST_AsGeoJSON(geom)::jsonb,
    #     #                     'properties', json_build_object(
    #     #                         'id',               id,
    #     #                         'visible',          visible,
    #     #                         'version',          version,
    #     #                         'fk_changeset_id',  fk_changeset_id
    #     #                     ),
    #     #                     'tags',       tags.jsontags
    #     #                 ))
    #     #             ) AS row_to_json
    #     #             FROM
    #     #             {1}
    #     #             CROSS JOIN LATERAL (
    #     #                 -- (3) get the tags of some element on JSON format
    #     #                 SELECT json_agg(json_build_object('k', k, 'v', v)) AS jsontags
    #     #                 FROM
    #     #                 (
    #     #                     -- (2) get the tags of some element
    #     #                     SELECT k, v
    #     #                     FROM current_{0}_tag
    #     #                     WHERE fk_current_{0}_id = element.id
    #     #                     ORDER BY k, v ASC
    #     #                 ) subquery
    #     #             ) AS tags
    #     #         """.format(element, subquery_current_element_table)
    #
    #     # do the query in database
    #     self.__PGSQL_CURSOR__.execute(query_text)
    #
    #     # get the result of query
    #     results_of_query = self.__PGSQL_CURSOR__.fetchone()
    #
    #     ######################################################################
    #     # POST-PROCESSING
    #     ######################################################################
    #
    #     # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
    #     if "row_to_json" in results_of_query:
    #         results_of_query = results_of_query["row_to_json"]
    #
    #     # if there is not feature
    #     if results_of_query["features"] is None:
    #         raise HTTPError(404, "Not found any resource.")
    #
    #     return results_of_query

    # add elements

    # def add_element_in_db(self, element, geometry, changeset_id, tags):
    #
    #     # encode the dict in JSON
    #     geometry = json_encode(geometry)
    #
    #     tags = dumps(tags)  # convert python dict to json to save in db
    #
    #     query_text = """
    #         INSERT INTO current_{0} (geom, fk_changeset_id, tags)
    #         VALUES (ST_GeomFromGeoJSON('{1}'), {2}, '{3}')
    #         RETURNING id;
    #     """.format(element, geometry, changeset_id, tags)
    #
    #     # do the query in database
    #     self.__PGSQL_CURSOR__.execute(query_text)
    #
    #     # get the result of query
    #     result = self.__PGSQL_CURSOR__.fetchone()
    #
    #     return result["id"]

    # def add_element_tag_in_db(self, k, v, element, element_id):
    #     query_text = """
    #         INSERT INTO current_{0}_tag (k, v, fk_current_{0}_id)
    #         VALUES ('{1}', '{2}', {3});
    #     """.format(element, k, v, element_id)
    #
    #     # do the query in database
    #     self.__PGSQL_CURSOR__.execute(query_text)

    # def create_element(self, element, feature):
    #     # TODO: before to add, check if the user is valid. If the user that is adding, is really the correct user
    #     # searching if the changeset is its by fk_user_id. If the user is the owner of the changeset
    #
    #     validate_feature_json(feature)
    #
    #     # get the tags
    #     tags = feature["tags"]
    #
    #     # remove the "tags" key from feature (it is not necessary)
    #     del feature["tags"]
    #
    #     # get the id of changeset
    #     changeset_id = feature["properties"]["fk_changeset_id"]
    #
    #     # add the element in db and get the id of it
    #     element_id = self.add_element_in_db(element, feature["geometry"], changeset_id, tags)
    #
    #     return element_id

    # delete elements

    # def delete_element_in_db(self, element, element_id):
    #     if is_a_invalid_id(element_id):
    #         raise HTTPError(400, "Invalid parameter.")
    #
    #     query_text = """
    #         UPDATE current_{0} SET visible = FALSE WHERE id={1};
    #         """.format(element, element_id)
    #
    #     # do the query in database
    #     self.__PGSQL_CURSOR__.execute(query_text)
    #
    #     rows_affected = self.__PGSQL_CURSOR__.rowcount
    #
    #     if rows_affected == 0:
    #         raise HTTPError(404, "Not found any resource.")
