
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
