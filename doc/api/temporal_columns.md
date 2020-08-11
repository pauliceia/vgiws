## Time Columns


### GET /api/temporal_columns/?\<params>

This method gets temporal columns from DB. If you doesn't put any parameter, so it will return all.
- Parameters:
    - f_table_name (optional) (text): the feature table name (e.g. 'layer_1003');
    - start_date (optional) (text): the start date (e.g. '1890-01-01');
    - end_date (optional) (text): the end_date (e.g. '1920-12-31');
    - start_date_gte (optional) (text): it will search by greater than or equal the start date (e.g. '1890-01-01');
    - end_date_lte (optional) (text): it will search by less than or equal the end date (e.g. '1920-12-31').
- Examples:
     - Get all temporal columns: http://localhost:8888/api/temporal_columns/
     - Get time columns by f_table_name: http://localhost:8888/api/temporal_columns/?f_table_name=layer_1003
     - Get time columns by start_date: http://localhost:8888/api/temporal_columns/?start_date=1890-01-01
     - Get time columns by end_date: http://localhost:8888/api/temporal_columns/?end_date=1920-12-31
     - Get time columns by start_date_gte: http://localhost:8888/api/temporal_columns/?start_date_gte=1890-01-01
     - Get time columns by end_date_lte: http://localhost:8888/api/temporal_columns/?end_date_lte=1920-12-31
     - Get time columns by temporal bounding box with start_date_gte and end_date_lte: http://localhost:8888/api/temporal_columns/?start_date_gte=1890-01-01&end_date_lte=1920-12-31
- Send (in Body):
- Send (in Header):
- Response: a JSON that contains the resources selected. Example:
    ```javascript
    {
        'features': [
            {
                'properties': {'f_table_name': 'layer_1003', 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                               'end_date_column_name': 'end_date', 'start_date_column_name': 'start_date'},
                               'start_date_type': 'timestamp', 'end_date_type': 'timestamp',
                               'start_date_mask_id': 1001, 'end_date_mask_id': 1001
                'type': 'TemporalColumns'
            },
        ],
        'type': 'FeatureCollection'
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid date format.
    - 500 (Internal Server Error): Problem when get a resource. Please, contact the administrator.
- Notes:


### POST /api/temporal_columns/create

This method creates a new record in time columns table described in a JSON.
- Parameters:
- Examples:
    - Create a time columns: ```POST http://localhost:8888/api/temporal_columns/create```
- Send (in Body): a JSON describing the resource. Example:
    ```javascript
    {
        'properties': {'f_table_name': 'addresses', 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                       'end_date_column_name': 'end_date', 'start_date_column_name': 'start_date'},
        'type': 'TemporalColumns'
    }
    ```
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
    - 400 (Bad Request): Attribute already exists.
    - 400 (Bad Request): Some attribute in the JSON is missing. Look at the documentation!
    - 400 (Bad Request): f_table_name can not have special characters.
    - 400 (Bad Request): f_table_name can not start with number.
    - 401 (Unauthorized): A valid `Authorization` header is necessary!
    - 403 (Forbidden): The layer owner or administrator user are who can create or delete this resource.
    - 404 (Not Found): Not found any layer with the passed f_table_name. You need to create a layer with the f_table_name before of using this function.
    - 409 (Bad Request): Conflict of f_table_name. The table name is a reserved word. Please, rename it.
    - 500 (Internal Server Error): Problem when create a resource. Please, contact the administrator.
- Notes:


### PUT /api/temporal_columns

This method updates a record in time columns table described in a JSON.
- Parameters:
- Examples:
    - Create a time columns: ```PUT http://localhost:8888/api/temporal_columns```
- Send (in Body): a JSON describing the resource. Example:
    ```javascript
    {
        'properties': {'f_table_name': 'addresses', 'start_date': '1900-01-01', 'end_date': '1920-12-31',
                       'end_date_column_name': 'end_date', 'start_date_column_name': 'start_date'},
        'type': 'TemporalColumns'
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


### DELETE

A temporal column is removed automatically when the layer is deleted.
