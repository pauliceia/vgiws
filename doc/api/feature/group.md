## Group

A group is a set of users that work in projects. All projects have to be associated with a group.


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
                'properties': {'fk_user_id': 1002, 'created_at': '2017-12-25 00:00:00',
                               'removed_at': None, 'id': 1003, 'visible': True},
                'tags': {'name': 'UNIFESP SJC', 'description': ''}
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
        'tags': {'name': 'VS', 'description': 'group of my institution',
                'visibility': 'public'}
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


### PUT /api/group/update

This method update a group described in a JSON.
- Parameters:
- Examples:
     - Create a feature: ```PUT http://localhost:8888/api/group/update```
- Send: a JSON describing the feature. Example:
    ```javascript
    {
        'type': 'Group',
        'properties': {'id': 1003, 'fk_user_id': 1002},
        'tags': {'name': 'UNIFESP SJC', 'description': 'group of UNIFESP SJC',
                'visibility': 'private'}
    }
    ```
- Response:
- Error codes:
    - 403 (Forbidden): It is necessary a user logged in to access this URL.
    - 500 (Internal Server Error): Problem when update a feature. Please, contact the administrator.


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


### GET /api/user_group/?\<params>

This method gets users in groups from DB. If you doesn't put any parameter, so will return all.
- Parameters:
    - group_id (optional): the id of a group that is a positive integer not null (e.g. 1, 2, 3, ...).
    - user_id (optional): the id of a user that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Get all users in groups: http://localhost:8888/api/user_group/
     - Get users by group id: http://localhost:8888/api/user_group/?group_id=1001
     - Get groups by user id: http://localhost:8888/api/user_group/?user_id=1001
- Send:
- Response: a JSON that contain the features selected. Example:
    ```javascript
    {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'UserGroup',
                'properties': {'added_at': '2017-01-01 00:00:00', 'fk_user_id': 1001,
                               'group_permission': 'admin', 'fk_group_id': 1001,
                               'can_receive_notification': True, 'fk_user_id_added_by': 1001,
                               'group_status': 'joined'}
            }
        ]
    }
    ```
- Error codes:
     - 400 (Bad Request): Invalid parameter.
     - 404 (Not Found): Not found any feature.
     - 500 (Internal Server Error): Problem when get a feature. Please, contact the administrator.
- Notes:


### PUT /api/user_group/create

This method put a user in a group described in a JSON.
- Parameters:
- Examples:
     - Create a feature: ```PUT http://localhost:8888/api/user_group/create```
- Send: a JSON describing the feature. Example:
    ```javascript
    {
        'type': 'UserGroup',
        'properties': {'fk_user_id': 1004, 'fk_group_id': 1003,
                       'can_receive_notification': True, 'fk_user_id_added_by': 1002}
    }
    ```
- Response:
- Error codes:
    - 400 (Bad Request): The user_id is already added in group_id.
    - 403 (Forbidden): It is necessary a user logged in to access this URL.
    - 500 (Internal Server Error): Problem when create a feature. Please, contact the administrator.
- Notes:



<!-- PUT /api/user_group/update -->


### DELETE /api/user_group/delete/?user_id=#user_id&group_id=#group_id

This method delete one user with id = #user_id from a group with id = #group_id.
- Parameters:
    - #user_id (mandatory): the id of the user that is a positive integer not null (e.g. 1, 2, 3, ...).
    - #group_id (mandatory): the id of the group that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Delete a user from a group: ```DELETE http://localhost:8888/api/user_group/?user_id=1001&group_id=1001```
- Send:
- Response:
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 403 (Forbidden): It is necessary a user logged in to access this URL.
    - 404 (Not Found): Not found any feature.
    - 500 (Internal Server Error): Problem when delete a feature. Please, contact the administrator.
- Notes:

