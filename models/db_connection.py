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


from tornado.web import HTTPError
from tornado.escape import json_encode

from psycopg2 import connect, DatabaseError
from psycopg2._psycopg import ProgrammingError
from psycopg2.extras import RealDictCursor

from settings.db_settings import __PGSQL_CONNECTION_SETTINGS__, __DEBUG_PGSQL_CONNECTION_SETTINGS__
from modules.design_pattern import Singleton

from .util import *


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

    def __DO_CONNECTION__(self, __pgsql_connection_settings__):
        """
        Do the DB connection with the '__pgsql_connection_settings__'
        :param __pgsql_connection_settings__: the connection settings of PostgreSQL.
        It can be for the normal DB or test DB
        :return:
        """
        if self.__ARGS__["DEBUG_MODE"]:
            print("\nConnecting in PostgreSQL with:"
                  "\n- hostname: ", __pgsql_connection_settings__["HOSTNAME"],
                  "\n- port: ", __pgsql_connection_settings__["PORT"],
                  "\n- database: ", __pgsql_connection_settings__["DATABASE"], "\n")

        try:
            self.__PGSQL_CONNECTION__ = connect(host=__pgsql_connection_settings__["HOSTNAME"],
                                                port=__pgsql_connection_settings__["PORT"],
                                                user=__pgsql_connection_settings__["USERNAME"],
                                                password=__pgsql_connection_settings__["PASSWORD"],
                                                dbname=__pgsql_connection_settings__["DATABASE"])
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
    # PROJECT
    ################################################################################

    def get_projects(self, project_id=None, user_id=None):
        # the id have to be a int
        if is_a_invalid_id(project_id) or is_a_invalid_id(user_id):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_project_table(project_id=project_id, user_id=user_id)

        # CREATE THE QUERY AND EXECUTE IT
        query_text = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'Project',
                    'properties', json_build_object(
                        'id',           id,                        
                        'create_at',    to_char(create_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'removed_at',   to_char(removed_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'fk_user_id_owner', fk_user_id_owner
                    ),
                    'tags',       tags.jsontags
                ))
            ) AS row_to_json
            FROM 
            {0}
            CROSS JOIN LATERAL (
                SELECT json_agg(json_build_object('k', k, 'v', v)) AS jsontags 
                FROM project_tag 
                WHERE fk_project_id = project.id    
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

    def add_project_in_db(self, fk_user_id_owner):
        query_text = """
            INSERT INTO project (create_at, fk_user_id_owner) 
            VALUES (LOCALTIMESTAMP, {0}) RETURNING id;
        """.format(fk_user_id_owner)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        result = self.__PGSQL_CURSOR__.fetchone()

        return result

    def add_project_tag_in_db(self, k, v, fk_project_id):
        query_text = """
            INSERT INTO project_tag (k, v, fk_project_id) 
            VALUES ('{0}', '{1}', {2});
        """.format(k, v, fk_project_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

    def create_project(self, project_json, fk_user_id_owner):

        project = project_json["project"]

        # add the project in db and get the id of it
        project_id_in_json = self.add_project_in_db(fk_user_id_owner)

        # add in DB the tags of project
        for tag in project["tags"]:
            # add the project tag in db
            self.add_project_tag_in_db(tag["k"], tag["v"], project_id_in_json["id"])

        # put in DB the project and its tags
        self.commit()

        return project_id_in_json

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
    # CHANGESET
    ################################################################################

    def get_changesets(self, changeset_id=None, user_id=None, project_id=None, open=None, closed=None):
        # the id have to be a int
        if is_a_invalid_id(changeset_id) or is_a_invalid_id(user_id):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_changeset_table(changeset_id=changeset_id, project_id=project_id,
                                                user_id=user_id, open=open, closed=closed)

        # CREATE THE QUERY AND EXECUTE IT
        query_text = """
            SELECT jsonb_build_object(
                'type', 'FeatureCollection',
                'features',   jsonb_agg(jsonb_build_object(
                    'type',       'Changeset',
                    'properties', json_build_object(
                        'id',           id,                        
                        'create_at',    to_char(create_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'closed_at',    to_char(closed_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'fk_project_id',    fk_project_id,
                        'fk_user_id_owner', fk_user_id_owner
                    ),
                    'tags',       tags.jsontags
                ))
            ) AS row_to_json
            FROM 
            {0}
            CROSS JOIN LATERAL (
                SELECT json_agg(json_build_object('k', k, 'v', v)) AS jsontags 
                FROM changeset_tag 
                WHERE fk_changeset_id = changeset.id    
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

    def add_changeset_in_db(self, fk_project_id, fk_user_id_owner):
        """
        Add a changeset in DB
        :param fk_project_id: id of the project associated with the changeset
        :param fk_user_id_owner: id of the user (owner) of the changeset
        :return: the id of the changeset created inside a JSON, example: {"id": -1}
        """

        query_text = """
            INSERT INTO changeset (create_at, fk_project_id, fk_user_id_owner) 
            VALUES (LOCALTIMESTAMP, {0}, {1}) RETURNING id;
        """.format(fk_project_id, fk_user_id_owner)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        result = self.__PGSQL_CURSOR__.fetchone()

        return result

    def add_changeset_tag_in_db(self, k, v, fk_changeset_id):
        query_text = """
            INSERT INTO changeset_tag (k, v, fk_changeset_id) 
            VALUES ('{0}', '{1}', {2});
        """.format(k, v, fk_changeset_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        # id_changeset_tag = self.__PGSQL_CURSOR__.fetchone()

        # return id_changeset_tag

    def create_changeset(self, changeset_json, fk_user_id_owner):

        changeset = changeset_json["changeset"]

        # get the fields to add in DB
        fk_project_id = changeset["properties"]["fk_project_id"]

        # add the chengeset in db and get the id of it
        changeset_id_in_json = self.add_changeset_in_db(fk_project_id, fk_user_id_owner)

        # add in DB the tags of changeset
        for tag in changeset["tags"]:
            # add the chengeset tag in db
            self.add_changeset_tag_in_db(tag["k"], tag["v"], changeset_id_in_json["id"])

        # put in DB the changeset and its tags
        self.commit()

        return changeset_id_in_json

    def close_changeset(self, changeset_id=None):
        if is_a_invalid_id(changeset_id):
            raise HTTPError(400, "Invalid parameter.")

        query_text = """
            UPDATE changeset SET closed_at=LOCALTIMESTAMP WHERE id={0};
        """.format(changeset_id)

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
    # ELEMENT
    ################################################################################

    # get elements

    def get_elements(self, element, **arguments):
        if not are_arguments_valid_to_get_elements(**arguments):
            raise HTTPError(400, "Invalid parameter.")

        return self.get_elements_geojson(element, **arguments)

    def get_elements_geojson(self, element, element_id=None, user_id=None, project_id=None,
                             changeset_id=None):

        subquery_current_element_table = get_subquery_current_element_table(element,
                                                                            element_id=element_id,
                                                                            user_id=user_id,
                                                                            project_id=project_id,
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
                        'fk_changeset_id',  fk_changeset_id
                    ),
                    'tags',       tags.jsontags
                ))
            ) AS row_to_json
            FROM 
            {1}
            CROSS JOIN LATERAL ( 
                -- (2) get the tags of some element
                SELECT json_agg(json_build_object('k', k, 'v', v)) AS jsontags 
                FROM current_{0}_tag 
                WHERE fk_current_{0}_id = element.id                
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

    def add_element_in_db(self, element, geometry, fk_changeset_id):
        """
        :param element:
        :param element_json:
        :param fk_id_changeset:
        :return:
        """

        # encode the dict in JSON
        geometry = json_encode(geometry)

        query_text = """
            INSERT INTO current_{0} (geom, fk_changeset_id) 
            VALUES (ST_GeomFromGeoJSON('{1}'), {2})
            RETURNING id;
        """.format(element, geometry, fk_changeset_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        result = self.__PGSQL_CURSOR__.fetchone()

        return result["id"]

        list_of_id_of_features_created = []
    def add_element_tag_in_db(self, k, v, element, fk_element_id):
        query_text = """
            INSERT INTO current_{0}_tag (k, v, fk_current_{0}_id) 
            VALUES ('{1}', '{2}', {3});
        """.format(element, k, v, fk_element_id)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

    def create_element(self, element, feature, fk_user_id_owner):
        """
        Add a element in DB
        :param element_json:
        :param fk_user_id_owner:
        :return: the id of the element created
        """

        # TODO: before to add, verify if the user is valid. If the user that is adding, is really the correct user
        # searching if the changeset is its by fk_user_id_owner. If the user is the owner of the changeset

        # get the tags
        tags = feature["tags"]

        # remove the "tags" key from feature (it is not necessary)
        del feature["tags"]

        # get the id of changeset
        fk_changeset_id = feature["properties"]["fk_changeset_id"]

        # add the element in db and get the id of it
        element_id = self.add_element_in_db(element, feature["geometry"], fk_changeset_id)

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
    # USER
    ################################################################################

    def get_users(self, user_id=None):
        # the id have to be a int
        if is_a_invalid_id(user_id):
            raise HTTPError(400, "Invalid parameter.")

        subquery = get_subquery_user_table(user_id=user_id)

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
                        'name', name,
                        'is_email_valid', is_email_valid,
                        'description', description,                
                        'create_at',    to_char(create_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'removed_at',   to_char(removed_at, 'YYYY-MM-DD HH24:MI:SS'),
                        'terms_agreed', terms_agreed,
                        'terms_seen', terms_seen
                    ),
                    'tags',       tags.jsontags
                ))
            ) AS row_to_json
            FROM 
            {0}
            CROSS JOIN LATERAL (
                SELECT json_agg(json_build_object('k', k, 'v', v)) AS jsontags 
                FROM user_tag 
                WHERE fk_user_id = user.id    
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

    def get_user_in_db(self, email):
        query_text = """
            SELECT id, username, name, email FROM user_ WHERE email='{0}';
            """.format(email)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the result of query
        result = self.__PGSQL_CURSOR__.fetchone()

        return result

    def create_user_in_db(self, email):
        query_text = """INSERT INTO user_ (email) VALUES ('{0}');""".format(email)

        # do the query in database
        self.__PGSQL_CURSOR__.execute(query_text)

        # get the user information (id, name, username, email, etc)
        result = self.get_user_in_db(email)

        self.commit()

        return result
