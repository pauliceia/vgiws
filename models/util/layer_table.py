#!/usr/bin/env python
# -*- coding: utf-8 -*-


# test

def get_subquery_layer_table(**kwargs):
    # DEFAULT WHERE
    # by default, get all results that are visible (that exist)
    conditions_of_where = ["layer.visible=TRUE"]

    # conditions of WHERE CLAUSE
    if "layer_id" in kwargs and kwargs["layer_id"] is not None:
        conditions_of_where.append("layer.id = {0}".format(kwargs["layer_id"]))

    elif "user_id" in kwargs and kwargs["user_id"] is not None:
        conditions_of_where.append("layer.fk_user_id = {0}".format(kwargs["user_id"]))

    else:
        # default get all features, without where clause
        pass

    # default get all features, without where clause
    where_clause = ""

    # if there is some condition, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    # default get all features
    subquery_table = """
        (
            SELECT id, create_at, removed_at, fk_user_id 
            FROM layer {0}
            ORDER BY id
        ) AS layer
    """.format(where_clause)

    return subquery_table
