
def get_subquery_reference_table(**kwargs):
    # DEFAULT WHERE
    conditions_of_where = []

    # conditions of WHERE CLAUSE
    if "id" in kwargs and kwargs["id"] is not None:
        conditions_of_where.append("reference_id = {0}".format(kwargs["id"]))

    if "user_id_creator" in kwargs and kwargs["user_id_creator"] is not None:
        conditions_of_where.append("user_id_creator = {0}".format(kwargs["user_id_creator"]))

    if "description" in kwargs and kwargs["description"] is not None:
        conditions_of_where.append("unaccent(LOWER(description)) LIKE '%' || unaccent(LOWER('{0}')) || '%'".format(kwargs["description"]))

    # default get all resources, without where clause
    where_clause = ""

    # if there is some conditions, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    # default get all resources, ordering by id
    subquery_table = f"""
        (
            SELECT * FROM reference {where_clause} ORDER BY reference_id
        ) AS reference
    """

    return subquery_table
