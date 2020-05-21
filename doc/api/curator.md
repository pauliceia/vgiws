## Curator


### GET /api/curator/?\<params>

This method gets curators from DB. If you doesn't put any parameter, so it will return all.
- Parameters:
    - user_id (optional): the id of a user that is a positive integer not null (e.g. 1, 2, 3, ...);
    - keyword_id (optional): the id of a keyword that is a positive integer not null (e.g. 1, 2, 3, ...);
    - region (optional): the name of the region that is a text (e.g. 'Centro').
- Examples:
     - Get all curators: http://localhost:8888/api/curator/
     - Get curators by user id: http://localhost:8888/api/curator/?user_id=1001
     - Get curators by keyword id: http://localhost:8888/api/curator/?keyword_id=1001
     - Get curators by region: http://localhost:8888/api/curator/?region=Centro
- Send (in Body):
- Send (in Header):
- Response: a JSON that contains the resources selected. Example:
    ```javascript
    {
        'features': [
            {
                'properties': {'created_at': '2018-02-20 00:00:00', 'keyword_id': 1003,
                               'user_id': 1004, 'region': 'São Francisco'},
                'type': 'Curator'
            }
        ],
        'type': 'FeatureCollection'
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 404 (Not Found): Not found any resource.
    - 500 (Internal Server Error): Problem when get a resource. Please, contact the administrator.
- Notes:


### POST /api/curator/create/?\<params>

This method creates a new curator described in a JSON.
- Parameters:
- Examples:
    - Create a curator: ```POST http://localhost:8888/api/curator/create```
- Send (in Body): a JSON describing the resource. Example:
    ```javascript
    {
        'properties': {'user_id': 1004, 'keyword_id': 1003, 'region': 'São Francisco'},
        'type': 'Curator'
    }
    ```
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
    - 400 (Bad Request): Attribute already exists.
    - 400 (Bad Request): Some attribute in the JSON is missing. Look at the documentation!
    - 401 (Unauthorized): A valid `Authorization` header is necessary!
    - 403 (Forbidden): The administrator is who can create/update/delete a curator.
    - 500 (Internal Server Error): Problem when create a resource. Please, contact the administrator.
- Notes:


###  PUT /api/curator

This method updates a new curator described in a JSON.
- Parameters:
- Examples:
    - Create a curator: ```PUT http://localhost:8888/api/curator```
- Send (in Body): a JSON describing the resource. Example:
    ```javascript
    {
        'properties': {'user_id': 1004, 'keyword_id': 1003, 'region': 'São Francisco'},
        'type': 'Curator'
    }
    ```
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
    - 400 (Bad Request): Some attribute in the JSON is missing. Look at the documentation!
    - 401 (Unauthorized): A valid `Authorization` header is necessary!
    - 403 (Forbidden): The administrator is who can create/update/delete a curator.
    - 404 (Not Found): Not found any resource.
    - 500 (Internal Server Error): Problem when update a resource. Please, contact the administrator.
- Notes:


### DELETE /api/curator/?\<params>

This method deletes one curator.
- Parameters:
    - user_id (mandatory): the id of the user that is a positive integer not null (e.g. 1, 2, 3, ...).
    - keyword_id (mandatory): the id of the keyword that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Delete a resource by id: ```DELETE http://localhost:8888/api/curator/?user_id=1001&keyword_id=1002```
- Send (in Body):
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 401 (Unauthorized): A valid `Authorization` header is necessary!
    - 403 (Forbidden): The administrator is who can create/update/delete a curator.
    - 404 (Not Found): Not found any resource.
    - 500 (Internal Server Error): Problem when delete a resource. Please, contact the administrator.
- Notes:
