#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_subquery_changeset_table(**kwargs):
    conditions_of_where = []

    # conditions of WHERE CLAUSE
    if "changeset_id" in kwargs and kwargs["changeset_id"] is not None:
        conditions_of_where.append("changeset.id = {0}".format(kwargs["changeset_id"]))

    elif "project_id" in kwargs and kwargs["project_id"] is not None:
        conditions_of_where.append("changeset.fk_project_id = {0}".format(kwargs["project_id"]))

    elif "user_id" in kwargs and kwargs["user_id"] is not None:
        conditions_of_where.append("changeset.fk_user_id_owner = {0}".format(kwargs["user_id"]))

    else:
        # default get all features, without where clause
        pass

    # default get all features, without where clause
    where_clause = ""

    # if there is some condition, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    subquery_table = """
        (
            SELECT id, create_at, closed_at, fk_project_id, fk_user_id_owner FROM changeset {0} 
        ) AS changeset
    """.format(where_clause)

    return subquery_table
