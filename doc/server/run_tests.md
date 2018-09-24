## Run the tests


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
