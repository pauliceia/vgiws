
## Dependencies

It is needed to install the PostgreSQL database with PostGIS extension, Docker, Geoserver and the service to connect with Geoserver, before to start the application.
The following links can help to install them:
- https://www.digitalocean.com/community/tutorials/como-instalar-e-utilizar-o-postgresql-no-ubuntu-16-04-pt
- https://www.digitalocean.com/community/tutorials/como-instalar-e-usar-o-docker-no-ubuntu-16-04-pt
- http://docs.geoserver.org/stable/en/user/installation/linux.html
- https://github.com/Pauliceia/geoserver-rest

After installing the PostgreSQL, you must activate the database to accept connections with the public IP of your machine.
To do it, you need to follow the hints of Syed Aslam in the follow link:
- https://stackoverflow.com/questions/1287067/unable-to-connect-postgresql-to-remote-database-using-pgadmin


## Database connection

### Create the database in PostgreSQL with PostGis extension

After having the PostgreSQL installed, you need to access the Postgres by command line:

```
$ sudo -i -u postgres
$ psql -d postgres
```

Remove the database (main and test) if it exists and create a new one:

```sql
DROP DATABASE IF EXISTS pauliceia;
CREATE DATABASE pauliceia;

DROP DATABASE IF EXISTS pauliceia_test;
CREATE DATABASE pauliceia_test;
```

Connect on database created before and active the extensions:

```sql
\c pauliceia
CREATE EXTENSION postgis;
CREATE EXTENSION unaccent;

\c pauliceia_test
CREATE EXTENSION postgis;
CREATE EXTENSION unaccent;
```

To exit, use:
```sql
\q
```


Now, get into the root folder of the project and rename the following file:

```
$ cd vgiws/
$ mv settings/SAMPLE_db_settings.py settings/db_settings.py
```

This file contains the information related to the database connection.
It is needed to inform the correct credentials for your database.


#### Clean the database

It is necessary to create the database schema now, cleaning the database and putting the default values.
Follow the commands:

- Get into the root folder and create the container (production or test/debug mode):

```
$ cd vgiws/
$ docker-compose -f docker-compose.yml up -d
or
$ docker-compose -f docker-compose_debug.yml up
```

- Get into the container and clean the production database:
```
$ docker exec -it vgiws_prod /bin/bash
# python tests/util/clean_db.py
```

- Or get into the container and clean the test/debug database:

```
$ docker exec -it vgiws_debug /bin/bash
# python tests/util/clean_db.py --debug=True
```