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

- Run the Geoserver:

    On the terminal, get into the Geoserver main folder and start it up:

    ```
    $ cd geoserver/bin/
    $ startup.sh
    ```

- Run the geoserver-rest:

    On the terminal, get into the geoserver-rest main folder, install the dependencies and start it up:

    ```
    $ cd geoserver-rest/
    $ npm install
    $ npm run dev
    ```

    Don't forget of passing the Geoserver connection in the _config/environment.js file.

- Run the VGIMWS

    VGIMWS has two parameters that can be passed in front of the program:
    - --debug=True: If True, so run the server in Debug mode. If False (default), run the server in production mode.
    - --publish_layers_in_geoserver=False: If False, don't publish the layers in Geoserver. If True (default), publish the layers in Geoserver.
    This flag can be used when you are debugging and don't want to publish the layers in Geoserver.

    On the terminal, get into the VGIWS main folder:

    ```
    $ cd vgiws/
    ```

    Build the image:

    ```
    $ docker build --no-cache -t vgiws:latest -t vgiws:v_0.0.4 -f Dockerfile .
    ```

    To debug, create the container with the VGIMWS:

    ```
    $ docker run --rm -v $(pwd):/usr/src/vgiws -p 8888:8888 --name vgiws_debug vgiws python -u main.py --debug=True --publish_layers_in_geoserver=False
    ```

    Or you can create the container with the VGIMWS in production mode:

    ```
    $ docker-compose -f docker-compose.yml up -d
    or
    $ docker run --rm -d -v $(pwd):/usr/src/vgiws -p 8888:8888 --name vgiws vgiws
    or
    $ docker run --rm -d -v $(pwd):/usr/src/vgiws -p 8888:8888 --name vgiws vgiws python -u main.py
    ```

    The docker-compose will build the image of VGIMWS (if it doesn't exist) and create the container with this image.

    To see the logs of the production container, use:

    ```
    $ docker logs -f vgiws
    ```

    If it is needed to build the image again, use the commands:

    ```
    $ docker-compose -f docker-compose.yml build
    $ docker-compose -f docker-compose_debug.yml build
    ```


## Run the first version of production system

You need to run the Geoserver and the geoserver-rest as done in the previous section.

Now, on a console, get into the VGIMWS main folder and run the production container:

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
