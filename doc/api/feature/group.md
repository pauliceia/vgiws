## Group

A group is a set of projects. All projects have to be associated with a group.


### GET /api/group/?\<params>

This method gets groups from DB. If you doesn't put any parameter, so will return all.
- Parameters:
    - group_id (optional): the id of a group that is a positive integer not null (e.g. 1, 2, 3, ...).
    - user_id (optional): the id of a user that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Get all groups: http://localhost:8888/api/group/
     - Get one group by id: http://localhost:8888/api/group/?group_id=1001
     - Get groups by user id: http://localhost:8888/api/group/?user_id=1001
- Send:
- Response: a JSON that contain the features selected. Example:
    ```javascript
    {
        'features': [
            {
                'type': 'Group',
                'properties': {'fk_user_id': 1002, 'create_at': '2017-12-25 00:00:00',
                               'removed_at': None, 'id': 1003, 'visible': True},
                'tags': [{'v': '', 'k': 'description'}, {'v': 'UNIFESP SJC', 'k': 'name'}]
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


### PUT /api/group/create

This method create a new group described in a JSON.
- Parameters:
- Examples:
     - Create a feature: ```PUT http://localhost:8888/api/group/create```
- Send: a JSON describing the feature. Example:
    ```javascript
    {
        'type': 'Group',
        'properties': {'id': -1, 'fk_user_id': 1002},
        'tags': [{'k': 'description', 'v': 'group of my institution'},
                 {'k': 'name', 'v': 'VS'}]
    }
    ```
- Response: a JSON that contain the id of the feature created. Example:
    ```javascript
    {'id': 10}
    ```
- Error codes:
    - 403 (Forbidden): It is necessary a user logged in to access this URL.
    - 500 (Internal Server Error): Problem when create a feature. Please, contact the administrator.
- Notes: The key "id", when send a JSON, is indifferent. It is just there to know where the key "id" have to be.


<!-- PUT /api/group/update -->


### DELETE /api/group/delete/#id

This method delete one group by id = #id.
- Parameters:
    - #id (mandatory): the id of the feature that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Delete a feature by id: ```DELETE http://localhost:8888/api/group/7```
- Send:
- Response:
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 403 (Forbidden): It is necessary a user logged in to access this URL.
    - 404 (Not Found): Not found any feature.
    - 500 (Internal Server Error): Problem when delete a feature. Please, contact the administrator.
- Notes:
