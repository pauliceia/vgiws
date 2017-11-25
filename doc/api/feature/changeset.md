### Changeset

<details>
<summary> click here </summary>
<p>

<!-- - GET /api/changeset/#id -->

- PUT /api/changeset/create

    This method create a new changeset described in a JSON.
    - Parameters:
    - Examples:
         - Create a feature: ```PUT http://localhost:8888/api/changeset/create```
    - Send: a JSON describing the feature. Example:
        ```javascript
        {
            'changeset': {
                'tags': [{'k': 'created_by', 'v': 'test_api'},
                         {'k': 'comment', 'v': 'testing create changeset'}],
                'properties': {'id': -1, "fk_project_id": 1001}
            }
        }
        ```
    - Response: a JSON that contain the id of the feature created. Example:
        ```javascript
        {'id': 7}
        ```
    - Error codes:
        - 403 (Forbidden): It is necessary a user logged in to access this URL.
        - 500 (Internal Server Error): Problem when create a changeset. Please, contact the administrator.
    - Notes: The key "id", when send a JSON, is indifferent. It is just there to know where the key "id" have to be.

<!-- - PUT /api/changeset/update -->

- PUT /api/changeset/close/#id

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
        - 500 (Internal Server Error): Problem when delete a project. Please, contact the administrator.
    - Notes:


</p>
</details>