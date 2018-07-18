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
from copy import deepcopy

from tornado.web import HTTPError

from psycopg2 import connect, DatabaseError, ProgrammingError
from psycopg2.extras import RealDictCursor

from modules.design_pattern import Singleton

from settings.db_settings import __PGSQL_CONNECTION_SETTINGS__, __DEBUG_PGSQL_CONNECTION_SETTINGS__, \
                                    __GEOSERVER_CONNECTION_SETTINGS__, __DEBUG_GEOSERVER_CONNECTION_SETTINGS__, \
                                    __GEOSERVER_REST_CONNECTION_SETTINGS__

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


def format_the_table_name_to_standard(table_name, user_id):
    # the table name follow the standard: _<user_id>_<table_name>
    return "_" + str(user_id) + "_" + table_name


def remove_unnecessary_properties(properties):
    if "id" in properties:
        del properties["id"]

    if "geom" in properties:
        del properties["geom"]

    if "version" in properties:
        del properties["version"]

    if "changeset_id" in properties:
        del properties["changeset_id"]

    return properties


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
            self.__DO_CONNECTION__(__DEBUG_PGSQL_CONNECTION_SETTINGS__)
            self.__DB_CONNECTION__ = __DEBUG_PGSQL_CONNECTION_SETTINGS__
            self.__GEOSERVER_CONNECTION__ = __DEBUG_GEOSERVER_CONNECTION_SETTINGS__
        else:
            self.__DO_CONNECTION__(__PGSQL_CONNECTION_SETTINGS__)
            self.__DB_CONNECTION__ = __PGSQL_CONNECTION_SETTINGS__
            self.__GEOSERVER_CONNECTION__ = __GEOSERVER_CONNECTION_SETTINGS__

        self.__GEOSERVER_REST_CONNECTION_SETTINGS__ = __GEOSERVER_REST_CONNECTION_SETTINGS__

        # cursor_factory=RealDictCursor means that the "row" of the table will be
        # represented by a dictionary in python
        self.__PGSQL_CURSOR__ = self.__PGSQL_CONNECTION__.cursor(cursor_factory=RealDictCursor)

        # create a browser simulator to connect with geoserver
        self.__SESSION__ = Session()
        self.__URL_GEOSERVER_REST__ = "http://{0}:{1}".format(self.__GEOSERVER_REST_CONNECTION_SETTINGS__["HOSTNAME"],
                                                              self.__GEOSERVER_REST_CONNECTION_SETTINGS__["PORT"])

    def __DO_CONNECTION__(self, __connection_settings__):
        """
        Do the DB connection with the '__pgsql_connection_settings__'
        :param __connection_settings__: the connection settings of PostgreSQL.
        It can be for the normal DB or test DB
        :return:
        """
        if self.DEBUG_MODE:
            print("\nConnecting in PostgreSQL with:"
                  "\n- hostname: ", __connection_settings__["HOSTNAME"],
                  "\n- port: ", __connection_settings__["PORT"],
                  "\n- database: ", __connection_settings__["DATABASE"], "\n")

        try:
            self.__PGSQL_CONNECTION__ = connect(host=__connection_settings__["HOSTNAME"],
                                                port=__connection_settings__["PORT"],
                                                user=__connection_settings__["USERNAME"],
                                                password=__connection_settings__["PASSWORD"],
                                                dbname=__connection_settings__["DATABASE"])
            print("PostgreSQL's connection was successful!")
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

        print("\nClosed the PostgreSQL's connection!\n")

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

    def execute(self, query_text, modify_information=False):

        try:
            # do the query in database
            self.__PGSQL_CURSOR__.execute(query_text)
        except ProgrammingError as error:
            print("Error when executing the query text")
            print("Error: ", error, "\n")
            raise ProgrammingError(error)

        try:
            # get the result of query
            results_of_query = self.__PGSQL_CURSOR__.fetchall()
        except ProgrammingError:
            return None

        # if modify some information, so do commit
        if modify_information:
            # commit the modifications
            self.commit()

        return results_of_query

    ################################################################################
    # GEOSERVER
    ################################################################################

    @run_if_can_publish_layers_in_geoserver
    def get_layers_from_geoserver(self):
        response = self.__SESSION__.get(self.__URL_GEOSERVER_REST__ + '/layers/{0}/{1}'.format(self.__GEOSERVER_CONNECTION__["WORKSPACE"],
                                                                                               self.__GEOSERVER_CONNECTION__["DATASTORE"]))

        if response.status_code == 404:
            raise HTTPError(404, str(response))
        elif response.status_code == 500:
            raise HTTPError(500, str(response))

    @run_if_can_publish_layers_in_geoserver
    def publish_feature_table_in_geoserver(self, f_table_name):
        request_body = {
            "workspace": self.__GEOSERVER_CONNECTION__["WORKSPACE"],
            "datastore": self.__GEOSERVER_CONNECTION__["DATASTORE"],
            "layer": f_table_name,
            "description": "Description",
            "projection": "EPSG: 4326"
        }

        response = self.__SESSION__.post(self.__URL_GEOSERVER_REST__ + '/layer/publish', data=request_body)

        if response.status_code == 404:
            raise HTTPError(404, str(response.text))
        elif response.status_code == 500:
            raise HTTPError(500, str(response.text))

    @run_if_can_publish_layers_in_geoserver
    def unpublish_feature_table_in_geoserver(self, f_table_name):
        response = self.__SESSION__.delete(self.__URL_GEOSERVER_REST__ + '/layer/remove/{0}/{1}/{2}'.format(self.__GEOSERVER_CONNECTION__["WORKSPACE"],
                                                                                                            self.__GEOSERVER_CONNECTION__["DATASTORE"],
                                                                                                            f_table_name))

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
        query_text = """
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
                        'receive_notification_by_email',   receive_notification_by_email 
                    )
                ))
            ) AS row_to_json
            FROM 
            {0}
        """.format(subquery)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        results_of_query = self.__PGSQL_CURSOR__.fetchone()

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

    def create_user(self, resource_json, verified_social_login_email=False):
        p = resource_json["properties"]

        if verified_social_login_email:
            p["is_email_valid"] = True
        else:
            p["is_email_valid"] = False

        query_text = """
            INSERT INTO pauliceia_user (email, username, name, password, created_at, terms_agreed, 
                                        receive_notification_by_email, is_email_valid) 
            VALUES ('{0}', '{1}', '{2}', '{3}', LOCALTIMESTAMP, {4}, {5}, {6})
            RETURNING user_id;
        """.format(p["email"], p["username"], p["name"], p["password"], p["terms_agreed"],
                   p["receive_notification_by_email"], p["is_email_valid"])

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        result = self.__PGSQL_CURSOR__.fetchone()

        return result

    def update_user_email_is_valid(self, user_id, is_email_valid=True):
        query_text = """
            UPDATE pauliceia_user SET is_email_valid = {1} 
            WHERE user_id = {0};
        """.format(user_id, is_email_valid)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    def update_user(self, resource_json, user_id):
        p = resource_json["properties"]

        query_text = """
            UPDATE pauliceia_user SET email = '{1}', username = '{2}', name = '{3}',
                                        terms_agreed = {4}, receive_notification_by_email = {5} 
            WHERE user_id = {0};
        """.format(p["user_id"], p["email"], p["username"], p["name"],
                   p["terms_agreed"], p["receive_notification_by_email"])

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    def delete_user(self, feature_id):
        if is_a_invalid_id(feature_id):
            raise HTTPError(400, "Invalid parameter.")

        query_text = """
            DELETE FROM pauliceia_user WHERE user_id={0};
        """.format(feature_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

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
        query_text = """
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

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        results_of_query = self.__PGSQL_CURSOR__.fetchone()

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

    def create_curator(self, resource_json, user_id):
        p = resource_json["properties"]

        query_text = """
                    INSERT INTO curator (user_id, keyword_id, region, created_at)
                    VALUES ({0}, {1}, LOWER('{2}'), LOCALTIMESTAMP);
                """.format(p["user_id"], p["keyword_id"], p["region"])

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

    def update_curator(self, resource_json, user_id):
        p = resource_json["properties"]

        query_text = """
            UPDATE curator SET region = LOWER('{2}')
            WHERE user_id = {0} AND keyword_id = {1};
        """.format(p["user_id"], p["keyword_id"], p["region"])

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    def delete_curator(self, user_id=None, keyword_id=None):
        if is_a_invalid_id(user_id) or is_a_invalid_id(keyword_id):
            raise HTTPError(400, "Invalid parameter.")

        # delete the curator
        if user_id is None:
            query_text = """
                DELETE FROM curator WHERE keyword_id = {0};
            """.format(keyword_id)
        elif keyword_id is None:
            query_text = """
                DELETE FROM curator WHERE user_id = {0};
            """.format(user_id)
        else:
            query_text = """
                DELETE FROM curator WHERE user_id = {0} AND keyword_id = {1};
            """.format(user_id, keyword_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

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
        query_text = """
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

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        results_of_query = self.__PGSQL_CURSOR__.fetchone()

        ######################################################################
        # POST-PROCESSING
        ######################################################################

        # if key "row_to_json" in results_of_query, remove it, putting the result inside the variable
        if "row_to_json" in results_of_query:
            results_of_query = results_of_query["row_to_json"]

        # if there is not feature
        if results_of_query["features"] is None:
            raise HTTPError(404, "Not found any resource.")

        # POST PROCESSING

        # iterate in features to change the original table name (_<user_id>_<table_name>) by just table_name
        # for feature in results_of_query["features"]:
        #     table_name = feature["properties"]["table_name"]
        #
        #     # get just the table name, without the user id
        #     second_underscore = table_name.find("_", 2)
        #     table_name_without_user_id = table_name[second_underscore+1:]
        #
        #     feature["properties"]["table_name"] = table_name_without_user_id

        return results_of_query

    def add_layer_in_db(self, properties):
        p = properties

        query_text = """
            INSERT INTO layer (f_table_name, name, description, source_description, created_at) 
            VALUES ('{0}', '{1}', '{2}', '{3}', LOCALTIMESTAMP) RETURNING layer_id;
        """.format(p["f_table_name"], p["name"], p["description"], p["source_description"])

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        result = self.__PGSQL_CURSOR__.fetchone()

        return result

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
        self.create_user_layer(user_layer_json)

        return id_in_json

    def update_table_name(self, old_table_name, new_table_name):
        query_text = """
            ALTER TABLE IF EXISTS {0}
            RENAME TO {1};
        """.format(old_table_name, new_table_name)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

    def update_layer_in_db(self, properties):
        p = properties

        query_text = """
                    UPDATE layer SET f_table_name = '{1}', name = '{2}', description = '{3}', source_description = '{4}'
                    WHERE layer_id = {0};
                """.format(p["layer_id"], p["f_table_name"], p["name"], p["description"], p["source_description"])

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

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

        # get the old layer properties
        old_layer_properties = self.get_layers(layer_id=new_layer_properties["layer_id"])["features"][0]["properties"]

        ##################################################
        # update the layer in db
        ##################################################
        self.update_layer_in_db(new_layer_properties)

        ##################################################
        # remove the references and keywords from layer
        ##################################################
        self.delete_layer_reference(layer_id=new_layer_properties["layer_id"])
        self.delete_layer_keyword(layer_id=new_layer_properties["layer_id"])

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
        if old_layer_properties["f_table_name"] != new_layer_properties["f_table_name"]:
            # update the feature table
            self.update_table_name(old_layer_properties["f_table_name"], new_layer_properties["f_table_name"])
            # update the version feature table
            self.update_table_name("version_" + old_layer_properties["f_table_name"], "version_" + new_layer_properties["f_table_name"])
            # update the temporal columns
            self.update_temporal_columns_f_table_name(old_layer_properties["f_table_name"], new_layer_properties["f_table_name"])

    def delete_layer_dependencies(self, layer_id):
        # get the layer information before to remove the layer
        layer = self.get_layers(layer_id=layer_id)
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
            self.PGSQLConn.rollback()  # do a rollback to comeback in a safe state of DB
            raise HTTPError(500, str(error))

    def delete_layer(self, layer_id):
        if is_a_invalid_id(layer_id):
            raise HTTPError(400, "Invalid parameter.")

        # delete layer dependencies
        self.delete_layer_dependencies(layer_id)

        # delete the layer
        query_text = """
            DELETE FROM layer WHERE layer_id={0};
        """.format(layer_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    ################################################################################
    # FEATURE TABLE
    ################################################################################

    def get_feature_table(self, f_table_name=None):
        subquery = get_subquery_feature_table(f_table_name=f_table_name)

        # CREATE THE QUERY AND EXECUTE IT
        query_text = """
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

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        results_of_query = self.__PGSQL_CURSOR__.fetchone()

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

    def create_feature_table(self,  resource_json, user_id):
        f_table_name = resource_json["f_table_name"]
        geometry_type = resource_json["geometry"]["type"]
        EPSG = resource_json["geometry"]["crs"]["properties"]["name"].split(":")[1]
        properties = resource_json["properties"]

        properties = remove_unnecessary_properties(properties)

        # get the attributes of the feature table
        properties_string = ""
        for property in properties:
            properties_string += property + " " + properties[property] + ", \n"

        tables_to_create = [f_table_name, "version_{0}".format(f_table_name)]

        for table_to_create in tables_to_create:
            # create the feature table
            query_text = """        
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

            self.__PGSQL_CURSOR__.execute(query_text)

        # put the feature tables in database
        self.commit()
        # publish the features tables/layers in geoserver
        self.publish_feature_table_in_geoserver(f_table_name)

    def update_feature_table(self,  resource_json, user_id):
        f_table_name = resource_json["f_table_name"]
        geometry_type = resource_json["geometry"]["type"]
        EPSG = resource_json["geometry"]["crs"]["properties"]["name"].split(":")[1]
        properties = resource_json["properties"]

        properties = remove_unnecessary_properties(properties)

        # get the attributes of the feature table
        properties_string = ""
        for property in properties:
            properties_string += property + " " + properties[property] + ", \n"

        tables_to_create = [f_table_name, "version_{0}".format(f_table_name)]

        for table_to_create in tables_to_create:
            # create the feature table
            query_text = """        
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

            self.__PGSQL_CURSOR__.execute(query_text)

        # put the feature tables in database
        self.commit()
        # publish the features tables/layers in geoserver
        self.publish_feature_table_in_geoserver(f_table_name)

    def delete_feature_table(self, f_table_name):
        tables_to_drop = [f_table_name, "version_{0}".format(f_table_name)]

        for table_to_drop in tables_to_drop:
            # delete the feature table
            query_text = """        
                DROP TABLE IF EXISTS {0} CASCADE ;
            """.format(table_to_drop)

            self.__PGSQL_CURSOR__.execute(query_text)

        # unpublish the features table in geoserver
        self.unpublish_feature_table_in_geoserver(f_table_name)
        # remove the feature table from database
        self.commit()

    ################################################################################
    # FEATURE TABLE COLUMN
    ################################################################################

    def create_feature_table_column(self, resource_json):

        query_text = """
            ALTER TABLE {0} 
            ADD COLUMN {1} {2};   
        """.format(resource_json["f_table_name"], resource_json["column_name"], resource_json["column_type"])

        self.__PGSQL_CURSOR__.execute(query_text)

    def delete_feature_table_column(self, f_table_name, column_name):

        query_text = """
            ALTER TABLE {0} 
            DROP COLUMN {1} CASCADE;   
        """.format(f_table_name, column_name)

        self.__PGSQL_CURSOR__.execute(query_text)

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
        query_text = """
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

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        results_of_query = self.__PGSQL_CURSOR__.fetchone()

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

    def create_temporal_columns(self, resource_json, user_id):
        p = resource_json["properties"]

        query_text = """
            INSERT INTO temporal_columns (f_table_name, start_date_column_name, end_date_column_name, start_date, end_date,
                                          start_date_mask_id, end_date_mask_id)
            VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', {5}, {6});
        """.format(p["f_table_name"], p["start_date_column_name"], p["end_date_column_name"], p["start_date"], p["end_date"],
                   p["start_date_mask_id"], p["end_date_mask_id"])

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

    def update_temporal_columns_f_table_name(self, old_f_table_name, new_f_table_name):
        query_text = """
            UPDATE temporal_columns SET f_table_name='{1}'                                
            WHERE f_table_name = '{0}';
        """.format(old_f_table_name, new_f_table_name)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

    def update_temporal_columns(self, resource_json, user_id):
        p = resource_json["properties"]

        query_text = """
            UPDATE temporal_columns SET start_date_column_name='{1}', end_date_column_name='{2}', start_date='{3}', end_date='{4}',
                                        start_date_mask_id={5}, end_date_mask_id={6}                                    
            WHERE f_table_name = '{0}';
        """.format(p["f_table_name"], p["start_date_column_name"], p["end_date_column_name"], p["start_date"], p["end_date"],
                   p["start_date_mask_id"], p["end_date_mask_id"])

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    def delete_temporal_columns(self, f_table_name):
        # if is_a_invalid_id(user_id) or is_a_invalid_id(keyword_id):
        #     raise HTTPError(400, "Invalid parameter.")

        # delete the temporal_columns
        query_text = """
            DELETE FROM temporal_columns WHERE f_table_name = '{0}';
        """.format(f_table_name)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

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
        query_text = """
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

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        results_of_query = self.__PGSQL_CURSOR__.fetchone()

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

    def create_user_layer(self, resource_json):
        p = resource_json["properties"]

        query_text = """
                    INSERT INTO user_layer (layer_id, user_id, created_at, is_the_creator) 
                    VALUES ({0}, {1}, LOCALTIMESTAMP, {2});
                """.format(p["layer_id"], p["user_id"], p["is_the_creator"])

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

    def delete_user_layer(self, user_id=None, layer_id=None):
        if is_a_invalid_id(user_id) or is_a_invalid_id(layer_id):
            raise HTTPError(400, "Invalid parameter.")

        if user_id is None:
            query_text = """
                DELETE FROM user_layer WHERE layer_id={0};
            """.format(layer_id)
        elif layer_id is None:
            query_text = """
                DELETE FROM user_layer WHERE user_id={0};
            """.format(user_id)
        else:
            query_text = """
                DELETE FROM user_layer WHERE user_id={0} AND layer_id={1};
            """.format(user_id, layer_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

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
        query_text = """
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

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        results_of_query = self.__PGSQL_CURSOR__.fetchone()

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

    def create_reference(self, resource_json, user_id):
        # put the current user id as the creator of the reference
        resource_json["properties"]["user_id"] = user_id

        p = resource_json["properties"]

        query_text = """
            INSERT INTO reference (description, user_id_creator)
            VALUES ('{0}', {1}) RETURNING reference_id;
        """.format(p["description"], p["user_id"])

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        result = self.__PGSQL_CURSOR__.fetchone()

        return result

    def update_reference(self, resource_json, user_id):
        p = resource_json["properties"]

        query_text = """
            UPDATE reference SET description = '{1}'
            WHERE reference_id={0};
        """.format(p["reference_id"], p["description"])

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    def delete_reference(self, resource_id):
        if is_a_invalid_id(resource_id):
            raise HTTPError(400, "Invalid parameter.")

        # delete the reference
        query_text = """
            DELETE FROM reference WHERE reference_id={0};
        """.format(resource_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    ################################################################################
    # LAYER REFERENCE
    ################################################################################

    # def get_layer_references(self, layer_id=None, user_id=None, is_the_creator=None):
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

    def create_layer_reference(self, resource_json):
        p = resource_json["properties"]

        query_text = """
            INSERT INTO layer_reference (layer_id, reference_id) 
            VALUES ({0}, {1});
        """.format(p["layer_id"], p["reference_id"])

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

    def delete_layer_reference(self, layer_id=None, reference_id=None):
        if is_a_invalid_id(layer_id) or is_a_invalid_id(reference_id):
            raise HTTPError(400, "Invalid parameter.")

        if reference_id is None:
            query_text = """
                DELETE FROM layer_reference WHERE layer_id={0};
            """.format(layer_id)
        else:
            query_text = """
                DELETE FROM layer_reference WHERE layer_id={0} AND reference_id={1};
            """.format(layer_id, reference_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    ################################################################################
    # KEYWORD
    ################################################################################

    def get_keywords(self, keyword_id=None, name=None, parent_id=None, user_id_creator=None):

        # the id have to be a int
        if is_a_invalid_id(keyword_id) or is_a_invalid_id(parent_id) or is_a_invalid_id(user_id_creator):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_keyword_table(keyword_id=keyword_id, name=name,
                                              parent_id=parent_id, user_id_creator=user_id_creator)

        # CREATE THE QUERY AND EXECUTE IT
        query_text = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'Keyword',
                    'properties', json_build_object(
                        'keyword_id',      keyword_id,
                        'name',            name,
                        'parent_id',       parent_id,
                        'user_id_creator', user_id_creator,
                        'created_at',      to_char(created_at, 'YYYY-MM-DD HH24:MI:SS')
                    )
                ))
            ) AS row_to_json
            FROM 
            {0}            
        """.format(subquery)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        results_of_query = self.__PGSQL_CURSOR__.fetchone()

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

    def create_keyword(self, resource_json, user_id):
        # put the current user id as the creator of the keyword
        resource_json["properties"]["user_id_creator"] = user_id

        p = resource_json["properties"]

        if p["parent_id"] is None:
            p["parent_id"] = "NULL"

        query_text = """
            INSERT INTO keyword (name, parent_id, user_id_creator, created_at)
            VALUES ('{0}', {1}, {2}, LOCALTIMESTAMP) RETURNING keyword_id;
        """.format(p["name"], p["parent_id"], p["user_id_creator"])

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        result = self.__PGSQL_CURSOR__.fetchone()

        return result

    def update_keyword(self, resource_json, user_id):
        p = resource_json["properties"]

        if p["parent_id"] is None:
            p["parent_id"] = "NULL"

        query_text = """
            UPDATE keyword SET name = '{1}', parent_id = {2}
            WHERE keyword_id={0};
        """.format(p["keyword_id"], p["name"], p["parent_id"])

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    def delete_keyword(self, resource_id):
        if is_a_invalid_id(resource_id):
            raise HTTPError(400, "Invalid parameter.")

        # delete the reference
        query_text = """
            DELETE FROM keyword WHERE keyword_id={0};
        """.format(resource_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

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

        query_text = """
            INSERT INTO layer_keyword (layer_id, keyword_id) 
            VALUES ({0}, {1});
        """.format(p["layer_id"], p["keyword_id"])

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

    def delete_layer_keyword(self, layer_id=None, keyword_id=None):
        if is_a_invalid_id(layer_id) or is_a_invalid_id(keyword_id):
            raise HTTPError(400, "Invalid parameter.")

        if keyword_id is None:
            query_text = """
                DELETE FROM layer_keyword WHERE layer_id={0};
            """.format(layer_id)
        else:
            query_text = """
                DELETE FROM layer_keyword WHERE layer_id={0} AND keyword_id={1};
            """.format(layer_id, keyword_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

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
        query_text = """
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

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        results_of_query = self.__PGSQL_CURSOR__.fetchone()

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

    def create_changeset(self, resource_json, user_id):
        # put the current user id as the creator of the keyword
        resource_json["properties"]["user_id_creator"] = user_id

        p = resource_json["properties"]

        query_text = """
            INSERT INTO changeset (description, created_at, layer_id, user_id_creator)
            VALUES ('{0}', LOCALTIMESTAMP, {1}, {2}) RETURNING changeset_id;
        """.format(p["description"], p["layer_id"], p["user_id_creator"])

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        result = self.__PGSQL_CURSOR__.fetchone()

        return result

    def close_changeset(self, current_user_id, changeset_id):
        if is_a_invalid_id(changeset_id):
            raise HTTPError(400, "Invalid parameter.")

        # verify if the changeset is closed or not, if it is closed, raise 409 exception
        list_changesets = self.get_changesets(changeset_id=changeset_id)
        closed_at = list_changesets['features'][0]['properties']['closed_at']
        if closed_at is not None:
            raise HTTPError(409,
                            "Changeset with ID {0} has already been closed at {1}.".format(changeset_id, closed_at))

        # verify if the user created the changeset
        user_id_creator = list_changesets['features'][0]['properties']['user_id_creator']
        if user_id_creator != current_user_id:
            raise HTTPError(409,
                            "The user {0} didn't create the changeset {1}.".format(current_user_id, changeset_id))

        query_text = """
            UPDATE changeset SET closed_at=LOCALTIMESTAMP WHERE changeset_id={0};
        """.format(changeset_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    def delete_changeset(self, changeset_id=None, layer_id=None):
        if is_a_invalid_id(changeset_id) or is_a_invalid_id(layer_id):
            raise HTTPError(400, "Invalid parameter.")

        if changeset_id is not None:
            # delete the reference
            query_text = """
                DELETE FROM changeset WHERE changeset_id={0};
            """.format(changeset_id)
        elif layer_id is not None:
            # delete the reference
            query_text = """
                DELETE FROM changeset WHERE layer_id={0};
            """.format(layer_id)
        else:
            raise HTTPError(400, "Invalid parameter.")

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

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
        query_text = """
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

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        results_of_query = self.__PGSQL_CURSOR__.fetchone()

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

        query_text = """
            INSERT INTO notification (description, created_at, is_denunciation, user_id_creator, 
                                      layer_id, keyword_id, notification_id_parent)
            VALUES ('{0}', LOCALTIMESTAMP, {1}, {2}, {3}, {4}, {5}) RETURNING notification_id;
        """.format(p["description"], p["is_denunciation"], p["user_id_creator"], p["layer_id"],
                   p["keyword_id"], p["notification_id_parent"])

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        result = self.__PGSQL_CURSOR__.fetchone()

        return result

    def update_notification(self, resource_json, user_id):
        p = resource_json["properties"]

        if p["layer_id"] is None:
            p["layer_id"] = "NULL"

        if p["keyword_id"] is None:
            p["keyword_id"] = "NULL"

        if p["notification_id_parent"] is None:
            p["notification_id_parent"] = "NULL"

        query_text = """
            UPDATE notification SET description = '{1}', layer_id = {2}, keyword_id = {3}, notification_id_parent = {4}
            WHERE notification_id={0};
        """.format(p["notification_id"], p["description"], p["layer_id"], p["keyword_id"], p["notification_id_parent"])

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    def delete_notification(self, notification_id):
        if is_a_invalid_id(notification_id):
            raise HTTPError(400, "Invalid parameter.")

        # delete the reference
        query_text = """
            DELETE FROM notification WHERE notification_id={0};
        """.format(notification_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        if rows_affected == 0:
            raise HTTPError(404, "Not found any resource.")

    ################################################################################
    # IMPORT
    ################################################################################

    def create_new_table_with_the_schema_of_old_table(self, new_table_name, old_table_name):
        query_text = """
            CREATE TABLE {0} ( like {1} including all )
        """.format(new_table_name, old_table_name)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

    def add_version_column_in_table(self, table_name):
        query_text = """
            ALTER TABLE {0} 
            ADD COLUMN version INT NOT NULL DEFAULT 1
        """.format(table_name)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

    def add_changeset_id_column_in_table(self, table_name):
        # create the column
        query_text = """
            ALTER TABLE {0} ADD COLUMN changeset_id INT
        """.format(table_name)

        # put the column as FK
        self.__PGSQL_CURSOR__.execute(query_text)

        query_text = """
            ALTER TABLE {0}
            ADD CONSTRAINT constraint_changeset_id
            FOREIGN KEY (changeset_id)
                REFERENCES changeset (changeset_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE
        """.format(table_name)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

    def update_feature_table_setting_in_all_records_a_version(self, f_table_name, version):
        # create the column
        query_text = """
            UPDATE {0} SET version = {1};
        """.format(f_table_name, version)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

    def update_feature_table_setting_in_all_records_a_changeset_id(self, f_table_name, changeset_id):
        # create the column
        query_text = """
            UPDATE {0} SET changeset_id = {1};
        """.format(f_table_name, changeset_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

    ################################################################################
    # MASK
    ################################################################################

    def get_mask(self, mask_id=None):
        # the id have to be a int
        if is_a_invalid_id(mask_id):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_mask_table(mask_id=mask_id)

        # CREATE THE QUERY AND EXECUTE IT
        query_text = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'Mask',
                    'properties',  json_build_object(
                        'mask_id',          mask_id,
                        'mask',             mask,
                        'user_id_creator',  user_id_creator
                    )
                ))
            ) AS row_to_json
            FROM 
            {0}            
        """.format(subquery)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        results_of_query = self.__PGSQL_CURSOR__.fetchone()

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
    #     # TODO: before to add, verify if the user is valid. If the user that is adding, is really the correct user
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
