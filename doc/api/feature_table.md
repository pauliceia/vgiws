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


### POST /api/feature_table/create/

This method creates a new feature table described in a JSON.
- Parameters:
- Examples:
    - Create a feature table: ```POST http://localhost:8888/api/feature_table/create```
- Send (in Body): a JSON describing the resource. Example:
    ```javascript
    {
        'type': 'FeatureTable',
        'f_table_name': 'addresses',
        'properties': {'start_date': 'timestamp', 'end_date': 'timestamp',
                       'address': 'text', 'count': 'int'},
        'geometry': {
            'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326'}},
            'type': 'MULTIPOINT'
        }
    }
    ```
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
    - 400 (Bad Request): Some attribute in the JSON is missing. Look at the documentation!
    - 400 (Bad Request): f_table_name can not have special characters.
    - 400 (Bad Request): f_table_name can not start with number.
    - 400 (Bad Request): There is a field with have special characters. Please, rename it. (field: X)
    - 400 (Bad Request): There is a field that starts with number. Please, rename it. (field: X)
    - 400 (Bad Request): There is a field with white spaces. Please, rename it. (field: X)
    - 400 (Bad Request): There is a field that is a reserved word. Please, rename it. (field: X)
    - 401 (Unauthorized): A valid `Authorization` header is necessary!
    - 403 (Forbidden): The layer owner or administrator user are who can create or delete this resource.
    - 404 (Not Found): Not found any layer with the passed f_table_name. You need to create a layer with the f_table_name before of using this function.
    - 409 (Bad Request): Conflict of f_table_name. The table name is a reserved word. Please, rename it.
    - 500 (Internal Server Error): Problem when create a resource. Please, contact the administrator.
- Notes:


### DELETE

A feature table is removed automatically when a layer is deleted.


### POST /api/feature_table_column/create/

This method creates a new column in a feature table described in a JSON.
- Parameters:
- Examples:
    - Create a feature table: ```POST http://localhost:8888/api/feature_table_column/create```
- Send (in Body): a JSON describing the resource. Example:
    ```javascript
    {
        'type': 'FeatureTableColumn',
        'f_table_name': 'address',
        'column_name': 'name',
        'column_type': 'text',
    }
    ```
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
     - 400 (Bad Request): Some attribute in the JSON is missing. Look at the documentation!
     - 401 (Unauthorized): A valid `Authorization` header is necessary!
     - 403 (Forbidden): The layer owner or collaborator user, or administrator one are who can update this resource.
     - 404 (Not Found): Not found any layer with the passed f_table_name. You need to create a layer with the f_table_name before of using this function.
     - 500 (Internal Server Error): Problem when create a resource. Please, contact the administrator.
- Notes:


### DELETE /api/feature_table_column/?\<params>

This method deletes one column of a feature table.
- Parameters:
    - f_table_name (mandatory) (text): the feature table name (e.g. 'layer_X');
    - column_name (mandatory) (text): the column name of the feature table (e.g. 'name').
- Examples:
    - Delete a resource: ```DELETE http://localhost:8888/api/feature_table_column/?f_table_name=layer&column_name=name```
- Send (in Body):
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 401 (Unauthorized): A valid `Authorization` header is necessary!
    - 403 (Forbidden): The layer owner or collaborator user, or administrator one are who can update this resource.
    - 404 (Not Found): Not found any layer with the passed f_table_name. You need to create a layer with the f_table_name before of using this function.
    - 404 (Not Found): Not found the specified column.
    - 500 (Internal Server Error): Problem when delete a resource. Please, contact the administrator.
- Notes:
