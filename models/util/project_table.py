#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_subquery_project_table(**kwargs):
    # DEFAULT WHERE
    # by default, get all results that are visible (that exist)
    conditions_of_where = ["project.visible=TRUE"]

    # SUBQUERY
    if "project_id" in kwargs and kwargs["project_id"] is not None:
        conditions_of_where.append("project.id = {0}".format(kwargs["project_id"]))

        where_project_table = "WHERE " + " AND ".join(conditions_of_where)

        subquery_project_table = """
            (
                SELECT id, create_at, removed_at, fk_user_id_owner FROM project {0}
            ) AS project
        """.format(where_project_table)

    elif "user_id" in kwargs and kwargs["user_id"] is not None:
        conditions_of_where.append("project.fk_user_id_owner = {0}".format(kwargs["user_id"]))

        if "project_id" in kwargs and kwargs["project_id"] is not None:
            conditions_of_where.append("project.id = {0}".format(kwargs["project_id"]))

        where_project_table = "WHERE " + " AND ".join(conditions_of_where)

        subquery_project_table = """
            (
                SELECT id, create_at, removed_at, fk_user_id_owner FROM project {0} 
            ) AS project
        """.format(where_project_table)
    else:
        where_project_table = "WHERE " + " AND ".join(conditions_of_where)

        # default get all features
        subquery_project_table = """
            (
                SELECT id, create_at, removed_at, fk_user_id_owner FROM project {0}
            ) AS project
        """.format(where_project_table)

    return subquery_project_table
