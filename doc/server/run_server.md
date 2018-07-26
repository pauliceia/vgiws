## Firsts steps

Before to run the server for once. It is necessary to rename two files that are inside the settings folder:

```
$ mv settings/SAMPLE_db_settings.py settings/db_settings.py
$ mv settings/SAMPLE_accounts.py settings/accounts.py
```

The files have the settings information that are secrets. So fill it as you want and remember: don't let anyone know its content!

The file db_settings.py contains the database connection settings and the accounts.py contains the settings of social login accounts (Google and Facebook) and the cookie secret.

Hint: How to generate a new cookie secret: https://gist.github.com/didip/823887


## Run the server

This project has made in Python 3 and use [VirtualEnvWrapper](http://www.arruda.blog.br/programacao/python/usando-virtualenvwrapper/) to facilitate the environment.

WARNING: It is necessary a database to run it, whether is not exist, create a new one [here](db_connection.md).

If you don't have the pip, install it:
```
$ sudo apt-get update
$ sudo apt-get -y install python-pip
$ sudo apt-get -y install python3-pip
```

To create a new virtualenv with Python 3:

```
$ mkvirtualenv -p /usr/bin/python3.5 pauliceia_webservice
```

If the environment do not turn on automatically, so switch it:

```
$ workon pauliceia_webservice
```

Install the dependencies that are in requirements.txt file:

```
$ pip install -r requirements.txt
```

Run the application normally, on Debug Mode, or on Debug Mode and not publishing the layers in geoserver:

```
$ python main.py
$ python main.py --debug=True
$ python main.py --debug=True --publish_layers_in_geoserver=False
```


## Run the first version of production system

On a console, get into the main folder, for example:

```
$ cd vgiws/
```

Turn on the environment:

```
$ workon pauliceia_webservice
```

Clean the production database:

```
$ python tests/util/clean_db.py
```

Run the application in production mode:

```
$ python main.py
```

On another console, activate the environment and after that run the code to upload the database:

```
$ cd vgiws/
$ workon pauliceia_webservice
$ python files/production/upload_old_db_in_new_db.py
```
