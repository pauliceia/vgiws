## User


### GET /api/user/?\<params>

This method gets users from DB. If you doesn't put any parameter, so will return all.
- Parameters:
    - user_id (optional): the id of a user that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Get all users: http://localhost:8888/api/user/
     - Get one user by id: http://localhost:8888/api/user/?user_id=1002
- Send:
- Response: a JSON that contain the features selected. Example:
    ```javascript
    {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'User',
                'tags': {'institution': 'INPE'},
                'properties': {'id': 1002, 'is_email_valid': None, 'created_at': None, 'terms_agreed': None,
                               'description': None, 'email': 'rodrigo@admin.com', 'name': 'Rodrigo',
                               'terms_seen': None, 'removed_at': None, 'username': 'rodrigo'}
            }
        ]
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 404 (Not Found): Not found any feature.
    - 500 (Internal Server Error): Problem when get a user. Please, contact the administrator.
- Notes:


### PUT /api/user/create

This method create a new user described in a JSON.
- Parameters:
- Examples:
     - Create a feature: ```PUT http://localhost:8888/api/user/create```
- Send: a JSON describing the feature. Example:
    ```javascript
    {
        'type': 'User',
        'tags': {},
        'properties': {'id': -1, 'email': 'roger@roger.com',
                       'password': 'roger', 'username': ''}
    }
    ```
- Response: a JSON that contain the id of the feature created. Example:
    ```javascript
    {'id': 7}
    ```
- Error codes:
    - 500 (Internal Server Error): Problem when create a feature. Please, contact the administrator.
- Notes: The key "id", when send a JSON, is indifferent. It is just there to know where the key "id" have to be.


<!-- - PUT /api/user/update -->


### DELETE /api/user/delete/#id

This method delete one user by id = #id.
- Parameters:
    - #id (mandatory): the id of the feature that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Delete a feature by id: ```DELETE http://localhost:8888/api/user/7```
- Send:
- Response:
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 403 (Forbidden): It is necessary a user logged in to access this URL.
    - 404 (Not Found): Not found any feature.
    - 500 (Internal Server Error): Problem when delete a feature. Please, contact the administrator.
- Notes:
