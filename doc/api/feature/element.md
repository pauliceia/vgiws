## Element (it can be node, way or area)


###  GET /api/\[node|way|area]/?\<params>

This method gets elements from DB. If you doesn't put any parameter, so will return all.
- Parameters:
    - element_id (optional): the id of a element that is a positive integer not null (e.g. 1, 2, 3, ...).
    - user_id (optional): the id of a user that is a positive integer not null (e.g. 1, 2, 3, ...).
    - project_id (optional): the id of a project that is a positive integer not null (e.g. 1, 2, 3, ...).
    - changeset_id (optional): the id of a changeset that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
    - Get one node by id: http://localhost:8888/api/node/?element_id=1001
    - Get all ways of project: http://localhost:8888/api/way/?project_id=1001
    - Get all areas of one changeset:  http://localhost:8888/api/area/?changeset_id=1001
    - Get all ways of one user:  http://localhost:8888/api/way/?user_id=1001
    - Get all area elements: http://localhost:8888/api/area/
- Send:
- Response: a GeoJSON that contain the features selected. Example:
    ```javascript
    {
        'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
        'type': 'FeatureCollection',
        'features': [
            {
                'tags': [{'v': 'R. São José', 'k': 'addr:street'},
                         {'v': '10', 'k': 'addr:housenumber'},
                         {'v': '1870', 'k': 'start_date'},
                         {'v': '1910', 'k': 'end_date'}],
                'type': 'Feature',
                'properties': {'id': 1001, 'fk_changeset_id': 1001},
                'geometry': {'type': 'MultiPoint', 'coordinates': [[-23.546421, -46.635722]]}
            }
        ]
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 404 (Not Found): Not found any feature.
    - 500 (Internal Server Error): Problem when get a element. Please, contact the administrator.
- Notes: If pass more than one parameter, the server will use the one that have more importance.
        The importance order is describe in 'Parameters' section above (element_id, user_id, ...).
        It means that: whether use the 'element_id' parameter, will be ignored the others (user_id, project_id, ...).


### PUT /api/\[node|way|area]/create

This method create a new element described in a GeoJSON.
- Parameters:
- Examples:
    - Create a feature: ```PUT http://localhost:8888/api/node/create```
- Send: a GeoJSON describing the element. The key 'features' receive a list of features to create. Example:
    ```javascript
    {
        'type': 'FeatureCollection',
        'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
        'features': [
            {
                'tags': [{'k': 'event', 'v': 'robbery'},
                         {'k': 'date', 'v': '1910'}],
                'type': 'Feature',
                'properties': {'id': -1, 'fk_changeset_id': 1001},
                'geometry': {
                    'type': 'MultiPoint',
                    'coordinates': [[-23.546421, -46.635722]]
                },
            },
            ...
        ]
    }
    ```
- Response: a list that contain the ids of the features created.
    ```javascript
    [10, ...]
    ```
- Error codes:
    - 400 (Bad Request): ERROR: The changeset with id=X is closed, so it is not possible to use it.
        - PS: Just can use changesets that are open.
    - 403 (Forbidden): It is necessary a user logged in to access this URL.
    - 500 (Internal Server Error): Problem when create a element. Please, contact the administrator.
- Notes:
<!-- when add a element, it starts with a default version 1 and it is saved in current_element table. -->

<!--
- PUT /api/\[node|way|area]/update

 This method update a element described in a GeoJSON.
 - Parameters:
 - Send: a GeoJSON describing the element.
 - Response: a JSON that contain the id of the feature created.
 - Error codes:
     - 500 (Internal Server Error): Problem when update a element. Please, contact the administrator.
 - Notes: when update a element, it is added in element table (historical), with the same id.
         After that, the original row is removed from current element table (main) and the element updated is added in database with the version incremented (+1).
-->


###  DELETE /api/\[node|way|area]/#id

This method delete one element by id = #id.
- Parameters:
    - #id (mandatory): the id of the feature that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
    - Delete a feature by id: ```DELETE http://localhost:8888/api/way/3```
- Send:
- Response:
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 403 (Forbidden): It is necessary a user logged in to access this URL.
    - 404 (Not Found): Not found any feature.
    - 500 (Internal Server Error): Problem when delete a project. Please, contact the administrator.
- Notes:
        <!-- when delete a element, it is removed from current_element table (main) and put in element table (historical), with its version. -->
        <!-- After that, is duplicated the row and with this copy, save in element table with new version (increment +1) and with its visibility equals FALSE, because it was removed. -->

<!-- - GET /api/\[node|way|area]/history/#id -->
