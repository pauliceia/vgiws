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
- Response: a JSON that contain the features selected. Example:
    ```javascript
    {
        'features': [
            {
                'type': 'Layer',
                'tags': [{'k': 'created_by', 'v': 'escolástica'},
                         {'k': 'name', 'v': 'Robberies on 1930'},
                         {'k': 'description', 'v': ''},
                         {'k': 'start_date', 'v': '1930/01/01'},
                         {'k': 'end_date', 'v': '1930/12/31'},
                         {'k': 'theme', 'v': 'robbery'}],
                'properties': {'removed_at': None, 'fk_user_id': 1002,
                               'id': 1001, 'created_at': '2017-10-20 00:00:00'}
            }
        ],
        'type': 'FeatureCollection'
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 404 (Not Found): Not found any feature.
    - 500 (Internal Server Error): Problem when get a feature. Please, contact the administrator.
- Notes:


### PUT /api/layer/create

This method create a new layer described in a JSON.
- Parameters:
- Examples:
     - Create a feature: ```PUT http://localhost:8888/api/layer/create```
- Send: a JSON describing the feature. Example:
    ```javascript
    {
        'tags': [{'k': 'created_by', 'v': 'agostinho'},
                 {'k': 'name', 'v': 'layer of theathers'},
                 {'k': 'description', 'v': 'theathers on 1930'},
                 {'k': 'start_date', 'v': '1930/01/01'},
                 {'k': 'end_date', 'v': '1930/12/31'},
                 {'k': 'theme', 'v': 'theather'}],
        'properties': {'id': -1},
        'type': 'Layer'
    }
    ```
- Response: a JSON that contain the id of the feature created. Example:
    ```javascript
    {'id': 7}
    ```
- Error codes:
    - 403 (Forbidden): It is necessary a user logged in to access this URL.
    - 500 (Internal Server Error): Problem when create a feature. Please, contact the administrator.
- Notes: The key "id", when send a JSON, is indifferent. It is just there to know where the key "id" have to be.


<!-- - PUT /api/layer/update -->


### DELETE /api/layer/delete/#id

This method delete one layer by id = #id.
- Parameters:
    - #id (mandatory): the id of the feature that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Delete a feature by id: ```DELETE http://localhost:8888/api/layer/7```
- Send:
- Response:
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 403 (Forbidden): It is necessary a user logged in to access this URL.
    - 404 (Not Found): Not found any feature.
    - 500 (Internal Server Error): Problem when delete a feature. Please, contact the administrator.
- Notes:
