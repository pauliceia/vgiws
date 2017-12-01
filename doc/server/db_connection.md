
## Database connection

It is necessary to create the database before to start running the server, mainly if the follow error appears: "database "db_pauliceia_test" does not exist".


### Create the database

First of all, access the postgres on command line:

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

Connect on database created before and active the PostGIS extension:

```sql
\c pauliceia
CREATE EXTENSION postgis;

\c pauliceia_test
CREATE EXTENSION postgis;
```

To exit, use:
```sql
\q
```

It is necessary to create the schema database now, for it, follow the section "Clean the database".


### Clean the database

If you want to clean the database, on the root folder of the project, use the follow commands to main DB or test DB:

```
$ python tests/util/clean_db.py
$ python tests/util/clean_db.py --debug=True
```