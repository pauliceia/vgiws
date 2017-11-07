#!/usr/bin/env python
# -*- coding: utf-8 -*-


# put the root project in sys path and import the ROOT_PROJECT_PATH
from common import ROOT_PROJECT_PATH

# now can use the module models
from models.db_connection import PGSQLConnection


__PATH_SQL_SCHEMA_FILE__ = ROOT_PROJECT_PATH + "/files/db/sql/schema/db_pauliceia_by_postgresql.sql"
__PATH_SQL_INSERT_FILE__ = ROOT_PROJECT_PATH + "/files/db/sql/db_pauliceia_insert.sql"


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
    # text = text.replace("\n", " ")
    text = text.replace("  ", "")

    return text


def prepare_test_db_before_tests():
    # create a instance of DB passing arguments
    PGSQLConn = PGSQLConnection.get_instance({"DEBUG_MODE": True})

    # open the schema file and the insert file, both to edit the DB
    with open(__PATH_SQL_SCHEMA_FILE__, 'r') as schema_file, \
            open(__PATH_SQL_INSERT_FILE__, 'r') as insert_file:

        # get the data of files
        schema_data = schema_file.read()
        insert_data = insert_file.read()

        # cleaning and arranging the files
        schema_data = remove_comments_from_sql_file(schema_data)
        schema_data = remove_special_characters(schema_data)

        insert_data = remove_comments_from_sql_file(insert_data)
        insert_data = remove_special_characters(insert_data)

        # executing the SQL files
        PGSQLConn.execute(schema_data, modify_information=True)
        print("Cleaning and creating the schema of DB.")

        PGSQLConn.execute(insert_data, modify_information=True)
        print("Inserting the test data in DB.")

    # close DB
    PGSQLConn.close()


# If the file is run as Python script (main), so execute it
# if the file is called as a module, so doesn't execute it
if __name__ == "__main__":
    prepare_test_db_before_tests()
