## User


### GET /api/user/?\<params>

This method gets users from DB. If you doesn't put any parameter, so will return all.
- Parameters:
    - user_id (optional): the id of a user that is a positive integer not null (e.g. 1, 2, 3, ...);
    - name (optional): a text with a name (e.g 'José').
    - email (optional): a text with a email (e.g 'joao@mail.com').
    - username (optional): a text with a username (e.g 'jose').
- Examples:
    - Get all users: http://localhost:8888/api/user/
    - Get one user by id: http://localhost:8888/api/user/?user_id=1002
    - Get users by name: http://localhost:8888/api/user/?name=Joao
    - Get user by email: http://localhost:8888/api/user/?email=joao@mail.com
    - Get user by username: http://localhost:8888/api/user/?username=jose
- Send:
- Response: a JSON that contains the selected resources. Example:
    ```javascript
    {
        'type': 'FeatureCollection',
        'features': [
            {
                'type': 'User',
                'properties': {'receive_notification_by_email': True, 'terms_agreed': False,
                               'username': 'gabriel', 'user_id': 1005, 'email': 'gabriel@admin.com',
                               'name': 'Gabriel', 'is_the_admin': False, 'can_add_layer': True,
                               'created_at': '2017-09-20 00:00:00', 'login_date': '2017-09-20T00:00:00',
                               'is_email_valid': False}
            },
        ]
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 500 (Internal Server Error): Problem when get a user. Please, contact the administrator.
- Notes:


### POST /api/user/create

This method create a new user described in a JSON.
- Parameters:
- Examples:
     - Create a resource: ```POST http://localhost:8888/api/user/create```
- Send: a JSON describing the resource. Example:
    ```javascript
    {
        'type': 'User',
        'properties': {'user_id': -1, 'email': email, 'password': '29EU290UE', 'username': 'roger', 'name': 'Roger',
                       'terms_agreed': True, 'receive_notification_by_email': False}
    }
    ```
- Response: a JSON that contains the id of the created resource. Example:
    ```javascript
    {'user_id': 7}
    ```
- Error codes:
    - 400 (Bad Request): Some attribute in the JSON is missing. Look at the documentation!
    - 400 (Bad Request): Attribute already exists.
    - 500 (Internal Server Error): Problem when create a resource. Please, contact the administrator.
- Notes:
    - The password needs to be encrypted with a hash called sha512 (HEX)
    - The key "user_id", when send a JSON, is indifferent. It is just there to know where the key "user_id" have to be.


### PUT /api/user

This method updates a user described in a JSON.
- Parameters:
- Examples:
    - Update a reference: ```PUT http://localhost:8888/api/user```
- Send (in Body): a JSON describing the resource. Example:
    ```javascript
    {
        'type': 'User',
        'properties': {'user_id': 7, 'email': email, 'username': 'roger', 'name': 'Roger',
                       'terms_agreed': True, 'receive_notification_by_email': False}
    }
    ```
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
     - 400 (Bad Request): Attribute already exists.
     - 400 (Bad Request): Some attribute in the JSON is missing. Look at the documentation!
     - 401 (Unauthorized): A valid `Authorization` header is necessary!
     - 403 (Forbidden): Just the own user or an administrator can update a user.
     - 404 (Not Found): Not found any resource.
     - 500 (Internal Server Error): Problem when update a resource. Please, contact the administrator.
- Notes:

<!--
### DELETE /api/user/#id

This method delete one user by id = #id.
- Parameters:
    - #id (mandatory): the id of the resource that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Delete a resource by id: ```DELETE http://localhost:8888/api/user/7```
- Send:
- Response:
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 401 (Unauthorized): A valid `Authorization` header is necessary!
    - 403 (Forbidden): Just administrator can delete other user.
    - 404 (Not Found): Not found any resource.
    - 500 (Internal Server Error): Problem when delete a resource. Please, contact the administrator.
- Notes:
-->