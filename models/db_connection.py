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

    __LIST_TABLES_INFORMATION__ = [
        {"table_name": "TABLE_NAME"},
        {"table_name": "TABLE_NAME"},
        ...
    ]

    This __PGSQL_CONNECTION_SETTINGS__ dictionary is the connection with PostgreSQL
    The __LIST_TABLES_INFORMATION__ is a list with all tables` name
"""

from abc import ABCMeta
from requests import exceptions, Session
from json import loads, dumps

from tornado.web import HTTPError
from tornado.escape import json_encode

from psycopg2 import connect, DatabaseError, IntegrityError
from psycopg2._psycopg import ProgrammingError
from psycopg2.extras import RealDictCursor

from modules.common import get_username_and_password_as_string_in_base64
from modules.design_pattern import Singleton

from settings.db_settings import __PGSQL_CONNECTION_SETTINGS__, __DEBUG_PGSQL_CONNECTION_SETTINGS__, \
                                __NEO4J_CONNECTION_SETTINGS__, __DEBUG_NEO4J_CONNECTION_SETTINGS__

from .util import *


def if_neo4j_is_not_running_so_put_db_offline_and_raise_500_error_status(method):

    def wrapper(self, *args, **kwargs):

        try:
            result = method(self, *args, **kwargs)
        except exceptions.ConnectionError:
            # put DB status on offline
            self.set_connection_status(status=False)

            raise HTTPError(500, "Neo4J is not running.")

        return result

    return wrapper


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

    def __init__(self, args={}):
        self.__ARGS__ = args

        if self.__ARGS__["DEBUG_MODE"]:
            self.__DO_CONNECTION__(__DEBUG_PGSQL_CONNECTION_SETTINGS__)
        else:
            self.__DO_CONNECTION__(__PGSQL_CONNECTION_SETTINGS__)

        # cursor_factory=RealDictCursor means that the "row" of the table will be
        # represented by a dictionary in python
        self.__PGSQL_CURSOR__ = self.__PGSQL_CONNECTION__.cursor(cursor_factory=RealDictCursor)

    def __DO_CONNECTION__(self, __connection_settings__):
        """
        Do the DB connection with the '__pgsql_connection_settings__'
        :param __connection_settings__: the connection settings of PostgreSQL.
        It can be for the normal DB or test DB
        :return:
        """
        if self.__ARGS__["DEBUG_MODE"]:
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

        print("Closed the PostgreSQL's connection!\n")

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
    # user group
    ################################################################################

    def get_user_group(self, group_id=None, user_id=None):
        # the id have to be a int
        if is_a_invalid_id(group_id) or is_a_invalid_id(user_id):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_user_group_table(group_id=group_id, user_id=user_id)

        # CREATE THE QUERY AND EXECUTE IT
        query_text = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'UserGroup',
                    'properties', json_build_object(
                        'fk_group_id',              fk_group_id,
                        'fk_user_id',               fk_user_id,
                        'added_at',                 to_char(added_at, 'YYYY-MM-DD HH24:MI:SS'),                    
                        'group_permission',         group_permission,
                        'group_status',             group_status,
                        'can_receive_notification', can_receive_notification,
                        'fk_user_id_added_by',      fk_user_id_added_by                        
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
            raise HTTPError(404, "Not found any feature.")

        return results_of_query

    def add_user_group_in_db(self, properties):
        p = properties

        # change can_receive_notification boolean to string to can add in DB
        p['can_receive_notification'] = "TRUE" if p['can_receive_notification'] else "FALSE"

        query_text = """
            INSERT INTO user_group (fk_group_id, fk_user_id, added_at, 
                   can_receive_notification, fk_user_id_added_by) 
            VALUES ({0}, {1}, LOCALTIMESTAMP, 
                   {2}, {3})
        """.format(p['fk_group_id'], p['fk_user_id'],
                   p['can_receive_notification'], p['fk_user_id_added_by'])

        try:
            # do the query in database
            self.__PGSQL_CURSOR__.execute(query_text)
        except IntegrityError as error:
            # how the error is of PostgreSQL, so it is necessary do a rollback
            # to be in a safe state
            self.rollback()

            # 23505 - unique_violation
            if error.pgcode == "23505":
                raise HTTPError(400, "The user_id is already added in group_id")

            raise HTTPError(500, "Undefined Integrity Error. Please, contact the administrator.")

        # return nothing, because is not generated a new ID when put a user in a group

        # get the result of query
        # result = self.__PGSQL_CURSOR__.fetchone()
        #
        # return result

    # def add_user_group_tag_in_db(self, k, v, feature_id):
    #     query_text = """
    #         INSERT INTO group_tag (k, v, fk_group_id)
    #         VALUES ('{0}', '{1}', {2});
    #     """.format(k, v, feature_id)
    #
    #     # do the query in database
    #     self.__PGSQL_CURSOR__.execute(query_text)

    def create_user_group(self, feature_json, user_id):

        properties = feature_json["properties"]

        # add the user in a group
        self.add_user_group_in_db(properties)

        # put in DB the feature
        self.commit()

    def delete_user_group(self, group_id=None, user_id=None):
        if (is_a_invalid_id(group_id) or is_a_invalid_id(user_id)) or \
                (group_id is None or user_id is None):
            raise HTTPError(400, "Invalid parameter.")

        query_text = """
            DELETE FROM user_group 
            WHERE fk_user_id = {0} AND fk_group_id = {1};
        """.format(user_id, group_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        self.commit()

        if rows_affected == 0:
            raise HTTPError(404, "Not found any feature.")


    ################################################################################
    # group
    ################################################################################

    def get_group(self, group_id=None, user_id=None, group_status=None):
        # the id have to be a int
        if is_a_invalid_id(group_id) or is_a_invalid_id(user_id):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_group_table(group_id=group_id, user_id=user_id,
                                            group_status=group_status)

        # CREATE THE QUERY AND EXECUTE IT
        query_text = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'Group',
                    'properties', json_build_object(
                        'id',           id,                        
                        'created_at',   to_char(created_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'removed_at',   to_char(removed_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'visible',      visible,
                        'fk_user_id',   fk_user_id
                    ),
                    'tags',       tags.jsontags
                ))
            ) AS row_to_json
            FROM 
            {0}
            CROSS JOIN LATERAL (
                -- (3) get the tags of some feature on JSON format   
                SELECT json_agg(json_build_object('k', k, 'v', v)) AS jsontags 
                FROM 
                (
                    -- (2) get the tags of some feature
                    SELECT k, v
                    FROM group_tag 
                    WHERE fk_group_id = group_.id
                    ORDER BY k, v ASC
                ) subquery      
            ) AS tags
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
            raise HTTPError(404, "Not found any feature.")

        return results_of_query

    def add_group_in_db(self, user_id):
        query_text = """
            INSERT INTO group_ (created_at, fk_user_id)
            VALUES (LOCALTIMESTAMP, {0}) RETURNING id;
        """.format(user_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        result = self.__PGSQL_CURSOR__.fetchone()

        return result

    def add_group_tag_in_db(self, k, v, feature_id):
        query_text = """
            INSERT INTO group_tag (k, v, fk_group_id)
            VALUES ('{0}', '{1}', {2});
        """.format(k, v, feature_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

    def create_group(self, feature_json, user_id):

        # group_id = feature_json["properties"]["fk_group_id"]

        # add the layer in db and get the id of it
        id_in_json = self.add_group_in_db(user_id)

        # add in DB the tags of layer
        for tag in feature_json["tags"]:
            # add the layer tag in db
            self.add_group_tag_in_db(tag["k"], tag["v"], id_in_json["id"])

        # put in DB the layer and its tags
        self.commit()

        return id_in_json

    def delete_group_in_db(self, feature_id):
        if is_a_invalid_id(feature_id):
            raise HTTPError(400, "Invalid parameter.")

        query_text = """
            UPDATE group_ SET visible = FALSE, removed_at = LOCALTIMESTAMP
            WHERE id={0};
        """.format(feature_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        self.commit()

        if rows_affected == 0:
            raise HTTPError(404, "Not found any feature.")

    ################################################################################
    # project
    ################################################################################

    def get_projects(self, project_id=None, group_id=None, user_id=None):
        # the id have to be a int
        if is_a_invalid_id(project_id) or is_a_invalid_id(group_id) or is_a_invalid_id(user_id):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_project_table(project_id=project_id, group_id=group_id, user_id=user_id)

        # CREATE THE QUERY AND EXECUTE IT
        query_text = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'Project',
                    'properties', json_build_object(
                        'id',           id,                        
                        'created_at',   to_char(created_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'removed_at',   to_char(removed_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'fk_group_id', fk_group_id,
                        'fk_user_id', fk_user_id
                    ),
                    'tags',       tags.jsontags
                ))
            ) AS row_to_json
            FROM 
            {0}
            CROSS JOIN LATERAL (
                -- (3) get the tags of some feature on JSON format   
                SELECT json_agg(json_build_object('k', k, 'v', v)) AS jsontags 
                FROM 
                (
                    -- (2) get the tags of some feature
                    SELECT k, v
                    FROM project_tag 
                    WHERE fk_project_id = project.id
                    ORDER BY k, v ASC
                ) subquery      
            ) AS tags
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
            raise HTTPError(404, "Not found any feature.")

        return results_of_query

    def add_project_in_db(self, group_id, user_id):
        query_text = """
            INSERT INTO project (created_at, fk_group_id, fk_user_id)
            VALUES (LOCALTIMESTAMP, {0}, {1}) RETURNING id;
        """.format(group_id, user_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        result = self.__PGSQL_CURSOR__.fetchone()

        return result

    def add_project_tag_in_db(self, k, v, feature_id):
        query_text = """
            INSERT INTO project_tag (k, v, fk_project_id)
            VALUES ('{0}', '{1}', {2});
        """.format(k, v, feature_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

    def create_project(self, feature_json, user_id):

        group_id = feature_json["properties"]["fk_group_id"]

        # add the layer in db and get the id of it
        id_in_json = self.add_project_in_db(group_id, user_id)

        # add in DB the tags of layer
        for tag in feature_json["tags"]:
            # add the layer tag in db
            self.add_project_tag_in_db(tag["k"], tag["v"], id_in_json["id"])

        # put in DB the layer and its tags
        self.commit()

        return id_in_json

    def delete_project_in_db(self, feature_id):
        if is_a_invalid_id(feature_id):
            raise HTTPError(400, "Invalid parameter.")

        query_text = """
            UPDATE project SET visible = FALSE, removed_at = LOCALTIMESTAMP
            WHERE id={0};
        """.format(feature_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        self.commit()

        if rows_affected == 0:
            raise HTTPError(404, "Not found any feature.")

    ################################################################################
    # layer
    ################################################################################

    def get_layers(self, layer_id=None, user_id=None):
        # the id have to be a int
        if is_a_invalid_id(layer_id) or is_a_invalid_id(user_id):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_layer_table(layer_id=layer_id, user_id=user_id)

        # CREATE THE QUERY AND EXECUTE IT
        query_text = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'Layer',
                    'properties', json_build_object(
                        'id',           id,                        
                        'created_at',   to_char(created_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'removed_at',   to_char(removed_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'fk_user_id', fk_user_id
                    ),
                    'tags',       tags.jsontags
                ))
            ) AS row_to_json
            FROM 
            {0}
            CROSS JOIN LATERAL (                
                -- (3) get the tags of some feature on JSON format   
                SELECT json_agg(json_build_object('k', k, 'v', v)) AS jsontags 
                FROM 
                (
                    -- (2) get the tags of some feature
                    SELECT k, v
                    FROM layer_tag 
                    WHERE fk_layer_id = layer.id
                    ORDER BY k, v ASC
                ) subquery      
            ) AS tags
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
            raise HTTPError(404, "Not found any feature.")

        return results_of_query

    def add_layer_in_db(self, project_id, user_id):
        query_text = """
            INSERT INTO layer (created_at, fk_project_id, fk_user_id) 
            VALUES (LOCALTIMESTAMP, {0}, {1}) RETURNING id;
        """.format(project_id, user_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        result = self.__PGSQL_CURSOR__.fetchone()

        return result

    def add_layer_tag_in_db(self, k, v, feature_id):
        query_text = """
            INSERT INTO layer_tag (k, v, fk_layer_id) 
            VALUES ('{0}', '{1}', {2});
        """.format(k, v, feature_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

    def create_layer(self, feature_json, user_id):

        # get the fields to add in DB
        project_id = feature_json["properties"]["fk_project_id"]

        # add the layer in db and get the id of it
        id_in_json = self.add_layer_in_db(project_id, user_id)

        # add in DB the tags of layer
        for tag in feature_json["tags"]:
            # add the layer tag in db
            self.add_layer_tag_in_db(tag["k"], tag["v"], id_in_json["id"])

        # put in DB the layer and its tags
        self.commit()

        return id_in_json

    def delete_layer_in_db(self, feature_id):
        if is_a_invalid_id(feature_id):
            raise HTTPError(400, "Invalid parameter.")

        query_text = """
            UPDATE layer SET visible = FALSE, removed_at = LOCALTIMESTAMP
            WHERE id={0};
        """.format(feature_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        self.commit()

        if rows_affected == 0:
            raise HTTPError(404, "Not found any feature.")

    ################################################################################
    # CHANGESET
    ################################################################################

    def get_changesets(self, changeset_id=None, user_id=None, layer_id=None, open=None, closed=None):
        # the id have to be a int
        if is_a_invalid_id(changeset_id) or is_a_invalid_id(user_id):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_changeset_table(changeset_id=changeset_id, layer_id=layer_id,
                                                user_id=user_id, open=open, closed=closed)

        # CREATE THE QUERY AND EXECUTE IT
        query_text = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'Changeset',
                    'properties', json_build_object(
                        'id',           id,                        
                        'created_at',   to_char(created_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'closed_at',    to_char(closed_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'fk_layer_id',    fk_layer_id,
                        'fk_user_id', fk_user_id
                    ),
                    'tags',       tags.jsontags
                ))
            ) AS row_to_json
            FROM 
            {0}
            CROSS JOIN LATERAL (
                -- (3) get the tags of some element on JSON format   
                SELECT json_agg(json_build_object('k', k, 'v', v)) AS jsontags 
                FROM 
                (
                    -- (2) get the tags of some element
                    SELECT k, v
                    FROM changeset_tag 
                    WHERE fk_changeset_id = changeset.id
                    ORDER BY k, v ASC
                ) subquery
            ) AS tags
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
            raise HTTPError(404, "Not found any feature.")

        return results_of_query

    def add_changeset_in_db(self, layer_id, user_id):
        """
        Add a changeset in DB
        :param layer_id: id of the layer associated with the changeset
        :param user_id: id of the user (owner) of the changeset
        :return: the id of the changeset created inside a JSON, example: {"id": -1}
        """

        query_text = """
            INSERT INTO changeset (created_at, fk_layer_id, fk_user_id) 
            VALUES (LOCALTIMESTAMP, {0}, {1}) RETURNING id;
        """.format(layer_id, user_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        result = self.__PGSQL_CURSOR__.fetchone()

        return result

    def add_changeset_tag_in_db(self, k, v, feature_id):
        query_text = """
            INSERT INTO changeset_tag (k, v, fk_changeset_id) 
            VALUES ('{0}', '{1}', {2});
        """.format(k, v, feature_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        # id_changeset_tag = self.__PGSQL_CURSOR__.fetchone()

        # return id_changeset_tag

    def create_changeset(self, feature_json, user_id):

        # get the fields to add in DB
        layer_id = feature_json["properties"]["fk_layer_id"]

        # add the chengeset in db and get the id of it
        changeset_id_in_json = self.add_changeset_in_db(layer_id, user_id)

        # add in DB the tags of changeset
        for tag in feature_json["tags"]:
            # add the chengeset tag in db
            self.add_changeset_tag_in_db(tag["k"], tag["v"], changeset_id_in_json["id"])

        # put in DB the changeset and its tags
        self.commit()

        return changeset_id_in_json

    def close_changeset(self, feature_id=None):
        if is_a_invalid_id(feature_id):
            raise HTTPError(400, "Invalid parameter.")

        query_text = """
            UPDATE changeset SET closed_at=LOCALTIMESTAMP WHERE id={0};
        """.format(feature_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        self.commit()

        if rows_affected == 0:
            raise HTTPError(404, "Not found any feature.")

    def delete_changeset_in_db(self, feature_id):
        if is_a_invalid_id(feature_id):
            raise HTTPError(400, "Invalid parameter.")

        query_text = """
            UPDATE changeset SET visible = FALSE
            WHERE id={0};
        """.format(feature_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        self.commit()

        if rows_affected == 0:
            raise HTTPError(404, "Not found any feature.")

    ################################################################################
    # notification
    ################################################################################

    def get_notification(self, notification_id=None, user_id=None, is_read=None):
        # the id have to be a int
        if is_a_invalid_id(notification_id) or is_a_invalid_id(user_id):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_notification_table(notification_id=notification_id, user_id=user_id,
                                                   is_read=is_read)

        # CREATE THE QUERY AND EXECUTE IT
        query_text = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'Notification',
                    'properties', json_build_object(
                        'id',           id,                        
                        'created_at',   to_char(created_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'removed_at',   to_char(removed_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'is_read',      is_read,
                        'visible',      visible,
                        'fk_user_id',   fk_user_id
                    ),
                    'tags',       tags.jsontags
                ))
            ) AS row_to_json
            FROM 
            {0}
            CROSS JOIN LATERAL (
                -- (3) get the tags of some feature on JSON format   
                SELECT json_agg(json_build_object('k', k, 'v', v)) AS jsontags 
                FROM 
                (
                    -- (2) get the tags of some feature
                    SELECT k, v
                    FROM notification_tag 
                    WHERE fk_notification_id = notification.id
                    ORDER BY k, v ASC
                ) subquery      
            ) AS tags
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
            raise HTTPError(404, "Not found any feature.")

        return results_of_query

    def add_notification_in_db(self, user_id):
        query_text = """
            INSERT INTO notification (created_at, fk_user_id)
            VALUES (LOCALTIMESTAMP, {0}) RETURNING id;
        """.format(user_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        result = self.__PGSQL_CURSOR__.fetchone()

        return result

    def add_notification_tag_in_db(self, k, v, feature_id):
        query_text = """
            INSERT INTO notification_tag (k, v, fk_notification_id)
            VALUES ('{0}', '{1}', {2});
        """.format(k, v, feature_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

    def create_notification(self, feature_json, user_id):

        # group_id = feature_json["properties"]["fk_group_id"]

        # add the layer in db and get the id of it
        id_in_json = self.add_notification_in_db(user_id)

        # add in DB the tags of layer
        for tag in feature_json["tags"]:
            # add the layer tag in db
            self.add_notification_tag_in_db(tag["k"], tag["v"], id_in_json["id"])

        # put in DB the layer and its tags
        self.commit()

        return id_in_json

    def delete_notification_in_db(self, feature_id):
        if is_a_invalid_id(feature_id):
            raise HTTPError(400, "Invalid parameter.")

        query_text = """
            UPDATE notification SET visible = FALSE, removed_at = LOCALTIMESTAMP
            WHERE id={0};
        """.format(feature_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        self.commit()

        if rows_affected == 0:
            raise HTTPError(404, "Not found any feature.")

    ################################################################################
    # ELEMENT
    ################################################################################

    # get elements

    def get_elements(self, element, **arguments):
        if not are_arguments_valid_to_get_elements(**arguments):
            raise HTTPError(400, "Invalid parameter.")

        return self.get_elements_geojson(element, **arguments)

    def get_elements_geojson(self, element, element_id=None, user_id=None, layer_id=None,
                             changeset_id=None):

        subquery_current_element_table = get_subquery_current_element_table(element,
                                                                            element_id=element_id,
                                                                            user_id=user_id,
                                                                            layer_id=layer_id,
                                                                            changeset_id=changeset_id)

        query_text = """
            SELECT jsonb_build_object(
                'type',       'FeatureCollection',
                'crs',  json_build_object(
                    'type',      'name', 
                    'properties', json_build_object(
                        'name', 'EPSG:4326'
                    )
                ),
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'Feature',
                    'geometry',   ST_AsGeoJSON(geom)::jsonb,
                    'properties', json_build_object(
                        'id',               id,
                        'visible',          visible,
                        'version',          version,
                        'fk_changeset_id',  fk_changeset_id
                    ),
                    'tags',       tags.jsontags
                ))
            ) AS row_to_json
            FROM 
            {1}
            CROSS JOIN LATERAL ( 
                -- (3) get the tags of some element on JSON format   
                SELECT json_agg(json_build_object('k', k, 'v', v)) AS jsontags 
                FROM 
                (
                    -- (2) get the tags of some element
                    SELECT k, v
                    FROM current_{0}_tag 
                    WHERE fk_current_{0}_id = element.id
                    ORDER BY k, v ASC
                ) subquery             
            ) AS tags
        """.format(element, subquery_current_element_table)

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
            raise HTTPError(404, "Not found any feature.")

        return results_of_query

    # add elements

    def add_element_in_db(self, element, geometry, changeset_id):

        # encode the dict in JSON
        geometry = json_encode(geometry)

        query_text = """
            INSERT INTO current_{0} (geom, fk_changeset_id) 
            VALUES (ST_GeomFromGeoJSON('{1}'), {2})
            RETURNING id;
        """.format(element, geometry, changeset_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        result = self.__PGSQL_CURSOR__.fetchone()

        return result["id"]

    def add_element_tag_in_db(self, k, v, element, element_id):
        query_text = """
            INSERT INTO current_{0}_tag (k, v, fk_current_{0}_id) 
            VALUES ('{1}', '{2}', {3});
        """.format(element, k, v, element_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

    def create_element(self, element, feature):
        # TODO: before to add, verify if the user is valid. If the user that is adding, is really the correct user
        # searching if the changeset is its by fk_user_id. If the user is the owner of the changeset

        # get the tags
        tags = feature["tags"]

        # remove the "tags" key from feature (it is not necessary)
        del feature["tags"]

        # get the id of changeset
        changeset_id = feature["properties"]["fk_changeset_id"]

        # add the element in db and get the id of it
        element_id = self.add_element_in_db(element, feature["geometry"], changeset_id)

        for tag in tags:
            # add the element tag in db
            # PS: how the element is new in db, so the fk_element_version = 1
            self.add_element_tag_in_db(tag["k"], tag["v"], element, element_id)

        # put in DB the element and its tags
        # self.commit()

        return element_id

    # delete elements

    def delete_element_in_db(self, element, element_id):
        if is_a_invalid_id(element_id):
            raise HTTPError(400, "Invalid parameter.")

        query_text = """
            UPDATE current_{0} SET visible = FALSE WHERE id={1};
            """.format(element, element_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        self.commit()

        if rows_affected == 0:
            raise HTTPError(404, "Not found any feature.")

    ################################################################################
    # user
    ################################################################################

    def get_users(self, user_id=None, email=None, password=None):
        # the id have to be a int
        if is_a_invalid_id(user_id):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_user_table(user_id=user_id, email=email, password=password)

        # CREATE THE QUERY AND EXECUTE IT
        query_text = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'User',
                    'properties', json_build_object(
                        'id',           id,
                        'username', username,
                        'email', email,
                        'is_email_valid', is_email_valid,           
                        'created_at',    to_char(created_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'removed_at',   to_char(removed_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'terms_agreed', terms_agreed
                    ),
                    'tags',       tags.jsontags
                ))
            ) AS row_to_json
            FROM 
            {0}
            CROSS JOIN LATERAL (
                SELECT json_agg(json_build_object('k', k, 'v', v)) AS jsontags 
                FROM user_tag 
                WHERE fk_user_id = user_.id    
            ) AS tags
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
            raise HTTPError(404, "Not found any feature.")

        return results_of_query

    def add_user_in_db(self, properties):
        p = properties

        query_text = """
            INSERT INTO user_ (email, username, password, created_at) 
            VALUES ('{0}', '{1}', '{2}', LOCALTIMESTAMP)
            RETURNING id;
        """.format(p["email"], p["username"], p["password"])

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        result = self.__PGSQL_CURSOR__.fetchone()

        return result

    def add_user_tag_in_db(self, k, v, feature_id):
        query_text = """
            INSERT INTO user_tag (k, v, fk_user_id)
            VALUES ('{0}', '{1}', {2});
        """.format(k, v, feature_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

    def create_user(self, feature_json):

        properties = feature_json["properties"]

        id_in_json = self.add_user_in_db(properties)

        # add in DB the tags of layer
        for tag in feature_json["tags"]:
            # add the layer tag in db
            self.add_user_tag_in_db(tag["k"], tag["v"], id_in_json["id"])

        # put in DB the layer and its tags
        self.commit()

        return id_in_json

    # delete user

    def delete_user(self, feature_id):
        if is_a_invalid_id(feature_id):
            raise HTTPError(400, "Invalid parameter.")

        query_text = """
            UPDATE user_ SET visible = FALSE, removed_at = LOCALTIMESTAMP
            WHERE id={0};
        """.format(feature_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        rows_affected = self.__PGSQL_CURSOR__.rowcount

        self.commit()

        if rows_affected == 0:
            raise HTTPError(404, "Not found any feature.")

@Singleton
class Neo4JConnection(BaseDBConnection):

    def __init__(self, args={}):
        super().__init__()  # call the __init__ from super class

        self.__ARGS__ = args

        if self.__ARGS__["DEBUG_MODE"]:
            self.__DO_CONNECTION__(__DEBUG_NEO4J_CONNECTION_SETTINGS__)
        else:
            self.__DO_CONNECTION__(__NEO4J_CONNECTION_SETTINGS__)

    def __DO_CONNECTION__(self, __connection_settings__):
        """
        Do the DB connection with the '__pgsql_connection_settings__'
        :param __connection_settings__: the connection settings of Neo4J.
        It can be for the normal DB or test DB
        :return:
        """

        # create a session to do the requests
        self.session = Session()

        # username_and_password = __connection_settings__["USERNAME"] + ":" + __connection_settings__["PASSWORD"]
        # string_in_base64 = (b64encode(username_and_password.encode('utf-8'))).decode('utf-8')

        string_in_base64 = get_username_and_password_as_string_in_base64(__connection_settings__["USERNAME"],
                                                                         __connection_settings__["PASSWORD"])

        self.headers = {'Content-type': 'application/json',
                        'Accept': 'application/json; charset=UTF-8',
                        'Authorization': 'Basic ' + string_in_base64}

        self.URL = "http://" + __connection_settings__["HOSTNAME"] + ":" + str(__connection_settings__["PORT"])

        if self.__ARGS__["DEBUG_MODE"]:
            print("\nConnecting in Neo4J with:"
                  "\n- hostname: ", __connection_settings__["HOSTNAME"],
                  "\n- port: ", __connection_settings__["PORT"],
                  "\n- database: ", __connection_settings__["DATABASE"],
                  "\n- URL: ", self.URL, "\n")

        neo4j_status = self.is_connecting_with_db()

        self.set_connection_status(status=neo4j_status)

    def is_connecting_with_db(self):
        """
        Try to do a connection with Neo4J. If it works, so return True, else return False;
        :return: one boolean value, depending of the connection status.
        """
        try:
            self.session.get(self.URL + '/db/data/', headers=self.headers)

            # response = self.session.get(self.URL + '/db/data/', headers=self.headers)
            # result = loads(response.text)
            # print("\n>>> result: ", result, "\n")
        except exceptions.ConnectionError:
            return False

        return True

    @if_neo4j_is_not_running_so_put_db_offline_and_raise_500_error_status
    def match(self, query, params={}):

        query_dict = {
            "query": query,
            "params": params
        }

        response = self.session.post(self.URL + '/db/data/cypher',
                                     data=dumps(query_dict), headers=self.headers)

        result = loads(response.text)

        return result

    def get_theme_tree(self):

        result = self.match("""
                    MATCH path = (generic:Theme {key: "generic"})-[:can_be*]-(:Theme)
                    WITH collect(path) as paths
                    CALL apoc.convert.toTree(paths) yield value
                    RETURN value;
                """)

        return result
