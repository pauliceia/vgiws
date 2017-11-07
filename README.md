# webservice

VGI's Web Service for the Pauliceia's project.

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


## Database connection

It is necessary to create the database before to start running the server, mainly if the follow error appears: "database "db_pauliceia_test" does not exist".



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


## Run the tests

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



## To run this application in PyCharm

Just point the Python interpreter of Pycharm to the folder of the virtualenv was created



## To render it in Atom

Use the command "CTRL+SHIFT+M" to show the rendered HTML markdown in Atom.
