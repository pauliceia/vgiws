
def get_subquery_temporal_columns_table(**kwargs):
    # DEFAULT WHERE
    # by default, get all results
    conditions_of_where = []

    # conditions of WHERE CLAUSE
    if "f_table_name" in kwargs and kwargs["f_table_name"] is not None:
        conditions_of_where.append("unaccent(LOWER(f_table_name)) LIKE '%' || unaccent(LOWER('{0}')) || '%'".format(kwargs["f_table_name"]))

    if "start_date" in kwargs and kwargs["start_date"] is not None:
        conditions_of_where.append("start_date::date = '{0}'".format(kwargs["start_date"]))

    if "end_date" in kwargs and kwargs["end_date"] is not None:
        conditions_of_where.append("end_date::date = '{0}'".format(kwargs["end_date"]))

    if "start_date_gte" in kwargs and kwargs["start_date_gte"] is not None:
        conditions_of_where.append("start_date::date >= '{0}'".format(kwargs["start_date_gte"]))

    if "end_date_lte" in kwargs and kwargs["end_date_lte"] is not None:
        conditions_of_where.append("end_date::date <= '{0}'".format(kwargs["end_date_lte"]))

    # default get all features, without where clause
    where_clause = ""

    # if there is some conditions, put in where_clause
    if conditions_of_where:
        where_clause = "WHERE " + " AND ".join(conditions_of_where)

    # default get all features
    subquery_table = f"""
        (
            SELECT tc.*, m1.mask as start_date_mask, m2.mask as end_date_mask
            FROM temporal_columns tc
            LEFT JOIN mask m1
                ON tc.start_date_mask_id = m1.mask_id
            LEFT JOIN mask m2
                ON tc.end_date_mask_id = m2.mask_id
            {where_clause}
            ORDER BY tc.f_table_name
        ) AS tc
    """

    return subquery_table
