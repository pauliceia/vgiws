#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_subquery_keyword_table(**kwargs):
    # DEFAULT WHERE
    conditions_of_where = []

    # conditions of WHERE CLAUSE
    if "keyword_id" in kwargs and kwargs["keyword_id"] is not None:
        conditions_of_where.append("keyword_id = {0}".format(kwargs["keyword_id"]))

    if "name" in kwargs and kwargs["name"] is not None:
        conditions_of_where.append("unaccent(LOWER(name)) LIKE '%' || unaccent(LOWER('{0}')) || '%'".format(kwargs["name"]))

    if "user_id_creator" in kwargs and kwargs["user_id_creator"] is not None:
        conditions_of_where.append("user_id_creator = {0}".format(kwargs["user_id_creator"]))

    # default get all resources, without where clause
    where_clause = ""

    # if there is some conditions, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    # default get all resources, ordering by id
    subquery_table = """
        (
            SELECT * FROM keyword {0} ORDER BY keyword_id
        ) AS keyword
    """.format(where_clause)

    return subquery_table
