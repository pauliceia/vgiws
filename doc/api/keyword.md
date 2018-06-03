## Keyword


### GET /api/keyword/?\<params>

This method gets keywords from DB. If you doesn't put any parameter, so it will return all.
- Parameters:
    - keyword_id (optional): the id of a keyword that is a positive integer not null (e.g. 1, 2, 3, ...);
    - parent_id (optional): the id of a parent keyword that is a positive integer not null (e.g. 1, 2, 3, ...);
    - name (optional): a text with a name of the keyword that is searching (e.g 'assault');
    - user_id_creator (optional): the id of a user that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Get all keywords: http://localhost:8888/api/keyword/
     - Get one keyword by id: http://localhost:8888/api/keyword/?keyword_id=1001
     - Get keywords by user id: http://localhost:8888/api/keyword/?user_id_creator=1001
     - Get keywords by parent id: http://localhost:8888/api/keyword/?parent_id=1001
     - Get keywords by name: http://localhost:8888/api/keyword/?name=assault
- Send (in Body):
- Send (in Header):
- Response: a JSON that contains the resources selected. Example:
    ```javascript
    {
        'features': [
            {
                'properties': {'parent_id': 1001, 'name': 'event', 'user_id_creator': 1001,
                               'created_at': '2017-01-01 00:00:00', 'keyword_id': 1002},
                'type': 'Keyword'
            },
        ],
        'type': 'FeatureCollection'
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 404 (Not Found): Not found any resource.
    - 500 (Internal Server Error): Problem when get a resource. Please, contact the administrator.
- Notes:


### POST /api/keyword/create/

This method creates a new keyword described in a JSON.
- Parameters:
- Examples:
    - Create a keyword: ```POST http://localhost:8888/api/keyword/create```
- Send (in Body): a JSON describing the resource. Example:
    ```javascript
    {
        'properties': {'keyword_id': -1, 'name': 'newkeyword', 'parent_id': 1001},
        'type': 'Keyword'
    }
    ```
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response: a JSON that contains the id of the resource created. Example:
    ```javascript
    {'keyword_id': 15}
    ```
- Error codes:
     - 400 (Bad Request): Attribute already exists.
     - 400 (Bad Request): Some attribute in JSON is missing. Look the documentation!
     - 401 (Unauthorized): It is necessary an Authorization header valid.
     - 500 (Internal Server Error): Problem when create a resource. Please, contact the administrator.
- Notes:
    - The key "id", when send a JSON, is indifferent. It is just there to know where the key "id" have to be.


<!-- - PUT /api/layer/update -->


### DELETE /api/keyword/#id

This method deletes one keyword by id = #id.
- Parameters:
    - #id (mandatory): the id of the resource that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Delete a resource by id: ```DELETE http://localhost:8888/api/keyword/10```
- Send (in Body):
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response:
- Error codes:
     - 400 (Bad Request): Invalid parameter.
     - 401 (Unauthorized): It is necessary an Authorization header valid.
     - 403 (Forbidden): The creator of the keyword is the unique who can delete the keyword.
     - 404 (Not Found): Not found any resource.
     - 500 (Internal Server Error): Problem when delete a resource. Please, contact the administrator.
- Notes: