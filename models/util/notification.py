#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_subquery_notification_table(**kwargs):
    # DEFAULT WHERE
    # by default, get all results
    conditions_of_where = []

    # conditions of WHERE CLAUSE
    if "notification_id" in kwargs and kwargs["notification_id"] is not None:
        conditions_of_where.append("notification_id = {0}".format(kwargs["notification_id"]))

    if "is_denunciation" in kwargs and kwargs["is_denunciation"] is not None:
        conditions_of_where.append("is_denunciation = {0}".format(kwargs["is_denunciation"]))

    if "user_id_creator" in kwargs and kwargs["user_id_creator"] is not None:
        conditions_of_where.append("user_id_creator = {0}".format(kwargs["user_id_creator"]))

    if "keyword_id" in kwargs and kwargs["keyword_id"] is not None:
        if kwargs["keyword_id"] == "NULL" or kwargs["keyword_id"] == "None":
            conditions_of_where.append("keyword_id is {0}".format(kwargs["keyword_id"]))
        else:
            conditions_of_where.append("keyword_id = {0}".format(kwargs["keyword_id"]))

    if "layer_id" in kwargs and kwargs["layer_id"] is not None:
        if kwargs["layer_id"] == "NULL" or kwargs["layer_id"] == "None":
            conditions_of_where.append("layer_id is {0}".format(kwargs["layer_id"]))
        else:
            conditions_of_where.append("layer_id = {0}".format(kwargs["layer_id"]))

    if "notification_id_parent" in kwargs and kwargs["notification_id_parent"] is not None:
        if kwargs["notification_id_parent"] == "NULL" or kwargs["notification_id_parent"] == "None":
            conditions_of_where.append("notification_id_parent is {0}".format(kwargs["notification_id_parent"]))
        else:
            conditions_of_where.append("notification_id_parent = {0}".format(kwargs["notification_id_parent"]))

    # default get all features, without where clause
    where_clause = ""

    # if there is some condition, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    # default get all features
    subquery_table = """
        (
            SELECT * FROM notification {0} ORDER BY created_at DESC, notification_id DESC
        ) AS notification
    """.format(where_clause)

    return subquery_table
