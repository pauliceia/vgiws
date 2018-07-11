#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_subquery_feature_table(**kwargs):
    # DEFAULT WHERE
    conditions_of_where = ["table_schema = 'public'",
                           # remove the version feature tables
                           "unaccent(LOWER(table_name)) NOT LIKE '%version%'"]

    # conditions of WHERE CLAUSE
    if "f_table_name" in kwargs and kwargs["f_table_name"] is not None:
        conditions_of_where.append("unaccent(LOWER(table_name)) LIKE '%' || unaccent(LOWER('{0}')) || '%'".format(kwargs["f_table_name"]))

    # default get all resources, without where clause
    where_clause = "WHERE " + " AND ".join(conditions_of_where)

    # default get all resources, ordering by id
    subquery_table = """
        (
            -- (2) do a JOIN with geometry_columns to get the SRID of the feature table
            SELECT isc.table_name as f_table_name, gc.srid as srid, gc.type as type, isc.dict as dict
            FROM (
                -- (1) get the columns name of the feature table as JSON 
                SELECT table_name, JSON_OBJECT(ARRAY_AGG(column_name::TEXT), ARRAY_AGG(udt_name::regtype::TEXT)) as dict
                FROM information_schema.columns
                {0}
                GROUP BY table_name
            ) isc 
            INNER JOIN geometry_columns gc
            ON gc.f_table_name = isc.table_name
            ORDER BY isc.table_name
        ) AS feature_table 
    """.format(where_clause)

    return subquery_table
