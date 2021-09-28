
def get_subquery_changeset_table(**kwargs):
    # DEFAULT WHERE
    # by default, get all results
    conditions_of_where = []

    # conditions of WHERE CLAUSE
    if "id" in kwargs and kwargs["id"] is not None:
        conditions_of_where.append("changeset_id = {0}".format(kwargs["id"]))
    if "layer_id" in kwargs and kwargs["layer_id"] is not None:
        conditions_of_where.append("layer_id = {0}".format(kwargs["layer_id"]))
    if "user_id_creator" in kwargs and kwargs["user_id_creator"] is not None:
        conditions_of_where.append("user_id_creator = {0}".format(kwargs["user_id_creator"]))

    # extra conditions: open or closed changesets
    if "open" in kwargs and kwargs["open"] is not None:
        conditions_of_where.append("closed_at is NULL")
    if "closed" in kwargs and kwargs["closed"] is not None:
        conditions_of_where.append("closed_at is not NULL")

    # default get all features, without where clause
    where_clause = ""

    # if there is some condition, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    subquery_table = f"""
        (
            SELECT * FROM changeset {where_clause} ORDER BY changeset_id
        ) AS changeset
    """

    return subquery_table
