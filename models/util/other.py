
def get_subquery_mask_table(**kwargs):
    # DEFAULT WHERE
    conditions_of_where = []

    # conditions of WHERE CLAUSE
    if "id" in kwargs and kwargs["id"] is not None:
        conditions_of_where.append("mask_id = {0}".format(kwargs["id"]))

    # default get all resources, without where clause
    where_clause = ""

    # if there is some conditions, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    # default get all resources, ordering by id
    subquery_table = f"""
        (
            SELECT mask_id as id, mask FROM mask {where_clause} ORDER BY mask_id
        ) AS mask
    """

    return subquery_table
