## Layer

A layer is a group of elements. All elements have to be associated with a layer.


### GET /api/layer/?\<params>

This method gets layers from DB. If you doesn't put any parameter, so it will return all.

- Parameters:
    - layer_id (optional): the id of a layer that is a positive integer not null (e.g. 1, 2, 3, ...);
    - is_published (optional): it is a boolean that indicates if a layer is published or not (e.g. 'TRUE' or 'FALSE');
    - f_table_name (optional): the name of the table that is a text (e.g. '_1005_layer_1003').
    - keyword_id (optional): the id of a keyword that is a positive integer not null (e.g. 1, 2, 3, ...);
- Examples:
     - Get all layers: http://localhost:8888/api/layer/
     - Get one layer by id: http://localhost:8888/api/layer/?layer_id=1001
     - Get layers by is_published: http://localhost:8888/api/layer/?is_published=TRUE
     - Get one layer by f_table_name: http://localhost:8888/api/layer/?f_table_name=layer_1003
     - Get layers by keyword id: http://localhost:8888/api/layer/?keyword_id=1001
- Send (in Body):
- Send (in Header):
- Response: a JSON that contains the resources selected. Example:
    ```javascript
    {
        'features': [
            {
                'properties': {'description': '', 'name': 'Addresses in 1869', 'reference': [1001, 1002],
                               'layer_id': 1001, 'f_table_name': 'layer_1001', 'source_description': '',
                               'created_at': '2017-01-01 00:00:00', 'keyword': [1001, 1041]},
                'type': 'Layer'
            }
        ],
        'type': 'FeatureCollection'
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 500 (Internal Server Error): Problem when get a resource. Please, contact the administrator.
- Notes:


### POST /api/layer/create/?\<params>

This method creates a new layer described in a JSON.

- Parameters:
- Examples:
    - Create a layer with feature table: ```POST http://localhost:8888/api/layer/create```
- Send (in Body): a JSON describing the resource. Example:
    ```javascript
    {
        'type': 'Layer',
        'properties': {'layer_id': -1, 'f_table_name': 'new_layer', 'name': 'Addresses in 1930',
                       'description': '', 'source_description': '',
                       'reference': [1001], 'keyword': [1041]},
    }
    ```
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response: a JSON that contains the id of the resource created. Example:
    ```javascript
    {'layer_id': 7}
    ```
- Error codes:
    - 400 (Bad Request): The parameters reference and keyword need to be a list.
    - 400 (Bad Request): Some attribute in the JSON is missing. Look at the documentation!
    - 400 (Bad Request): f_table_name can not have special characters.
    - 400 (Bad Request): f_table_name can not start with number.
    - 400 (Bad Request): The minimum length for the f_table_name attribute is 5 characters.
    - 400 (Bad Request): The maximum length for the f_table_name attribute is 63 characters.
    - 401 (Unauthorized): A valid `Authorization` header is necessary!
    - 409 (Conflict): Conflict of f_table_name. The table name already exist. Please, rename it.
    - 409 (Conflict): Conflict of f_table_name. The table name is a reserved word. Please, rename it.
    - 409 (Conflict): The maximum of keywords allowed to a layer are 5.
    - 500 (Internal Server Error): Problem when create a resource. Please, contact the administrator.
- Notes:
    - After create the layer, it is necessary to create the feature table.
    There are two ways to create do it: (1) creating manually the feature table [(see here)](feature_table.md) and (2) importing a shapefile [(see here)](import.md).
    - The key "id", when send a JSON, is indifferent. It is just there to know where the key "id" have to be.


### PUT /api/layer

This method updated a reference described in a JSON.

- Parameters:
- Examples:
    - Update a reference: ```PUT http://localhost:8888/api/layer```
- Send (in Body): a JSON describing the resource. Example:
    ```javascript
    {
        'properties': {'description': '', 'name': 'Addresses in 1869', 'reference': [1001, 1002],
                       'layer_id': 1001, 'source_description': '',
                       'created_at': '2017-01-01 00:00:00', 'keyword': [1001, 1041]},
        'type': 'Layer'
    }
    ```
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
     - 400 (Bad Request): Some attribute in the JSON is missing. Look at the documentation!
     - 401 (Unauthorized): A valid `Authorization` header is necessary!
     - 403 (Forbidden): The layer owner or collaborator user, or administrator one are who can update a layer.
     - 404 (Not Found): Not found the layer \`\<ID\>\`.
     - 404 (Not Found): Not found the reference \`\<ID\>\`.
     - 404 (Not Found): Not found the keyword \`\<ID\>\`.
     - 409 (Conflict): The maximum of keywords allowed to a layer are 5.
     - 500 (Internal Server Error): Problem when update a resource. Please, contact the administrator.
- Notes:
    - The user can't update the "f_table_name" attribute.


### DELETE /api/layer/#id

This method deletes one layer by id = #id.

- Parameters:
    - #id (mandatory): the id of the resource that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Delete a resource by id: ```DELETE http://localhost:8888/api/layer/7```
- Send (in Body):
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 401 (Unauthorized): A valid `Authorization` header is necessary!
    - 403 (Forbidden): The layer owner or administrator user are who can delete a layer.
    - 404 (Not Found): Not found the layer \<ID\>.
    - 500 (Internal Server Error): Problem when delete a resource. Please, contact the administrator.
- Notes:


## User_Layer

Users who are part of a layer.


### GET /api/user_layer/?\<params>

This method gets users in layers from DB. If you doesn't put any parameter, so it will return all.

