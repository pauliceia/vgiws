## Changeset

A changeset is a group of changes did by a user. It provide the changes of the elements, its versions and etc.


###  GET /api/changeset/?\<params>

This method gets changesets from DB. If you doesn't put any parameter, so will return all.
- Parameters:
    - changeset_id (optional): the id of a changeset that is a positive integer not null (e.g. 1, 2, 3, ...).
    - layer_id (optional): the id of a layer that is a positive integer not null (e.g. 1, 2, 3, ...).
    - user_id_creator (optional): the id of a user that is a positive integer not null (e.g. 1, 2, 3, ...).
    - open (optional): if use this parameter, get all open changesets.
    - closed (optional): if use this parameter, get all closed changesets.
- Examples:
    - Get all changesets: http://localhost:8888/api/changeset/
    - Get one changeset by id: http://localhost:8888/api/changeset/?changeset_id=1001
    - Get all changesets by layer id: http://localhost:8888/api/changeset/?layer_id=1001
    - Get all changesets by user id:  http://localhost:8888/api/changeset/?user_id_creator=1001
    - Get all changesets by layer id and that are open: http://localhost:8888/api/changeset/?layer_id=1001&open=True
    - Get all changesets that are closed: http://localhost:8888/api/changeset/?closed=True
- Send:
- Response: a JSON that contain the features selected. Example:
    ```javascript
    {
        'features': [
            {
                'properties': {'created_at': '2017-04-12 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1003,
                               'closed_at': '2017-04-12 00:00:00', 'layer_id': 1003,
                               'description': 'Creating layer_1003'},
                'type': 'Changeset'
            },
        ],
        'type': 'FeatureCollection'
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 404 (Not Found): Not found any feature.
    - 500 (Internal Server Error): Problem when get a resource. Please, contact the administrator.
- Notes:


<!-- ### POST /api/changeset/create -->

<!-- This method create a new changeset described in a JSON. -->
<!-- - Parameters: -->
<!-- - Examples: -->
     <!-- - Create a feature: ```PUT http://localhost:8888/api/changeset/create``` -->
<!-- - Send: a JSON describing the feature. Example: -->
    <!-- ```javascript -->
    <!-- { -->
        <!-- 'tags': {'created_by': 'Tomás de Aquino', 'comment': 'Changeset for crimes data.'}, -->
        <!-- 'properties': {'id': -1, "fk_project_id": 1001}, -->
        <!-- 'type': 'Changeset', -->
    <!-- } -->
    <!-- ``` -->
<!-- - Response: a JSON that contain the id of the feature created. Example: -->
    <!-- ```javascript -->
    <!-- {'id': 7} -->
    <!-- ``` -->
<!-- - Error codes: -->
    <!-- - 403 (Forbidden): It is necessary a user logged in to access this URL. -->
    <!-- - 500 (Internal Server Error): Problem when create a feature. Please, contact the administrator. -->
<!-- - Notes: The key "id", when send a JSON, is indifferent. It is just there to know where the key "id" have to be. -->


<!-- - PUT /api/changeset/update -->


<!-- ### POST /api/changeset/close/#id -->

<!-- This method close a changeset by id = #id. -->
<!-- - Parameters: -->
    <!-- - #id (mandatory): the id of the feature that is a positive integer not null (e.g. 1, 2, 3, ...). -->
<!-- - Examples: -->
     <!-- - Close a changeset by id: ```PUT http://localhost:8888/api/changeset/close/7``` -->
<!-- - Send: -->
<!-- - Response: -->
<!-- - Error codes: -->
    <!-- - 400 (Bad Request): Invalid parameter. -->
    <!-- - 403 (Forbidden): It is necessary a user logged in to access this URL. -->
    <!-- - 404 (Not Found): Not found any feature. -->
    <!-- - 500 (Internal Server Error): Problem when close a feature. Please, contact the administrator. -->
<!-- - Notes: -->


<!-- ### DELETE /api/changeset/delete/#id -->

<!-- This method delete one changeset by id = #id. -->
<!-- - Parameters: -->
    <!-- - #id (mandatory): the id of the feature that is a positive integer not null (e.g. 1, 2, 3, ...). -->
<!-- - Examples: -->
     <!-- - Delete a feature by id: ```DELETE http://localhost:8888/api/changeset/9``` -->
<!-- - Send: -->
<!-- - Response: -->
<!-- - Error codes: -->
    <!-- - 400 (Bad Request): Invalid parameter. -->
    <!-- - 403 (Forbidden): It is necessary a user logged in to access this URL. -->
    <!-- - 404 (Not Found): Not found any feature. -->
    <!-- - 500 (Internal Server Error): Problem when delete a feature. Please, contact the administrator. -->
<!-- - Notes: -->
