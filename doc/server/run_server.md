## First steps

Before to run the server for once. It is necessary to rename the following file:

```
$ cd vgiws/
$ mv settings/SAMPLE_accounts.py settings/accounts.py
```

The files have the settings information that are secrets. So fill it as you want and remember: don't let anyone know its content!

The file accounts.py contains the settings of social login accounts (Google and Facebook) and the cookie secret.

Hint: How to generate a new cookie secret: https://gist.github.com/didip/823887


## Run the server

On the terminal, get into the main folder:

```
$ cd vgiws/
```

To debug, build the image and create the container with the VGIMWS:

```
$ docker build -t vgiws -f Dockerfile
$ docker run --rm -v $(pwd):/usr/src/vgiws -p 8888:8888 --name vgiws_debug vgiws python -u main.py --debug=True --publish_layers_in_geoserver=False
```

Or you can create the container with the VGIMWS in production:

```
$ docker-compose -f docker-compose.yml up -d
or
$ docker run --rm -d -v $(pwd):/usr/src/vgiws -p 8888:8888 --name vgiws_prod vgiws python -u main.py
```

The docker-compose will build the image of VGIMWS (if it doesn't exist) and create the container with this image.

If it is needed to build the image again, use the commands:

```
$ docker-compose -f docker-compose.yml build
$ docker-compose -f docker-compose_debug.yml build
```


## Run the first version of production system

You need to run the Geoserver:

```
$ cd geoserver/bin
$ ./startup.sh
```

After that, you need to run the Geoserver-rest.
For that, follow the link: https://github.com/Pauliceia/geoserver-rest .
Don't forget to pass the Geoserver connection in the _config/environment.js file.

On a console, get into the main folder and run the production container:

```
$ cd vgiws/
$ docker-compose -f docker-compose.yml up -d
```

On another console, get into the production container:

```
$ docker exec -it vgiws_prod /bin/bash
```

Inside the container, clean the production database:

```
# python tests/util/clean_db.py
```

After that, you need to rise the old database to the new:

```
# python files/production/upload_old_db_in_new_db.py
```
