#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_subquery_layer_table(**kwargs):
    # DEFAULT WHERE
    # by default, get all results that are visible (that exist)
    conditions_of_where = ["removed_at is NULL"]  # visible=True

    # conditions of WHERE CLAUSE
    if "layer_id" in kwargs and kwargs["layer_id"] is not None:
        conditions_of_where.append("id = {0}".format(kwargs["layer_id"]))

    if "table_name" in kwargs and kwargs["table_name"] is not None:
        conditions_of_where.append("table_name = '{0}'".format(kwargs["table_name"]))

    if "user_id_author" in kwargs and kwargs["user_id_author"] is not None:
        conditions_of_where.append("fk_user_id_author = {0}".format(kwargs["user_id_author"]))

    if "is_published" in kwargs and kwargs["is_published"] is not None:
        conditions_of_where.append("is_published = {0}".format(kwargs["is_published"]))

    # default get all features, without where clause
    where_clause = ""

    # if there is some conditions, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    # default get all features
    subquery_table = """
        (
            SELECT * FROM layer {0} ORDER BY id
        ) AS layer
    """.format(where_clause)

    return subquery_table
