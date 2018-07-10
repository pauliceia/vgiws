#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_subquery_mask_table(**kwargs):
    # DEFAULT WHERE
    conditions_of_where = []

    # conditions of WHERE CLAUSE
    if "mask_id" in kwargs and kwargs["mask_id"] is not None:
        conditions_of_where.append("mask_id = {0}".format(kwargs["mask_id"]))

    # default get all resources, without where clause
    where_clause = ""

    # if there is some conditions, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    # default get all resources, ordering by id
    subquery_table = """
        (
            SELECT * FROM mask {0} ORDER BY mask_id
        ) AS mask
    """.format(where_clause)

    return subquery_table
