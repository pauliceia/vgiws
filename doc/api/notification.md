## Notification


### GET /api/notification/?\<params>

This method gets notifications from DB. If you doesn't put any parameter, so will return all.
- Parameters:
    - notification_id (optional) (int): the id of a notification that is a positive integer not null (e.g. 1, 2, 3, ...).
    - user_id_creator (optional) (int): the id of a user that is a positive integer not null (e.g. 1, 2, 3, ...).
    - layer_id (optional) (int): the id of a user that is a positive integer or null (e.g. NULL, 1, 2, 3, ...).
    - keyword_id (optional) (int): the id of a user that is a positive integer or null (e.g. NULL, 1, 2, 3, ...).
    - notification_id_parent (optional) (int): the id of a user that is a positive integer or null (e.g. NULL, 1, 2, 3, ...).
- Examples:
     - Get all notifications: http://localhost:8888/api/notification/
     - Get one notification by id: http://localhost:8888/api/notification/?notification_id=1001
     - Get notifications by user id: http://localhost:8888/api/notification/?user_id_creator=1001
     - Get notifications by layer id: http://localhost:8888/api/notification/?layer_id=1001
     - Get notifications by keyword id: http://localhost:8888/api/notification/?keyword_id=1001
     - Get notifications by notification id parent: http://localhost:8888/api/notification/?notification_id_parent=1001
     - Get all general notifications: http://localhost:8888/api/notification/?layer_id=NULL&keyword_id=NULL&notification_id_parent=NULL
- Send:
- Response: a JSON that contain the features selected. Example:
    ```javascript
    {
        'features': [
            {
                'type': 'Notification',
                'properties': {'notification_id': 1011, 'is_denunciation': False, 'keyword_id': None,
                               'user_id_creator': 1003, 'notification_id_parent': 1010, 'layer_id': None,
                               'description': 'Obrigado pelo aviso.', 'created_at': '2017-03-01 00:00:00'}
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

<!--
### POST /api/notification/create

This method create a new notification described in a JSON.
- Parameters:
- Examples:
     - Create a feature: ```POST http://localhost:8888/api/notification/create```
- Send: a JSON describing the feature. Example:
    ```javascript
    {
        'properties': {'id': -1, 'fk_user_id': 1002},
        'type': 'Notification',
        'tags': {'body': 'You gained more points', 'type': 'point', 'url': ''}
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


<!- - PUT /api/notification/update - ->


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
-->