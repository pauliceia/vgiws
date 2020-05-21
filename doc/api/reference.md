## Reference


### GET /api/reference/?\<params>

This method gets references from DB. If you doesn't put any parameter, so it will return all.
- Parameters:
    - reference_id (optional): the id of a reference that is a positive integer not null (e.g. 1, 2, 3, ...);
    - user_id (optional): the id of a user that is a positive integer not null (e.g. 1, 2, 3, ...);
    - description (optional): a text with a description of the reference that is searching (e.g 'Marco').
- Examples:
     - Get all references: http://localhost:8888/api/reference/
     - Get one reference by id: http://localhost:8888/api/reference/?reference_id=1001
     - Get references by user id: http://localhost:8888/api/reference/?user_id=1001
     - Get reference by description: http://localhost:8888/api/reference/?description=Marco
- Send (in Body):
- Send (in Header):
- Response: a JSON that contains the resources selected. Example:
    ```javascript
    {
        'features': [
            {
                'type': 'Reference',
                'properties': {'user_id': 1003, 'reference_id': 1053, 'description': 'DissertationD'}
            }
        ],
        'type': 'FeatureCollection'
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 500 (Internal Server Error): Problem when get a resource. Please, contact the administrator.
- Notes:


### POST /api/reference/create/

This method creates a new reference described in a JSON.
- Parameters:
- Examples:
    - Create a reference: ```POST http://localhost:8888/api/reference/create```
- Send (in Body): a JSON describing the resource. Example:
    ```javascript
    {
        'type': 'Reference',
        'properties': {'reference_id': -1, 'description': 'ArticleA'}
    }
    ```
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response: a JSON that contains the id of the resource created. Example:
    ```javascript
    {'reference_id': 10}
    ```
- Error codes:
     - 400 (Bad Request): Some attribute in the JSON is missing. Look at the documentation!
     - 401 (Unauthorized): A valid `Authorization` header is necessary!
     - 500 (Internal Server Error): Problem when create a resource. Please, contact the administrator.
- Notes:
    - The key "id", when send a JSON, is indifferent. It is just there to know where the key "id" have to be.


### PUT /api/reference

This method updates a reference described in a JSON.
- Parameters:
- Examples:
    - Update a reference: ```PUT http://localhost:8888/api/reference```
- Send (in Body): a JSON describing the resource. Example:
    ```javascript
    {
        'type': 'Reference',
        'properties': {'reference_id': 1001, 'description': 'ArticleA'}
    }
    ```
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
     - 400 (Bad Request): Some attribute in the JSON is missing. Look at the documentation!
     - 401 (Unauthorized): A valid `Authorization` header is necessary!
     - 403 (Forbidden): The layer owner or collaborator user, or administrator one are who can update or delete a reference.
     - 404 (Not Found): Not found any resource.
     - 500 (Internal Server Error): Problem when update a resource. Please, contact the administrator.
- Notes:


### DELETE /api/reference/#id

This method deletes one reference by id = #id.
- Parameters:
    - #id (mandatory): the id of the resource that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Delete a resource by id: ```DELETE http://localhost:8888/api/reference/10```
- Send (in Body):
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
     - 400 (Bad Request): Invalid parameter.
     - 401 (Unauthorized): A valid `Authorization` header is necessary!
     - 403 (Forbidden): The layer owner or collaborator user, or administrator one are who can update or delete a reference.
     - 404 (Not Found): Not found any resource.
     - 500 (Internal Server Error): Problem when delete a resource. Please, contact the administrator.
- Notes:
