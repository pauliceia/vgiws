## Notification


### GET /api/notification/?\<params>

This method gets notifications from DB. If you doesn't put any parameter, so will return all.
- Parameters:
    - notification_id (optional) (int): the id of a notification that is a positive integer not null (e.g. 1, 2, 3, ...);
    - user_id_creator (optional) (int): the id of a user that is a positive integer not null (e.g. 1, 2, 3, ...);
    - layer_id (optional) (int): the id of a user that is a positive integer or null (e.g. NULL, 1, 2, 3, ...);
    - keyword_id (optional) (int): the id of a user that is a positive integer or null (e.g. NULL, 1, 2, 3, ...);
    - notification_id_parent (optional) (int): the id of a user that is a positive integer or null (e.g. NULL, 1, 2, 3, ...);
    - is_denunciation (optional) (boolean): a flag that indicates if the notification is a denunciation or not (e.g. True or False).
- Examples:
     - Get all notifications: http://localhost:8888/api/notification/
     - Get one notification by id: http://localhost:8888/api/notification/?notification_id=1001
     - Get notifications by user id: http://localhost:8888/api/notification/?user_id_creator=1001
     - Get notifications by layer id: http://localhost:8888/api/notification/?layer_id=1001
     - Get notifications by keyword id: http://localhost:8888/api/notification/?keyword_id=1001
     - Get notifications by notification id parent: http://localhost:8888/api/notification/?notification_id_parent=1001
     - Get denunciations: http://localhost:8888/api/notification/?is_denunciation=True
     - Don't get denunciations: http://localhost:8888/api/notification/?is_denunciation=False
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
    - 500 (Internal Server Error): Problem when get a feature. Please, contact the administrator.
- Notes:


### POST /api/notification/create/

This method creates a new notification described in a JSON.
- Parameters:
- Examples:
    - Create a notification: ```POST http://localhost:8888/api/notification/create```
- Send (in Body): a JSON describing the resource. Example:
    ```javascript
    {
        'type': 'Notification',
        'properties': {'notification_id': -1, 'is_denunciation': False, 'keyword_id': None,
                       'notification_id_parent': 1005, 'layer_id': None, 'description': 'Muito bom'}
    }
    ```
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response: a JSON that contains the id of the resource created. Example:
    ```javascript
    {'notification_id': 10}
    ```
- Error codes:
     - 400 (Bad Request): Some attribute in the JSON is missing. Look at the documentation!
     - 401 (Unauthorized): A valid `Authorization` header is necessary!
     - 500 (Internal Server Error): Problem when create a resource. Please, contact the administrator.
- Notes:
    - The key "id", when send a JSON, is indifferent. It is just there to know where the key "id" have to be.


### PUT /api/notification

This method updates a notification described in a JSON.
- Parameters:
- Examples:
    - Update a notification: ```PUT http://localhost:8888/api/notification```
- Send (in Body): a JSON describing the resource. Example:
    ```javascript
    {
        'type': 'Notification',
        'properties': {'notification_id': 10, 'keyword_id': None,
                       'notification_id_parent': 1005, 'layer_id': None, 'description': 'Muito bom'}
    }
    ```
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
     - 400 (Bad Request): Some attribute in the JSON is missing. Look at the documentation!
     - 401 (Unauthorized): A valid `Authorization` header is necessary!
     - 403 (Forbidden): The owner of notification or administrator are who can update/delete a notification.
     - 404 (Not Found): Not found any resource.
     - 500 (Internal Server Error): Problem when update a resource. Please, contact the administrator.
- Notes:


### DELETE /api/notification/?\<params>

This method deletes one notification by id = #id.
- Parameters:
    - notification_id (mandatory) (int): the id of the resource that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Delete a resource by id: ```DELETE http://localhost:8888/api/notification/notification_id=10```
- Send (in Body):
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
     - 400 (Bad Request): Invalid parameter.
     - 401 (Unauthorized): A valid `Authorization` header is necessary!
     - 403 (Forbidden): The owner of notification or administrator are who can update/delete a notification.
     - 404 (Not Found): Not found any resource.
     - 500 (Internal Server Error): Problem when delete a resource. Please, contact the administrator.
- Notes:


### GET /api/notification_related_to_user/?\<params>

This method gets all notifications related to a user.
- Parameters:
    - user_id (mandatory) (int): the id of a user that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Get notifications by user id: http://localhost:8888/api/notification_related_to_user/?user_id=1001
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
    - 404 (Not Found): Not found the user \<ID\>.
    - 500 (Internal Server Error): Problem when get a feature. Please, contact the administrator.
- Notes:
