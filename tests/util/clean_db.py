#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file clean the DB (main or test).
Parameters:
    --debug=True - iff you want to clean the test database
"""

# get the arguments of the file
from sys import argv
from ast import literal_eval

args = list(argv)
del args[0]  # the first element is the name file, so it is not necessary

arguments = {}

for arg in args:
    parts = arg.split("=")

    # if the value is a boolean, convert it
    if parts[1] == "True" or parts[1] == "False":
        parts[1] = literal_eval(parts[1])

    arguments[parts[0]] = parts[1]


# put the root project in sys path and import the ROOT_PROJECT_PATH
try:
    from config import ROOT_PROJECT_PATH
except:
    from .config import ROOT_PROJECT_PATH


# now can use the module models
from models.db_connection import PGSQLConnection


__PATH_SQL_SCHEMA_FILE__ = ROOT_PROJECT_PATH + "/files/db/sql/schema/02_create_schema_db_for_postgresql.sql"
__PATH_SQL_TRIGGER_FILE__ = ROOT_PROJECT_PATH + "/files/db/sql/03_create_triggers.sql"
__PATH_SQL_INSERT_FILE__ = ROOT_PROJECT_PATH + "/files/db/sql/04_insert_test_values.sql"


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


def prepare_test_db_before_tests(arguments):
    if "--debug" in arguments and arguments["--debug"] is True:
        # create a instance of DB passing arguments
        PGSQLConn = PGSQLConnection.get_instance({"DEBUG_MODE": True})
    else:
        PGSQLConn = PGSQLConnection.get_instance({"DEBUG_MODE": False})

    # open the schema file and the insert file, both to edit the DB
    with open(__PATH_SQL_SCHEMA_FILE__, 'r') as schema_file, \
            open(__PATH_SQL_TRIGGER_FILE__, 'r') as trigger_file, \
                open(__PATH_SQL_INSERT_FILE__, 'r') as insert_file:

        # get the data of files
        schema_data = schema_file.read()
        insert_data = insert_file.read()
        trigger_data = trigger_file.read()

        # cleaning and arranging the files
        schema_data = remove_comments_from_sql_file(schema_data)
        schema_data = remove_special_characters(schema_data)

        trigger_data = remove_comments_from_sql_file(trigger_data)
        trigger_data = remove_special_characters(trigger_data)

        # just insert test data if it is in debug mode
        if "--debug" in arguments and arguments["--debug"] is True:
            print("[1]")
            insert_data = remove_comments_from_sql_file(insert_data)
            insert_data = remove_special_characters(insert_data)

        # executing the SQL files
        print("\nCleaning and creating the schema of DB.")
        PGSQLConn.execute(schema_data, modify_information=True)

        print("Inserting the triggers in DB.")
        PGSQLConn.execute(trigger_data, modify_information=True)

        # just insert test data if it is in debug mode
        if "--debug" in arguments and arguments["--debug"] is True:
            print("[2]")
            print("Inserting the test data in DB.\n")
            PGSQLConn.execute(insert_data, modify_information=True)

        # send modifications to DB
        PGSQLConn.commit()

    # close DB
    PGSQLConn.close()


def are_you_sure_to_clean_database(arguments):
    # if is in debug mode, so ok
    if "--debug" in arguments and arguments["--debug"] is True:
        return True

    option = input("\nAre you sure that you want to CLEAN THE DATABASE? (s/n): ")

    if option.lower().replace(" ", "") != "s":
        print("Bye!")
        return False

    option = input("Are you REALLY SURE that you want to CLEAN THE DATABASE? (s/n): ")

    if option.lower().replace(" ", "") != "s":
        print("Bye!")
        return False

    print("Well, if it is what you want...\n")
    return True


# If the file is run as Python script (main), so execute it
# if the file is called as a module, so doesn't execute it
if __name__ == "__main__":
    if are_you_sure_to_clean_database(arguments):
        prepare_test_db_before_tests(arguments)
