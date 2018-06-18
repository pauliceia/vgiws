## Time Columns


### GET /api/time_columns/?\<params>

This method gets time columns from DB. If you doesn't put any parameter, so it will return all.
- Parameters:
- Examples:
     - Get all time columns: http://localhost:8888/api/time_columns/
- Send (in Body):
- Send (in Header):
- Response: a JSON that contains the resources selected. Example:
    ```javascript
    {
        'features': [
            {
                'properties': {'start_date': '1900-01-01', 'end_date': '1920-12-31',
                               'end_date_column_name': 'end_date', 'f_table_name': 'layer_1003',
                               'start_date_column_name': 'start_date'},
                'type': 'TimeColumns'
            },
        ],
        'type': 'FeatureCollection'
    }
    ```
- Error codes:
    <!--- 400 (Bad Request): Invalid parameter.-->
    <!--- 404 (Not Found): Not found any resource.-->
    - 500 (Internal Server Error): Problem when get a resource. Please, contact the administrator.
- Notes:


<!--### POST /api/time_columns/create/?\<params>-->

<!--This method creates a new time columns described in a JSON.-->
<!--- Parameters:-->
<!--- Examples:-->
    <!--- Create a time columns: ```POST http://localhost:8888/api/time_columns/create```-->
<!--- Send (in Body): a JSON describing the resource. Example:-->
    <!--```javascript-->
    <!--{-->
        <!--'properties': {'user_id': 1004, 'keyword_id': 1003, 'region': 'São Francisco'},-->
        <!--'type': 'time columns'-->
    <!--}-->
    <!--```-->
<!--- Send (in Header):-->
    <!--- Send an "Authorization" header with a valid Token.-->
<!--- Response:-->
<!--- Error codes:-->
    <!--- 400 (Bad Request): Attribute already exists.-->
    <!--- 400 (Bad Request): Some attribute in JSON is missing. Look the documentation!-->
    <!--- 401 (Unauthorized): It is necessary an Authorization header valid.-->
    <!--- 403 (Forbidden): The administrator is who can create/update/delete a time columns.-->
    <!--- 500 (Internal Server Error): Problem when create a resource. Please, contact the administrator.-->
<!--- Notes:-->


<!-- - PUT /api/time_columns/update -->


<!--### DELETE /api/time_columns/?\<params>-->

<!--This method deletes one time columns.-->
<!--- Parameters:-->
    <!--- user_id (mandatory): the id of the user that is a positive integer not null (e.g. 1, 2, 3, ...).-->
    <!--- keyword_id (mandatory): the id of the keyword that is a positive integer not null (e.g. 1, 2, 3, ...).-->
<!--- Examples:-->
     <!--- Delete a resource by id: ```DELETE http://localhost:8888/api/time_columns/?user_id=1001&keyword_id=1002```-->
<!--- Send (in Body):-->
<!--- Send (in Header):-->
    <!--- Send an "Authorization" header with a valid Token.-->
<!--- Response:-->
<!--- Error codes:-->
    <!--- 400 (Bad Request): Invalid parameter.-->
    <!--- 401 (Unauthorized): It is necessary an Authorization header valid.-->
    <!--- 403 (Forbidden): The administrator is who can create/update/delete a time columns.-->
    <!--- 404 (Not Found): Not found any resource.-->
    <!--- 500 (Internal Server Error): Problem when delete a resource. Please, contact the administrator.-->
<!--- Notes:-->
