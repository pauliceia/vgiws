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
                'tags': [{'v': 'INPE', 'k': 'institution'}],
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
