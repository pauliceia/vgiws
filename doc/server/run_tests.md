## Run the tests


### Without Docker

First of all, get into the root folder and turn the environment on:

```
$ cd vgiws/
$ workon pauliceia_webservice
```

If necessary, install the requirements:

```
$ pip install -r requirements.txt
```

Run the web server on debug mode:

```
$ python main.py --debug=True --publish_layers_in_geoserver=False
```

On another console, get into the test folder and turn the environment on:

```
$ cd vgiws/tests/
$ workon pauliceia_webservice
```

If necessary, clean the test database:

```
python tests/util/clean_db.py --debug=True
```

Run the tests:

```
$ python run_tests.py
```


### With Docker

First of all, get into the root folder and run the container:

```
$ cd vgiws/
$ docker-compose -f docker-compose_debug.yml up
```

On another console, get into the container and clean the database:

```
$ docker exec -it vgiws_debug /bin/bash
# python tests/util/clean_db.py --debug=True
```

Go to tests/ folder and execute the tests:

```
# cd tests/
# python run_tests.py
```

Alright, the tests will be executed with a new test database.
