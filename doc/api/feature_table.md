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
     - 400 (Bad Request): Some attribute in JSON is missing. Look the documentation!
     - 401 (Unauthorized): It is necessary an Authorization header valid.
     - 403 (Forbidden): Just the owner of the layer or administrator can create/update a resource.
     - 404 (Not Found): Not found any layer with the passed f_table_name. It is needed to create a layer with the f_table_name before of using this function.
     - 500 (Internal Server Error): Problem when create a resource. Please, contact the administrator.
- Notes:


### DELETE

A feature table is automatically removed when a layer is deleted.


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
     - 400 (Bad Request): Some attribute in JSON is missing. Look the documentation!
     - 401 (Unauthorized): It is necessary an Authorization header valid.
     - 403 (Forbidden): Just the owner of the layer or administrator can create/update a resource.
     - 404 (Not Found): Not found any layer with the passed f_table_name. It is needed to create a layer with the f_table_name before of using this function.
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
    - 401 (Unauthorized): It is necessary an Authorization header valid.
    - 403 (Forbidden): Just the owner of the layer or administrator can create/update a resource.
    - 404 (Not Found): Not found any layer with the passed f_table_name. It is needed to create a layer with the f_table_name before of using this function.
    - 404 (Not Found): Not found the specified column.
    - 500 (Internal Server Error): Problem when delete a resource. Please, contact the administrator.
- Notes:
