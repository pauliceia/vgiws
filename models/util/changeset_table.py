#!/usr/bin/env python
# -*- coding: utf-8 -*-


def get_subquery_changeset_table(**kwargs):
    # DEFAULT WHERE
    # by default, get all results that are visible (that exist)
    conditions_of_where = ["changeset.visible=TRUE"]

    # conditions of WHERE CLAUSE
    if "changeset_id" in kwargs and kwargs["changeset_id"] is not None:
        conditions_of_where.append("changeset.id = {0}".format(kwargs["changeset_id"]))
    elif "layer_id" in kwargs and kwargs["layer_id"] is not None:
        conditions_of_where.append("changeset.fk_layer_id = {0}".format(kwargs["layer_id"]))
    elif "user_id" in kwargs and kwargs["user_id"] is not None:
        conditions_of_where.append("changeset.fk_user_id = {0}".format(kwargs["user_id"]))
    else:
        # default get all features, without where clause
        pass

    # extra conditions: open or closed changesets
    if "open" in kwargs and kwargs["open"] is not None:
        conditions_of_where.append("closed_at is NULL")
    elif "closed" in kwargs and kwargs["closed"] is not None:
        conditions_of_where.append("closed_at is not NULL")
    else:
        pass

    # default get all features, without where clause
    where_clause = ""

    # if there is some condition, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    subquery_table = """
        (
            SELECT id, create_at, closed_at, fk_layer_id, fk_user_id
            FROM changeset {0}
            ORDER BY id 
        ) AS changeset
    """.format(where_clause)

    return subquery_table
