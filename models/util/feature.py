#!/usr/bin/env python
# -*- coding: utf-8 -*-


# def build_column_names_from_list_of_column_name_with_type(list_of_column_name_with_type):
#     column_names = []
#
#     for column_name_with_type in list_of_column_name_with_type:
#         # if the column is a geometry, so transform the geom to text
#         if "geometry" in column_name_with_type["type"]:
#             string = "ST_AsText(" + column_name_with_type["column_name"] + ") as " + column_name_with_type["column_name"]
#         else:
#             string = column_name_with_type["column_name"]
#
#         column_names.append(string)
#
#     column_names = ", ".join(column_names)
#
#     return column_names


def get_subquery_feature(f_table_name, feature_id, columns_of_table):
    # DEFAULT WHERE
    # by default, get all results
    conditions_of_where = []

    # conditions of WHERE CLAUSE
    if feature_id is not None:
        conditions_of_where.append("id = {0}".format(feature_id))

    # default get all features, without where clause
    where_clause = ""

    # if there is some condition, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    # default get all features
    subquery_table = """
        (
            SELECT * FROM {0} {1} ORDER BY id
        ) AS feature
    """.format(f_table_name, where_clause)

    return subquery_table
