#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_subquery_layer_table(**kwargs):
    # DEFAULT WHERE
    # by default, get all results that are visible (that exist)
    # conditions_of_where = ["removed_at is NULL"]  # visible=True
    layer_keyword_subquery = ""
    conditions_of_where = []  # visible=True

    # conditions of WHERE CLAUSE
    if "layer_id" in kwargs and kwargs["layer_id"] is not None:
        conditions_of_where.append("layer_id = {0}".format(kwargs["layer_id"]))

    if "f_table_name" in kwargs and kwargs["f_table_name"] is not None:
        conditions_of_where.append("unaccent(LOWER(f_table_name)) LIKE '%' || unaccent(LOWER('{0}')) || '%'".format(kwargs["f_table_name"]))

    # default get all features, without where clause
    where_clause = ""

    # if there is some conditions, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    # if is searching by keyword_id, so do a subquery with layer_keyword, putting the
    # keyword_id and the where_clause...
    if "keyword_id" in kwargs and kwargs["keyword_id"] is not None:
        subquery_table = """
            (
                SELECT * FROM
                (
                    SELECT layer_id as lk_layer_id, keyword_id
                    FROM layer_keyword WHERE keyword_id = {0}
                ) lk
                LEFT JOIN layer l
                ON lk.lk_layer_id = l.layer_id
                {1}
                ORDER BY l.layer_id
            ) AS layer
        """.format(kwargs["keyword_id"], where_clause)

    # ... else do a basic SELECT
    else:
        # default get all features
        subquery_table = """
            (
                SELECT * FROM layer {0} ORDER BY layer_id
            ) AS layer
        """.format(where_clause)

    return subquery_table


def get_subquery_layer_follower_table(**kwargs):
    # DEFAULT WHERE
    conditions_of_where = []

    # conditions of WHERE CLAUSE
    if "layer_id" in kwargs and kwargs["layer_id"] is not None:
        conditions_of_where.append("layer_id = {0}".format(kwargs["layer_id"]))

    if "user_id" in kwargs and kwargs["user_id"] is not None:
        conditions_of_where.append("user_id = '{0}'".format(kwargs["user_id"]))

    # default get all features, without where clause
    where_clause = ""

    # if there is some conditions, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    # default get all features
    subquery_table = """
        (
            SELECT * FROM layer_followers {0} ORDER BY layer_id, user_id
        ) AS layer_followers
    """.format(where_clause)

    return subquery_table


def get_subquery_layer_reference_table(**kwargs):
    # DEFAULT WHERE
    conditions_of_where = []

    # conditions of WHERE CLAUSE
    if "layer_id" in kwargs and kwargs["layer_id"] is not None:
        conditions_of_where.append("layer_id = {0}".format(kwargs["layer_id"]))

    if "reference_id" in kwargs and kwargs["reference_id"] is not None:
        conditions_of_where.append("reference_id = '{0}'".format(kwargs["reference_id"]))

    # default get all features, without where clause
    where_clause = ""

    # if there is some conditions, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    # default get all features
    subquery_table = """
        (
            SELECT * FROM layer_reference {0} ORDER BY layer_id, reference_id
        ) AS layer_reference
    """.format(where_clause)

    return subquery_table

# def get_subquery_user_layer_table(**kwargs):
#     # DEFAULT WHERE
#     # by default, get all results that are visible (that exist)
#     # conditions_of_where = ["removed_at is NULL"]  # visible=True
#     conditions_of_where = []  # visible=True
#
#     # conditions of WHERE CLAUSE
#     if "layer_id" in kwargs and kwargs["layer_id"] is not None:
#         conditions_of_where.append("layer_id = {0}".format(kwargs["layer_id"]))
#
#     if "user_id" in kwargs and kwargs["user_id"] is not None:
#         conditions_of_where.append("user_id = '{0}'".format(kwargs["user_id"]))
#
#     if "is_the_creator" in kwargs and kwargs["is_the_creator"] is not None:
#         conditions_of_where.append("is_the_creator = {0}".format(kwargs["is_the_creator"]))
#
#     # default get all features, without where clause
#     where_clause = ""
#
#     # if there is some conditions, put in where_clause
#     if conditions_of_where:
#         where_clause = "WHERE " + " AND ".join(conditions_of_where)
#
#     # default get all features
#     subquery_table = """
#         (
#             SELECT * FROM user_layer {0} ORDER BY layer_id, user_id
#         ) AS user_layer
#     """.format(where_clause)
#
#     return subquery_table
