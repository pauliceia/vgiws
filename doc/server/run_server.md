## Run the server

This project has made in Python 3 and use [VirtualEnvWrapper](http://www.arruda.blog.br/programacao/python/usando-virtualenvwrapper/) to facilitate the environment.

WARNING: It is necessary a database to run it, whether is not exist, create a new one [here](db_connection.md).

If you don't have the pip, install it:
```
$ sudo apt-get update
$ sudo apt-get -y install python-pip
$ sudo apt-get -y install python-pip3
```

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

Run the application normally or on Debug Mode:

```
$ python main.py
$ python main.py --debug=True
```
