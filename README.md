# webservice

Web Service for Explicit VGI for the Pauliceia's project.

<!---
A basic project for Tornado application.

The meaning of the mainly folders and files are:

- handlers: folder with the controllers;

- settings: folder with the settings;

- static: folder with the static files;

- template: folder with the static files;

- main.py: file that start the application;

- requirements.txt: list of requirements of the project;

- create_venv.sh: example how to create a virtualenv to the project;

- start_app.sh: example how to start the application using the virtualenv.

-->


## Running the server

<details>
<summary> click here </summary>
<p>

This project has made in Python 3 and use [VirtualEnvWrapper](http://www.arruda.blog.br/programacao/python/usando-virtualenvwrapper/) to facilitate the environment.

WARNING: It is necessary a database to run it, whether is not exist, create a new one as follow on next section.

To create a new virtualenv with Python 3:

```
$ mkvirtualenv -p /usr/bin/python3 pauliceia_webservice
```

If the environment do not turn on automatically, so switch it:

```
$ workon pauliceia_webservice
```

Install the dependencies that are in requirements.txt file:

```
$ pip install -r requirements.txt
```

Run the application normally or on Debug Mode::

```
$ python main.py
$ python main.py --debug=True
```

</p>
</details>


## Database connection

It is necessary to create the database before to start running the server, mainly if the follow error appears: "database "db_pauliceia_test" does not exist".

<details>
<summary> click here </summary>
<p>

### Create the database of test

First of all, access the postgres on command line:

```
$ sudo -i -u postgres
$ psql -d postgres
```

Remove the database, if it exists and create test database:

```sql
DROP DATABASE IF EXISTS db_pauliceia_test;
CREATE DATABASE db_pauliceia_test;
```

Connect on database created before and active the PostGIS extension:

```sql
\c db_pauliceia_test
CREATE EXTENSION postgis;
```

To exit, use:
```sql
\q
```

</p>
</details>


## Run the tests

<details>
<summary> click here </summary>
<p>

First of all, clean the DB of test. On console, go to root folder, turn on the environment and run the cleaning code:

```
$ workon pauliceia_webservice
$ python tests/util/clean_test_db.py
```


After that, run the server in Debug mode:

```
$ python main.py --debug=True
```


On another console, go to tests folder, turn on the environment and execute the tests:

```
$ cd tests/
$ workon pauliceia_webservice
$ python run_tests.py
```

Alright, the tests will be execute with a new test database.


</p>
</details>


## To run this application in PyCharm

Just point the Python interpreter of Pycharm to the folder of the virtualenv was created



## To render it in Atom

Use the command "CTRL+SHIFT+M" to show the rendered HTML markdown in Atom.


## API Doc:


### Miscellaneous

- GET /api/capabilities/

    This method return the capabilities of the server.
    - Parameters:
    - Send:
    - Response: a JSON that contain the capabilities of the server. Example:
        ```javascript
        {
            "version": "0.0.1",
            "status": {"database": "online"}
        }
        ```
    - Error codes:
    - Notes:

### Project

<details>
<summary> click here </summary>
<p>


- GET /api/project/?\<params>

    This method gets projects from DB. If you doesn't put any parameter, so will return all.
    - Parameters:
        - project_id (optional): the id of a project that is a positive integer not null (e.g. 1, 2, 3, ...).
        - user_id (optional): the id of a user that is a positive integer not null (e.g. 1, 2, 3, ...).
    - Send:
    - Response: a JSON that contain the features selected. Example:
        ```javascript
            {
                'features': [
                    {
                        'type': 'Project',
                        'tags': [{'k': 'name', 'v': 'default'},
                                 {'k': 'description', 'v': 'default project'}],
                        'properties': {'removed_at': None, 'fk_user_id_owner': 1001,
                                       'id': 1001, 'create_at': '2017-10-20 00:00:00'}
                    }
                ],
                'type': 'FeatureCollection'
            }
        ```
    - Error codes:
        - 400 (Bad Request): Invalid parameter.
        - 404 (Not Found): There is no project.
        - 500 (Internal Server Error): Problem when get a project. Please, contact the administrator.
    - Examples:
         - Get all projects: http://localhost:8888/api/project/
         - Get project by id: http://localhost:8888/api/project/?project_id=1001
         - Get projects by user id: http://localhost:8888/api/project/?user_id=1001
    - Notes:

- PUT /api/project/create

    This method create a new project described in a JSON.
    - Parameters:
    - Send: a JSON describing the feature. Example:
        ```javascript
            {
                'project': {
                    'tags': [{'k': 'created_by', 'v': 'test_api'},
                             {'k': 'name', 'v': 'project of data'},
                             {'k': 'description', 'v': 'description of the project'}],
                    'properties': {'id': -1}
                }
            }
        ```
    - Response: a JSON that contain the id of the feature created. Example:
        ```javascript
            {'id': 7}
        ```
    - Error codes:
        - 403 (Forbidden): It is necessary a user logged in to access this URL.
        - 500 (Internal Server Error): Problem when create a project. Please, contact the administrator.
    - Notes: The key "id", when send a JSON, is indifferent. It is just there to know where the key "id" have to be.

<!-- - PUT /api/project/update -->

- DELETE /api/project/delete/#id

    This method delete one project by id = #id.
    - Parameters:
        - #id (mandatory): the id of a project that is a positive integer not null (e.g. 1, 2, 3, ...).
    - Send:
    - Response:
    - Error codes:
        - 400 (Bad Request): Invalid parameter.
        - 403 (Forbidden): It is necessary a user logged in to access this URL.
        - 500 (Internal Server Error): Problem when delete a project. Please, contact the administrator.
    - Examples:
         - Delete a project by id: ```DELETE http://localhost:8888/api/project/7```
    - Notes:


</p>
</details>


### Changeset

<details>
<summary> click here </summary>
<p>

<!-- - GET /api/changeset/#id -->

- PUT /api/changeset/create

    This method create a new changeset described in a JSON.
    - Parameters:
    - Send: a JSON describing the feature.
    - Response: a JSON that contain the id of the feature created.
    - Error codes:
        - 500 (Internal Server Error): Problem when create a changeset. Please, contact the administrator.
    - Notes:

<!-- - PUT /api/changeset/update -->

- PUT /api/changeset/close/#id

    This method close a changeset by id = #id.
    - Parameters:
        - #id (mandatory): a positive integer (e.g. 1, 2, 3, ...).
    - Send:
    - Response:
    - Error codes:
        - 400 (Bad Request): Invalid parameter.
        - 400 (Bad Request): It needs a valid id to close a changeset.
        - 500 (Internal Server Error): Problem when close a changeset. Please, contact the administrator.
    - Notes:


</p>
</details>


### Elements (it can be node, way or area)

<details>
<summary> click here </summary>
<p>

- GET /api/\[node|way|area]/?\<params>

    This method gets elements from DB. If you doesn't put any parameter, so will return all.
    - Parameters:
        - element_id (optional): the id of a element (e.g. 1, 2, 3, ...).
        - project_id (optional): the id of a project (e.g. 1, 2, 3, ...).
        - changeset_id (optional): the id of a changeset (e.g. 1, 2, 3, ...).
    - Send:
    - Response: a GeoJSON that contain the features selected.
    - Error codes:
        - 400 (Bad Request): Invalid argument(s).
        - 404 (Not Found): There is no element.
        - 500 (Internal Server Error): Problem when get a element. Please, contact the administrator.
    - Examples:
        - http://localhost:8888/api/node/?element_id=1001
        - http://localhost:8888/api/way/?project_id=1001
        - http://localhost:8888/api/area/?changeset_id=1001
        - http://localhost:8888/api/node/?project_id=1001&changeset_id=1001
        - http://localhost:8888/api/way/?element_id=1001&project_id=1001&changeset_id=1001
        - http://localhost:8888/api/area/
    - Notes:

- PUT /api/\[node|way|area]/create

    This method create a new element described in a GeoJSON.
    - Parameters:
    - Send: a GeoJSON describing the element.
    - Response: a JSON that contain the id of the feature created.
    - Error codes:
        - 400 (Bad Request): ERROR: The changeset with id=X is closed, so it is not possible to use it.
            - Just can use changesets that are open.
        - 500 (Internal Server Error): Problem when create a element. Please, contact the administrator.
    - Notes: when add a element, it starts with a default version 1 and it is saved in current_element table.

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

- DELETE /api/\[node|way|area]/#id

    This method delete element by id = #id.
    - Parameters:
        - #id (mandatory): a positive integer (e.g. 1, 2, 3, ...).
    - Send:
    - Response:
    - Error codes:
        - 400 (Bad Request): Invalid parameter.
        - 400 (Bad Request): It needs a valid id to delete a element.
        - 500 (Internal Server Error): Problem when delete a element. Please, contact the administrator.
    - Notes: when delete a element, it is removed from current_element table (main) and put in element table (historical), with its version.
            After that, is duplicated the row and with this copy, save in element table with new version (increment +1) and with its visibility equals FALSE, because it was removed.

<!-- - GET /api/\[node|way|area]/history/#id -->

</p>
</details>


### Tags

<details>
<summary> click here </summary>
<p>

All features can be mapped usings [tags](http://wiki.openstreetmap.org/wiki/Tags), like OSM.
There are some standard features described in [OSM Map Features](http://wiki.openstreetmap.org/wiki/Map_Features) that can be used.
There are too others specific tags for Pauliceia' project, described on following sections.


#### Authors

| Key                  | Value                          | Element              | Comment                                  |
| -------------------- | ------------------------------ | -------------------- | ---------------------------------------- |
| original_author      | text (e.g. "J. R. R. Tolkien") | node, way or area    | the original author of the data          |
| food_author          | text (e.g. "Jorge")            | node, way or area    | the user that feeding the system         |


</p>
</details>


## Inspiration

This web service have as inspiration the following services:

- [OSM API](http://wiki.openstreetmap.org/wiki/API_v0.6)
- [Building Inspector](https://buildinginspector.nypl.org/data)
