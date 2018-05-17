## Layer

A layer is a group of elements. All elements have to be associated with a layer.


### GET /api/layer/?\<params>

This method gets layers from DB. If you doesn't put any parameter, so it will return all.
- Parameters:
    - layer_id (optional): the id of a layer that is a positive integer not null (e.g. 1, 2, 3, ...);
    - is_published (optional): it is a boolean that indicates if a layer is published or not (e.g. 'TRUE' or 'FALSE');
    - f_table_name (optional): the name of the table that is a text (e.g. '_1005_layer_1003').
- Examples:
     - Get all layers: http://localhost:8888/api/layer/
     - Get one layer by id: http://localhost:8888/api/layer/?layer_id=1001
     - Get layers by is_published: http://localhost:8888/api/layer/?is_published=TRUE
     - Get one layer by f_table_name: http://localhost:8888/api/layer/?f_table_name=layer_1003
- Send:
- Response: a JSON that contains the resources selected. Example:
    ```javascript
    {
        'features': [
            {
                'properties': {'user_id_published_by': 1003, 'is_published': True, 'description': '',
                               'name': 'Robberies between 1880 to 1900',
                               'reference': [{'reference_id': 1005, 'bibtex': '@Misc{marco2017articleB,\nauthor = {Marco},\ntitle = {ArticleB},\nhowpublished = {\\url{http://www.link_to_document.org/}},\nnote = {Accessed on 02/02/2017},\nyear={2017}\n}'}],
                               'layer_id': 1002, 'f_table_name': 'layer_1002', 'source_description': '',
                               'created_at': '2017-03-05 00:00:00'},
                'type': 'Layer'
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


### PUT /api/layer/create

This method createS a new layer described in a JSON.
- Parameters:
- Examples:
     - Create a resource: ```PUT http://localhost:8888/api/layer/create```
- Send: a JSON describing the resource. Example:
    ```javascript
    {
        'type': 'Layer',
        'properties': {'layer_id': -1, 'f_table_name': 'new_layer', 'name': 'Addresses in 1930',
                       'description': '', 'source_description': '',
                       'reference': [], 'theme': [{'theme_id': 1041}]},
        'feature_table': {
            'properties': {'name': 'text', 'start_date': 'text', 'end_date': 'text'},
            'geometry': {"type": "MultiPoint"}
        }
    }

    ```
- Response: a JSON that contains the id of the resource created. Example:
    ```javascript
    {'id': 7}
    ```
- Error codes:
    - 400 (Bad Request): Table name already exists.
    - 400 (Bad Request): The parameter source needs to be a list.
    - 403 (Forbidden): It is necessary a user logged in to access this URL.
    - 500 (Internal Server Error): Problem when create a resource. Please, contact the administrator.
- Notes: The key "id", when send a JSON, is indifferent. It is just there to know where the key "id" have to be.


<!-- - PUT /api/layer/update -->


### DELETE /api/layer/delete/#id

This method delete one layer by id = #id.
- Parameters:
    - #id (mandatory): the id of the resource that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Delete a resource by id: ```DELETE http://localhost:8888/api/layer/7```
- Send:
- Response:
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 403 (Forbidden): It is necessary a user logged in to access this URL.
    - 403 (Forbidden): The owner of the layer is the unique who can delete the layer.
    - 404 (Not Found): Not found any resource.
    - 500 (Internal Server Error): Problem when delete a resource. Please, contact the administrator.
- Notes:
