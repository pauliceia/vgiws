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
                'type': 'Layer',
                'tags': {'created_by': 'escolástica', 'name': 'Robberies on 1930',
                         'description': '', 'start_date': '1930/01/01',
                         'end_date': '1930/12/31', 'theme': 'robbery'},
                'properties': {'removed_at': None, 'fk_user_id': 1002,
                               'id': 1001, 'created_at': '2017-10-20 00:00:00'}
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
        'tags': {'created_by': 'agostinho', 'name': 'layer of theathers',
                 'description': 'theathers on 1930', 'start_date': '1930/01/01',
                 'end_date': '1930/12/31', 'theme': 'theather'},
        'properties': {'id': -1},
        'type': 'Layer'
    }
    ```
- Response: a JSON that contains the id of the resource created. Example:
    ```javascript
    {'id': 7}
    ```
- Error codes:
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
    - 404 (Not Found): Not found any resource.
    - 500 (Internal Server Error): Problem when delete a resource. Please, contact the administrator.
- Notes:
