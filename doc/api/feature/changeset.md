## Changeset

A changeset is a group of changes did by a user. It provide the changes of the elements, its versions and etc.


###  GET /api/changeset/?\<params>

This method gets changesets from DB. If you doesn't put any parameter, so will return all.
- Parameters:
    - changeset_id (optional): the id of a changeset that is a positive integer not null (e.g. 1, 2, 3, ...).
    - project_id (optional): the id of a project that is a positive integer not null (e.g. 1, 2, 3, ...).
    - user_id (optional): the id of a user that is a positive integer not null (e.g. 1, 2, 3, ...).
    - open: if use this parameter, get all open changesets.
    - closed: if use this parameter, get all closed changesets.
- Examples:
    - Get one changeset by id: http://localhost:8888/api/changeset/?changeset_id=1001
    - Get all changesets of one project: http://localhost:8888/api/changeset/?project_id=1001
    - Get all changesets of one project that are open: http://localhost:8888/api/changeset/?project_id=1001&open=true
    - Get all changesets of one user:  http://localhost:8888/api/changeset/?user_id=1001
    - Get all changesets: http://localhost:8888/api/changeset/
    - Get all changesets that are closed: http://localhost:8888/api/changeset/?closed=true
- Send:
- Response: a JSON that contain the features selected. Example:
    ```javascript
    {
        'features': [
            {
                'type': 'Changeset',
                'properties': {'closed_at': '2017-12-01 00:00:00', 'fk_user_id': 1001,
                               'create_at': '2017-10-20 00:00:00', 'id': 1001},
                'tags': [{'k': 'created_by', 'v': 'pauliceia_portal'},
                         {'k': 'comment', 'v': 'a changeset created'}]
            }
        ],
        'type': 'FeatureCollection'
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 404 (Not Found): Not found any feature.
    - 500 (Internal Server Error): Problem when get a changeset. Please, contact the administrator.
- Notes: If pass more than one parameter, the server will use the one that have more importance.
        The importance order is describe in 'Parameters' section above (changeset_id, project_id, ...).
        It means that: whether use the 'changeset_id' parameter, will be ignored the others (project_id, user_id, ...).
        'open' and 'closed' parameters can be used with the others.


###  PUT /api/changeset/create

This method create a new changeset described in a JSON.
- Parameters:
- Examples:
     - Create a feature: ```PUT http://localhost:8888/api/changeset/create```
- Send: a JSON describing the feature. Example:
    ```javascript
    {
        'tags': [{'k': 'created_by', 'v': 'Tomás de Aquino'},
                 {'k': 'comment', 'v': 'Changeset for crimes data.'}],
        'properties': {'id': -1, "fk_project_id": 1001},
        'type': 'Changeset',
    }
    ```
- Response: a JSON that contain the id of the feature created. Example:
    ```javascript
    {'id': 7}
    ```
- Error codes:
    - 403 (Forbidden): It is necessary a user logged in to access this URL.
    - 500 (Internal Server Error): Problem when create a feature. Please, contact the administrator.
- Notes: The key "id", when send a JSON, is indifferent. It is just there to know where the key "id" have to be.


<!-- - PUT /api/changeset/update -->


### PUT /api/changeset/close/#id

This method close a changeset by id = #id.
- Parameters:
    - #id (mandatory): the id of the feature that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Close a changeset by id: ```PUT http://localhost:8888/api/changeset/close/7```
- Send:
- Response:
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 403 (Forbidden): It is necessary a user logged in to access this URL.
    - 404 (Not Found): Not found any feature.
    - 500 (Internal Server Error): Problem when close a feature. Please, contact the administrator.
- Notes:


### DELETE /api/changeset/delete/#id

This method delete one changeset by id = #id.
- Parameters:
    - #id (mandatory): the id of the feature that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Delete a feature by id: ```DELETE http://localhost:8888/api/changeset/9```
- Send:
- Response:
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 403 (Forbidden): It is necessary a user logged in to access this URL.
    - 404 (Not Found): Not found any feature.
    - 500 (Internal Server Error): Problem when delete a feature. Please, contact the administrator.
- Notes:
