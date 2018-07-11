## Feature Table


### GET /api/feature_table/?\<params>

This method gets feature tables from DB. If you doesn't put any parameter, so it will return all.
- Parameters:
    - f_table_name (optional) (text): the feature table name (e.g. 'layer_X').
- Examples:
     - Get all feature tables: http://localhost:8888/api/feature_table/
     - Get one feature table by name: http://localhost:8888/api/feature_table/?f_table_name=layer
- Send (in Body):
- Send (in Header):
- Response: a JSON that contains the resources selected. Example:
    ```javascript
    {
        'features': [
            {
                'type': 'FeatureTable',
                'f_table_name': 'layer_1003',
                'properties': {'name': 'text', 'id': 'integer', 'end_date': 'timestamp without time zone',
                               'geom': 'geometry', 'version': 'integer', 'changeset_id': 'integer',
                               'start_date': 'timestamp without time zone'},
                'geometry': {
                    'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
                    'type': 'MULTILINESTRING'
                }
            }
        ],
        'type': 'FeatureCollection'
    }
    ```
- Error codes:
    - 404 (Not Found): Not found any resource.
    - 500 (Internal Server Error): Problem when get a resource. Please, contact the administrator.
- Notes:
