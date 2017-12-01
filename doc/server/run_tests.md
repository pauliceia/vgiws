## Run the tests


First of all, clean the DB of test. On console, go to root folder, turn on the environment and run the cleaning code:

```
$ workon pauliceia_webservice
$ python tests/util/clean_db.py --debug=True
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
