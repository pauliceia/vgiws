#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_subquery_user_table(**kwargs):
    # DEFAULT WHERE
    # by default, get all results
    conditions_of_where = []

    # conditions of WHERE CLAUSE
    if "user_id" in kwargs and kwargs["user_id"] is not None:
        conditions_of_where.append("user_id = {0}".format(kwargs["user_id"]))

    if "email" in kwargs and kwargs["email"] is not None:
        conditions_of_where.append("email = '{0}'".format(kwargs["email"]))

        # if put email and password, so they are trying do a login
        if "password" in kwargs and kwargs["password"] is not None:
            conditions_of_where.append("password = '{0}'".format(kwargs["password"]))

    if "username" in kwargs and kwargs["username"] is not None:
        conditions_of_where.append("username = '{0}'".format(kwargs["username"]))

    # case insensitive query
    if "name" in kwargs and kwargs["name"] is not None:
        conditions_of_where.append("unaccent(LOWER(name)) LIKE '%' || unaccent(LOWER('{0}')) || '%'".format(kwargs["name"]))

    # default get all features, without where clause
    where_clause = ""

    # if there is some condition, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    # default get all features
    subquery_table = """
        (
            SELECT * FROM pauliceia_user {0} ORDER BY user_id
        ) AS user_
    """.format(where_clause)

    return subquery_table
