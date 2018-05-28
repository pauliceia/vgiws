
## Database connection

It is necessary to create the database before to start running the server, mainly if the follow error appears: "database "pauliceia_test" does not exist".

This application uses two databases: PostgreSQL with PostGis extension and Neo4J.


### Create the database in PostgreSQL with PostGis extension

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
CREATE EXTENSION unaccent;

\c pauliceia_test
CREATE EXTENSION postgis;
CREATE EXTENSION unaccent;
```

To exit, use:
```sql
\q
```

It is necessary to create the schema database now, for it, follow the section "Clean the database".


#### Clean the database

If you want to clean the database and put default values, on the root folder of the project, use the follow commands to main DB or test DB:

```
$ python tests/util/clean_db.py
$ python tests/util/clean_db.py --debug=True
```


### Create the database in Neo4J

Install the [Neo4J version 3.3.1](https://neo4j.com/docs/operations-manual/current/installation/linux/debian/) in a Ubuntu machine.

If the service do not run automatically, execute:

```
$ sudo service neo4j start
```

Open a browser and enter in 'http://localhost:7474/browser/' to show the database interface. If is the once, will appear to change the password.

Now create a new database or change it, open the neo4j.conf file:

```
$ sudo nano /etc/neo4j/neo4j.conf
```

Search for ```dbms.active_database=```, its default value is ```graph.db```, so replace it to ```theme.db``` and restart the Neo4j (if is a test db, so use ```theme_test.db```):

```
$ sudo service neo4j restart
```

The databases are save in ```/var/lib/neo4j/data/databases``` folder.


#### To use a Tree Graph

Download the [APOC JAR version 3.3.0.1](https://github.com/neo4j-contrib/neo4j-apoc-procedures/releases/3.3.0.1).

Put the JAR inside the plugins folder (/var/lib/neo4j/plugins). One way is copying with the follow command:

```
$ sudo cp ~rodrigo/apoc-3.3.0.1-all.jar /var/lib/neo4j/plugins
```


#### Clean the database

Change the database (main or test DB) as explained on 'Create the database in Neo4J' section.
If you want to clean the database and put default values, on the root folder of the project, use the follow commands:

```
$ cat files/db/neo4j/theme_db.cql | cypher-shell -u <USERNAME> -p <PASSWORD> --format plain
```

Remember: \<USERNAME> and  \<PASSWORD> are the username and password of the database.
