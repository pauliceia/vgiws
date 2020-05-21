## Miscellaneous


### GET /api/user_by_token/

This method return the current logged user.
- Parameters:
- Examples:
     - Get the current logged user: http://localhost:8888/api/user_by_token/
- Send (in Body):
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response: a JSON that contains the resource. Example:
    ```javascript
    {
        'properties': {
            'username': 'rodrigo', 'is_the_admin': True, 'user_id': 1002,
            'email': 'rodrigo@admin.com', 'terms_agreed': True, 'name': 'Rodrigo',
            'is_email_valid': True, 'receive_notification_by_email': False
        },
        'type': 'User'
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid Token.
    - 401 (Unauthorized): A valid `Authorization` header is necessary!
- Notes:


### GET /api/validate_email/\<token>

This method validate a email account by \<token>.
- Parameters:
- Examples:
     - Validate email account: http://localhost:8888/api/validate_email/3XUE89Q98Q3E83HXH38D
- Send (in Body):
- Send (in Header):
- Response:
- Error codes:
    - 400 (Bad Request): Invalid Token.
    - 404 (Not Found): Not found any resource.
- Notes:


### GET /api/mask/?\<params>

This method gets masks from DB. If you doesn't put any parameter, so it will return all.
- Parameters:
    - mask_id (optional) (int): the id of a reference that is a positive integer not null (e.g. 1, 2, 3, ...).
- Examples:
     - Get all masks: http://localhost:8888/api/mask/
     - Get one mask by id: http://localhost:8888/api/mask/?mask_id=1001
- Send (in Body):
- Send (in Header):
- Response: a JSON that contains the resources selected. Example:
    ```javascript
    {
        'type': 'FeatureCollection',
        'features': [
            {
                'properties': {'mask_id': 1001, 'mask': 'YYYY-MM-DD'},
                'type': 'Mask'
            },
        ]
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid parameter.
    - 500 (Internal Server Error): Problem when get a resource. Please, contact the administrator.
- Notes:


### POST /api/convert_geojson_to_shapefile/?\<params>

This method converts a GeoJSON to ShapeFile.
- Parameters:
    - file_name (mandatory) (text): the file name of the zip with the extension (e.g. json.geojson).
- Examples:
    - Convert GeoJSON to ShapeFile: ```POST http://localhost:8888/api/convert_geojson_to_shapefile/?file_name=json.geojson```
- Send:
    - Send the binary of the GeoJSON file.
- Response:
    - Return the Shapefile inside a zip in binary mode.
- Error codes:
    - 400 (Bad Request): It is necessary to pass the file_name in request.
    - 400 (Bad Request): It is an invalid file name. (file_name: \<FILE_NAME\>)
    - 400 (Bad Request): It is necessary to pass one binary file in the body of the request.
    - 400 (Bad Request): Invalid file name: \<FILE_NAME\>. It is necessary to be a GeoJSON.
    - 500 (Internal Server Error): Problem when to convert the GeoJSON to Shapefile. OGR was not able to convert.
    - 500 (Internal Server Error): Problem when convert the resource. Please, contact the administrator.
- Notes:


<!-- ### GET /api/capabilities/ -->

<!-- This method return the capabilities of the server. -->
<!-- - Parameters: -->
<!-- - Examples: -->
<!-- - Get the capabilities: http://localhost:8888/api/capabilities/ -->
<!-- - Send: -->
<!-- - Response: a JSON that contain the capabilities of the server. Example: -->
<!-- ```javascript -->
<!-- { -->
<!-- "version": "0.0.2", -->
<!-- "status": {"postgresql": "online", "neo4j": "online"} -->
<!-- } -->
<!-- ``` -->
<!-- - Error codes: -->
<!-- - Notes: -->
