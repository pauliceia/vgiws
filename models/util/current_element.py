#!/usr/bin/env python
# -*- coding: utf-8 -*-


__select_elements__ = "element.id, element.geom, element.visible, element.version, element.fk_changeset_id, element.tags"


def get_subquery_current_element_table_if_user_id_is_not_none(element, conditions_of_where, **kwargs):

    # create the where clause with the conditions
    where_current_element_table = "WHERE " + " AND ".join(conditions_of_where)

    # by default, get all elements from a specific user
    conditions_of_where = ["user_.id = {0}".format(kwargs["user_id"])]

    # create the where clause with the conditions
    where_join_user_with_changeset = "WHERE " + " AND ".join(conditions_of_where)

    # search by project_id
    current_element_table = """
            (
                -- get the elements of the changesets of a specific user
                SELECT {0}
                FROM 
                (
                    -- get the changesets of a specific project
                    SELECT changeset.id
                    FROM user_ LEFT JOIN changeset ON user_.id = changeset.fk_user_id
                    {3}
                ) AS changeset
                LEFT JOIN current_{1} element ON changeset.id = element.fk_changeset_id
                {2}
                ORDER BY id
            ) AS element
        """.format(__select_elements__, element, where_current_element_table, where_join_user_with_changeset)

    return current_element_table


def get_subquery_current_element_table_if_layer_id_is_not_none(element, conditions_of_where, **kwargs):

    # create the where clause with the conditions
    where_current_element_table = "WHERE " + " AND ".join(conditions_of_where)

    # by default, get all elements from a specific layer
    conditions_of_where = ["layer.id = {0}".format(kwargs["layer_id"])]

    # create the where clause with the conditions
    where_join_layer_with_changeset = "WHERE " + " AND ".join(conditions_of_where)

    # search by layer_id
    current_element_table = """
        (
            -- get the elements of the changesets of a specific layer
            SELECT {0}
            FROM 
            (
                -- get the changesets of a specific layer
                SELECT changeset.id
                FROM layer LEFT JOIN changeset ON layer.id = changeset.fk_layer_id
                {3}
            ) AS changeset
            LEFT JOIN current_{1} element ON changeset.id = element.fk_changeset_id
            {2}
            ORDER BY id
        ) AS element
    """.format(__select_elements__, element, where_current_element_table, where_join_layer_with_changeset)

    return current_element_table


def get_subquery_current_element_table_if_changeset_id_is_not_none(element, conditions_of_where, **kwargs):

    # add the id of changeset in WHERE
    conditions_of_where.append("changeset.id = {0}".format(kwargs["changeset_id"]))
    # create the where clause with the conditions
    where_current_element_table = "WHERE " + " AND ".join(conditions_of_where)

    # search by changeset_id
    current_element_table = """
        (
            SELECT {0} 
            FROM current_{1} element LEFT JOIN changeset ON element.fk_changeset_id = changeset.id
            {2}
            ORDER BY id
        ) AS element
    """.format(__select_elements__, element, where_current_element_table)

    return current_element_table


def get_subquery_current_element_table_default(element, conditions_of_where, **kwargs):
    # create the where clause with the conditions
    where_current_element_table = "WHERE " + " AND ".join(conditions_of_where)

    # default subquery, get all elements
    current_element_table = """
        (
            SELECT {0}
            FROM current_{1} element
            {2}
            ORDER BY id
        ) AS element
    """.format(__select_elements__, element, where_current_element_table)

    return current_element_table


# main function

def get_subquery_current_element_table(element, **kwargs):
    # DEFAULT WHERE
    # by default, get all results that are visible (that exist)
    conditions_of_where = ["element.visible=TRUE"]

    # SUBQUERY
    # create a subquery to get the elements, by a type:
    if "element_id" in kwargs and kwargs["element_id"] is not None:
        conditions_of_where.append("element.id = {0}".format(kwargs["element_id"]))
        current_element_table = get_subquery_current_element_table_default(element, conditions_of_where, **kwargs)

    elif "user_id" in kwargs and kwargs["user_id"] is not None:
        # if there is a layer_id
        current_element_table = get_subquery_current_element_table_if_user_id_is_not_none(element,
                                                                                          conditions_of_where,
                                                                                          **kwargs)

    elif "layer_id" in kwargs and kwargs["layer_id"] is not None:
        # if there is a layer_id
        current_element_table = get_subquery_current_element_table_if_layer_id_is_not_none(element,
                                                                                           conditions_of_where,
                                                                                           **kwargs)

    elif "changeset_id" in kwargs and kwargs["changeset_id"] is not None:
        # if there is a changeset_id
        current_element_table = get_subquery_current_element_table_if_changeset_id_is_not_none(element,
                                                                                               conditions_of_where,
                                                                                               **kwargs)
    else:
        # default
        current_element_table = get_subquery_current_element_table_default(element, conditions_of_where, **kwargs)

    return current_element_table
