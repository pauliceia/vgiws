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
    - Response: a JSON that contain the capabilities of the server.
        - Example:
        ```json
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

- GET /api/project/#id

    This method get all projects in DB or a specific with id = #id
    - Parameters:
        - #id (optional): a positive integer (e.g. 1, 2, 3, ...).
    - Send:
    - Response: a JSON that contain the features selected.
    - Error codes:
        - 404: There is no project.
        - 500: Problem when get a project. Please, contact the administrator.
    - Notes:

- PUT /api/project/create

    This method create a new project described in a JSON.
    - Parameters:
    - Send: a JSON describing the feature.
    - Response: a JSON that contain the id of the feature created.
    - Error codes:
        - 500: Problem when create a project. Please, contact the administrator.
    - Notes:

<!-- - PUT /api/project/update -->

- DELETE /api/project/delete/#id

    This method delete project by id = #id.
    - Parameters:
        - #id (mandatory): a positive integer (e.g. 1, 2, 3, ...).
    - Send:
    - Response:
    - Error codes:
        - 400: Invalid parameter
        - 400: It needs a valid id to delete a project.
        - 500: Problem when delete a project. Please, contact the administrator.
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
        - 500: Problem when create a changeset. Please, contact the administrator.
    - Notes:

<!-- - PUT /api/changeset/update -->

- PUT /api/changeset/close/#id

    This method close a changeset by id = #id.
    - Parameters:
        - #id (mandatory): a positive integer (e.g. 1, 2, 3, ...).
    - Send:
    - Response:
    - Error codes:
        - 400: Invalid parameter.
        - 400: It needs a valid id to close a changeset.
        - 500: Problem when close a changeset. Please, contact the administrator.
    - Notes:


</p>
</details>


### Elements (it can be node, way or area)

<details>
<summary> click here </summary>
<p>

- GET /api/\[node|way|area]/#id

    This method get all elements in DB or a specific with id = #id
    - Parameters:
        - #id (optional): a positive integer (e.g. 1, 2, 3, ...).
    - Send:
    - Response: a GeoJSON that contain the features selected.
    - Error codes:
        - 400: Invalid parameter.
        - 404: There is no element.
        - 500: Problem when get a element. Please, contact the administrator.
    - Notes:

- PUT /api/\[node|way|area]/create

    This method create a new element described in a GeoJSON.
    - Parameters:
    - Send: a GeoJSON describing the element.
    - Response: a JSON that contain the id of the feature created.
    - Error codes:
        - 500: Problem when create a element. Please, contact the administrator.
    - Notes: when add a element, it starts with a default version 1 and it is saved in current_element table.

<!--
 - PUT /api/\[node|way|area]/update

     This method update a element described in a GeoJSON.
     - Parameters:
     - Send: a GeoJSON describing the element.
     - Response: a JSON that contain the id of the feature created.
     - Error codes:
         - 500: Problem when update a element. Please, contact the administrator.
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
        - 400: Invalid parameter.
        - 400: It needs a valid id to delete a element.
        - 500: Problem when delete a element. Please, contact the administrator.
    - Notes: when delete a element, it is removed from current_element table (main) and put in element table (historical), with its version.
            After that, is duplicated the row and with this copy, save in element table with new version (increment +1) and with its visibility equals FALSE, because it was removed.

    its visibility become FALSE, the row

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
