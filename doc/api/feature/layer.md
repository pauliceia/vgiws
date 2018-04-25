## Layer

A layer is a group of elements. All elements have to be associated with a layer.


### GET /api/layer/?\<params>

This method gets layers from DB. If you doesn't put any parameter, so will return all.
- Parameters:
    - layer_id (optional): the id of a layer that is a positive integer not null (e.g. 1, 2, 3, ...).
    - user_id (optional): the id of a user that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Get all layers: http://localhost:8888/api/layer/
     - Get one layer by id: http://localhost:8888/api/layer/?layer_id=1001
     - Get layers by user id: http://localhost:8888/api/layer/?user_id=1001
- Send:
- Response: a JSON that contains the resources selected. Example:
    ```javascript
    {
        'features': [
            {
                'properties': {
                    'fk_user_id_published_by': 1003, 'source_author_name': '', 'table_name': '_1003_layer_1002',
                    'created_at': '2017-03-05 00:00:00', 'reference': [{'description': 'http://link_to_document',
                                                                        'id': 1005}],
                    'removed_at': None, 'fk_user_id_author': 1003, 'description': '', 'is_published': True,
                    'id': 1002, 'name': 'Robberies between 1880 to 1900'
                },
                'type': 'Layer'
            }
        ],
        'type': 'FeatureCollection'
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 404 (Not Found): Not found any resource.
    - 500 (Internal Server Error): Problem when get a resource. Please, contact the administrator.
- Notes:


### PUT /api/layer/create

This method create a new layer described in a JSON.
- Parameters:
- Examples:
     - Create a resource: ```PUT http://localhost:8888/api/layer/create```
- Send: a JSON describing the resource. Example:
    ```javascript
    {
        'type': 'Layer',
        'properties': {'name': 'Addresses in 1930', 'table_name': '_1_new_layer',
                       'reference': [], 'description': '', 'fk_theme_id': 1041,
                       'id': -1},
        'feature_table': {
            'properties': {'name': 'text', 'start_date': 'text', 'end_date': 'text'},
            'geometry': {"type": "MultiPoint"}
        }
    }

    ```
- Response: a JSON that contains the id of the resource created. Example:
    ```javascript
    {'id': 7}
    ```
- Error codes:
    - 400 (Bad Request): Table name already exists.
    - 400 (Bad Request): The parameter source needs to be a list.
    - 403 (Forbidden): It is necessary a user logged in to access this URL.
    - 500 (Internal Server Error): Problem when create a resource. Please, contact the administrator.
- Notes: The key "id", when send a JSON, is indifferent. It is just there to know where the key "id" have to be.


<!-- - PUT /api/layer/update -->


### DELETE /api/layer/delete/#id

This method delete one layer by id = #id.
- Parameters:
    - #id (mandatory): the id of the resource that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Delete a resource by id: ```DELETE http://localhost:8888/api/layer/7```
- Send:
- Response:
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 403 (Forbidden): It is necessary a user logged in to access this URL.
    - 403 (Forbidden): The owner of the layer is the unique who can delete the layer.
    - 404 (Not Found): Not found any resource.
    - 500 (Internal Server Error): Problem when delete a resource. Please, contact the administrator.
- Notes:
