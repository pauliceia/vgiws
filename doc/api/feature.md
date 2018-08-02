## Feature


### GET /api/feature/?\<params>

This method gets features from DB. If you doesn't put any parameter, so it will return all.
- Parameters:
    - f_table_name (mandatory) (text): which feature table is searching (e.g 'layer_1001');
    - feature_id (optional) (int): the id of a feature that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Get all features by f_table_name: http://localhost:8888/api/feature/?f_table_name=layer_1001
     - Get one feature by id: http://localhost:8888/api/feature/?f_table_name=layer_1001&feature_id=1001
- Send (in Body):
- Send (in Header):
- Response: a JSON that contains the resources selected. Example:
    ```javascript
    {
        'features': [
            {
                'properties': {'end_date': '1869-12-31T00:00:00', 'version': 1, 'address': 'R. São José',
                               'id': 1001, 'start_date': '1869-01-01T00:00:00', 'changeset_id': 1001},
                'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
                'type': 'Feature'
            }
        ],
        'type': 'FeatureCollection'
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 400 (Bad Request): Some attribute is missing. Look the documentation!
    - 404 (Not Found): Not found any resource.
    - 500 (Internal Server Error): Problem when get a resource. Please, contact the administrator.
- Notes:


### POST /api/feature/create/

This method creates a new feature described in a JSON.
- Parameters:
- Examples:
    - Create a feature: ```POST http://localhost:8888/api/feature/create```
- Send (in Body): a JSON describing the resource. Example:
    ```javascript
    {
        'f_table_name': 'layer_1001',
        'properties': {'id': -1, 'start_date': '1870-01-01', 'end_date': '1870-12-31',
                       'address': 'R. São José', 'changeset_id': 1},
        'geometry': {'coordinates': [[-46.6375790530164, -23.5290461960682]], 'type': 'MultiPoint'},
        'type': 'Feature'
    }
    ```
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response: a JSON that contains the id of the resource created. Example:
    ```javascript
    {'id': 10}
    ```
- Error codes:
     - 400 (Bad Request): Some attribute in JSON is missing. Look the feature table structure!
     - 401 (Unauthorized): It is necessary an Authorization header valid.
     - 500 (Internal Server Error): Problem when create a resource. Please, contact the administrator.
- Notes:
    - The key "id", when send a JSON, is indifferent. It is just there to know where the key "id" have to be.
    - The system just accept "MULTI" geometries, like: MultiPoint, MultiLineString and MultiPolygon.

<!--
### PUT /api/feature

This method updates a feature described in a JSON.
- Parameters:
- Examples:
    - Update a feature: ```PUT http://localhost:8888/api/feature```
- Send (in Body): a JSON describing the resource. Example:
    ```javascript
    {
        'type': 'feature',
        'properties': {'feature_id': 1001, 'description': 'ArticleA'}
    }
    ```
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
     - 400 (Bad Request): Some attribute in JSON is missing. Look the documentation!
     - 401 (Unauthorized): It is necessary an Authorization header valid.
     - 403 (Forbidden): The creator of the feature and the administrator are who can update/delete the feature.
     - 404 (Not Found): Not found any resource.
     - 500 (Internal Server Error): Problem when update a resource. Please, contact the administrator.
- Notes:
-->

### DELETE /api/feature/?\<params>

This method deletes one feature by id.
- Parameters:
    - f_table_name (mandatory) (text): which feature table is searching (e.g 'layer_1001');
    - feature_id (mandatory) (int): the id of a feature that is a positive integer not null (e.g. 1, 2, 3, ...).
    - changeset_id (mandatory) (int): the id of a changeset that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Delete a resource by id: ```DELETE http://localhost:8888/api/feature/?f_table_name=layer_1001&feature_id=1001&changeset_id=1001```
- Send (in Body):
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
     - 400 (Bad Request): Invalid parameter.
     - 401 (Unauthorized): It is necessary an Authorization header valid.
     - 403 (Forbidden): The creator of the feature and the administrator are who can update/delete the feature.
     - 404 (Not Found): Not found any resource.
     - 500 (Internal Server Error): Problem when delete a resource. Please, contact the administrator.
- Notes:
