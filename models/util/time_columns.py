#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_subquery_time_columns_table(**kwargs):
    # DEFAULT WHERE
    # by default, get all results
    conditions_of_where = []

    # conditions of WHERE CLAUSE
    if "f_table_name" in kwargs and kwargs["f_table_name"] is not None:
        conditions_of_where.append("unaccent(LOWER(f_table_name)) LIKE '%' || unaccent(LOWER('{0}')) || '%'".format(kwargs["f_table_name"]))

    if "start_date_column_name" in kwargs and kwargs["start_date_column_name"] is not None:
        conditions_of_where.append("unaccent(LOWER(start_date_column_name)) LIKE '%' || unaccent(LOWER('{0}')) || '%'".format(kwargs["start_date_column_name"]))

    if "end_date_column_name" in kwargs and kwargs["end_date_column_name"] is not None:
        conditions_of_where.append("unaccent(LOWER(end_date_column_name)) LIKE '%' || unaccent(LOWER('{0}')) || '%'".format(kwargs["end_date_column_name"]))

    if "start_date" in kwargs and kwargs["start_date"] is not None:
        conditions_of_where.append("start_date = '{0}'".format(kwargs["start_date"]))

    if "end_date" in kwargs and kwargs["keyword_id"] is not None:
        conditions_of_where.append("end_date = '{0}'".format(kwargs["end_date"]))

    # default get all features, without where clause
    where_clause = ""

    # if there is some conditions, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    # default get all features
    subquery_table = """
        (
            SELECT * FROM time_columns {0} ORDER BY f_table_name
        ) AS time_columns
    """.format(where_clause)

    return subquery_table
