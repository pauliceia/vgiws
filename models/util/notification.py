#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_subquery_notification_table(**kwargs):
    # DEFAULT WHERE
    # by default, get all results that are visible (that exist)
    conditions_of_where = ["visible=TRUE"]

    # conditions of WHERE CLAUSE
    if "notification_id" in kwargs and kwargs["notification_id"] is not None:
        conditions_of_where.append("id = {0}".format(kwargs["notification_id"]))

    elif "user_id" in kwargs and kwargs["user_id"] is not None:
        conditions_of_where.append("fk_user_id = {0}".format(kwargs["user_id"]))

    else:
        # default get all features, without where clause
        pass

    # extra condition
    if "is_read" in kwargs and kwargs["is_read"] is not None:
        condition = "TRUE" if kwargs["is_read"] == "True" else "FALSE"

        conditions_of_where.append("is_read = {0}".format(condition))


    # default get all features, without where clause
    where_clause = ""

    # if there is some condition, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    # default get all features
    subquery_table = """
        (
            SELECT * FROM notification {0} ORDER BY id
        ) AS notification
    """.format(where_clause)

    return subquery_table