- Parameters:
    - layer_id (optional): the id of a layer that is a positive integer not null (e.g. 1, 2, 3, ...);
    - user_id (optional): the id of a layer that is a positive integer not null (e.g. 1, 2, 3, ...);
    - is_the_creator (optional): it is a boolean that indicates if a user is or not the creator of the layer (e.g. 'TRUE' or 'FALSE').
- Examples:
     - Get all users in layers: http://localhost:8888/api/user_layer/
     - Get users that belongs to a layer by id: http://localhost:8888/api/user_layer/?layer_id=1001
     - Get layers of a user by id: http://localhost:8888/api/user_layer/?user_id=1001
     - Get layers of a user who he/she is the creator by id: http://localhost:8888/api/user_layer/?user_id=1001&is_the_creator=TRUE
- Send (in Body):
- Send (in Header):
- Response: a JSON that contains the selected resources. Example:
    ```javascript
    {
        'features': [
            {
                'properties': {'is_the_creator': True, 'user_id': 1005, 'layer_id': 1003,
                               'created_at': '2017-04-10 00:00:00'},
                'type': 'Layer'
            },
        ],
        'type': 'FeatureCollection'
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 500 (Internal Server Error): Problem when get a resource. Please, contact the administrator.
- Notes:


### POST /api/user_layer/create

This method adds a user in a layer described in JSON.

- Parameters:
- Examples:
    - Add a user in a layer: ```POST http://localhost:8888/api/user_layer/create```
- Send (in Body): a JSON describing the resource. Example:
    ```javascript
    {
        'properties': {'user_id': 1004, 'layer_id': 1003},
        'type': 'UserLayer'
    }
    ```
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
    - 400 (Bad Request): Attribute already exists.
    - 400 (Bad Request): Some attribute in the JSON is missing. Look at the documentation!
    - 401 (Unauthorized): A valid `Authorization` header is necessary!
    - 403 (Forbidden): The creator of the layer is the unique who can add user in layer.
    - 500 (Internal Server Error): Problem when create a resource. Please, contact the administrator.
- Notes:


<!-- - PUT /api/layer/update -->


### DELETE /api/user_layer/?\<params>

This method remove a user from a layer.

- Parameters:
    - layer_id (mandatory): the id of a layer that is a positive integer not null (e.g. 1, 2, 3, ...);
    - user_id (mandatory): the id of a user that is a positive integer not null (e.g. 1, 2, 3, ...);
- Examples:
     - Delete a resource by id: ```DELETE http://localhost:8888/api/user_layer/?layer_id=1001&user_id=1004```
- Send (in Body):
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 401 (Unauthorized): A valid `Authorization` header is necessary!
    - 403 (Forbidden): The creator of the layer is the unique who can delete a user from a layer.
    - 404 (Not Found): Not found any resource.
    - 500 (Internal Server Error): Problem when delete a resource. Please, contact the administrator.
- Notes:



## Layer_follower

Users who follow a layer.


### GET /api/layer_follower/?\<params>

This method gets users who follow layers from DB. If you doesn't put any parameter, so it will return all.

- Parameters:
    - layer_id (optional) (int not null): the id of a layer (e.g. 1, 2, 3, ...);
    - user_id (optional) (int not null): the id of a layer (e.g. 1, 2, 3, ...).
- Examples:
     - Get all users who follow layers: http://localhost:8888/api/layer_follower/
     - Get users that follow a specific layer by id: http://localhost:8888/api/layer_follower/?layer_id=1001
     - Get layers that a user follow by id: http://localhost:8888/api/layer_follower/?user_id=1001
- Send (in Body):
- Send (in Header):
- Response: a JSON that contains the selected resources. Example:
    ```javascript
    {
        'features': [
            {
                'properties': {'created_at': '2017-01-02 00:00:00', 'layer_id': 1002, 'user_id': 1005},
                'type': 'LayerFollower'
            },
        ],
        'type': 'FeatureCollection'
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 500 (Internal Server Error): Problem when get a resource. Please, contact the administrator.
- Notes:


### POST /api/layer_follower/create

This method follow a user in a layer described in JSON.

- Parameters:
- Examples:
    - Add a user in a layer: ```POST http://localhost:8888/api/layer_follower/create```
- Send (in Body): a JSON describing the resource. Example:
    ```javascript
    {
        'properties': {'layer_id': 1006},
        'type': 'LayerFollower'
    }
    ```
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
    - 400 (Bad Request): Attribute already exists.
    - 400 (Bad Request): Some attribute in the JSON is missing. Look at the documentation!
    - 401 (Unauthorized): A valid `Authorization` header is necessary!
    - 409 (Bad Request): The user can't follow a layer, because he/she already follow it.
    - 500 (Internal Server Error): Problem when create a resource. Please, contact the administrator.
- Notes:


<!-- - PUT /api/layer_follower/update -->


### DELETE /api/layer_follower/?\<params>

This method do a user stop following a layer.

- Parameters:
    - layer_id (mandatory) (int not null): the id of a layer (e.g. 1, 2, 3, ...);
    - user_id (mandatory) (int not null): the id of a user (e.g. 1, 2, 3, ...).
- Examples:
     - Delete a resource by id: ```DELETE http://localhost:8888/api/layer_follower/?layer_id=1001&user_id=1004```
- Send (in Body):
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 401 (Unauthorized): A valid `Authorization` header is necessary!
    - 404 (Not Found): Not found any resource.
    - 500 (Internal Server Error): Problem when delete a resource. Please, contact the administrator.
- Notes: