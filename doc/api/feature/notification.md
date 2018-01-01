## Notification

A notification is a list of notice.


### GET /api/notification/?\<params>

This method gets notifications from DB. If you doesn't put any parameter, so will return all.
- Parameters:
    - notification_id (optional): the id of a notification that is a positive integer not null (e.g. 1, 2, 3, ...).
    - user_id (optional): the id of a user that is a positive integer not null (e.g. 1, 2, 3, ...).
    - is_read (optional): a boolean indicating if the notification was read or not (e.g. True or False).
- Examples:
     - Get all notifications: http://localhost:8888/api/notification/
     - Get one notification by id: http://localhost:8888/api/notification/?notification_id=1001
     - Get notifications by user id: http://localhost:8888/api/notification/?user_id=1001
     - Get notifications by user id, but just the notification that was not read yet: http://localhost:8888/api/notification/?user_id=1001&is_read=False
- Send:
- Response: a JSON that contain the features selected. Example:
    ```javascript
    {
        'features': [
            {
                'properties': {'is_read': False, 'removed_at': None, 'visible': True, 'id': 1002,
                               'created_at': '2017-03-25 00:00:00', 'fk_user_id': 1001},
                'type': 'Notification',
                'tags': [{'k': 'body', 'v': 'You was added in a group called X'},
                         {'k': 'type', 'v': 'group'},
                         {'k': 'url', 'v': ''}]
            },
        ],
        'type': 'FeatureCollection'
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 404 (Not Found): Not found any feature.
    - 500 (Internal Server Error): Problem when get a feature. Please, contact the administrator.
- Notes:


### PUT /api/notification/create

This method create a new notification described in a JSON.
- Parameters:
- Examples:
     - Create a feature: ```PUT http://localhost:8888/api/notification/create```
- Send: a JSON describing the feature. Example:
    ```javascript
    {
        'properties': {'id': -1, 'fk_user_id': 1002},
        'type': 'Notification',
        'tags': [{'k': 'body', 'v': 'You gained more points'},
                 {'k': 'type', 'v': 'point'},
                 {'k': 'url', 'v': ''}]
    }
    ```
- Response: a JSON that contain the id of the feature created. Example:
    ```javascript
    {'id': 10}
    ```
- Error codes:
    - 403 (Forbidden): It is necessary a user logged in to access this URL.
    - 500 (Internal Server Error): Problem when create a feature. Please, contact the administrator.
- Notes:
    - Follow the rules of Notification's attributes in its section in [Dynamic Attribute](dynamic_attribute.md) page.
    - The key "id", when send a JSON, is indifferent. It is just there to know where the key "id" have to be.


<!-- PUT /api/notification/update -->


### DELETE /api/notification/delete/#id

This method delete one notification by id = #id.
- Parameters:
    - #id (mandatory): the id of the feature that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Delete a feature by id: ```DELETE http://localhost:8888/api/notification/7```
- Send:
- Response:
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 403 (Forbidden): It is necessary a user logged in to access this URL.
    - 404 (Not Found): Not found any feature.
    - 500 (Internal Server Error): Problem when delete a feature. Please, contact the administrator.
- Notes:
