#!/usr/bin/env python
# -*- coding: utf-8 -*-


# test

def get_subquery_user_table(**kwargs):
    conditions_of_where = []

    # conditions of WHERE CLAUSE
    if "user_id" in kwargs and kwargs["user_id"] is not None:
        conditions_of_where.append("user_.id = {0}".format(kwargs["user_id"]))

    # default get all features, without where clause
    where_clause = ""

    # if there is some condition, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    # default get all features
    subquery_table = """
    (
        SELECT id, username, email, is_email_valid, create_at, removed_at, terms_agreed
        FROM user_ {0} ORDER BY id
    ) AS user_
    """.format(where_clause)

    return subquery_table
