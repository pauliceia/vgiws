#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_subquery_curator_table(**kwargs):
    # DEFAULT WHERE
    # by default, get all results
    conditions_of_where = []

    # conditions of WHERE CLAUSE
    if "user_id" in kwargs and kwargs["user_id"] is not None:
        conditions_of_where.append("user_id = {0}".format(kwargs["user_id"]))

    if "keyword_id" in kwargs and kwargs["keyword_id"] is not None:
        conditions_of_where.append("keyword_id = {0}".format(kwargs["keyword_id"]))

    if "region" in kwargs and kwargs["region"] is not None:
        conditions_of_where.append("unaccent(LOWER(region)) LIKE '%' || unaccent(LOWER('{0}')) || '%'".format(kwargs["region"]))

    # default get all features, without where clause
    where_clause = ""

    # if there is some conditions, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    # default get all features
    subquery_table = """
        (
            SELECT * FROM curator {0} ORDER BY user_id, keyword_id
        ) AS curator
    """.format(where_clause)

    return subquery_table
