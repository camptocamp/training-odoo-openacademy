<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# Docker and Databases

### Working with several databases

The Docker image only starts on one database and does not allow switching
databases at runtime. However, you can and should use several databases on your
postgres container for enabling databases for different usages or development.

The default database name will be the one configured in the variable `DB_NAME`
in `docker-compose.yml` (usually `odoodb`).

So if you just start a new odoo container using:

```
docker-compose run --rm odoo
```

You will work on `odoodb`.

Now let's say you want to work on a database with odoo demo data and no marabunta migration:

```
docker-compose run --rm -e MIGRATE=False -e DEMO=True -e DB_NAME=odoo_demo odoo
```

If you want to use a dump from production restored in a db called prod, you can run:

```
docker-compose run --rm -e DB_NAME=prod odoo
```

## Inspecting databases

### Automated task to list versions

You can list the odoo databases in your Docker volume using the automated
invoke task :

```
invoke database.list-versions
[...]
DB Name              Version    Install date
=======              =======    ============
odoodb               11.2.0     2018-08-05
prod                 11.1.0     2018-07-27
odoo_demo            unknown    unknown
```

Version and install date are stored on `marabunta_version` table of each DB.
As we specified `-e MIGRATE=False` on `odoo_demo`, no Marabunta migration was
executed, thus version and install date are unknown.


### Manual

However you can also inspect the databases manually, and you should also find
your 3 databases :

```
$ docker-compose run --rm odoo psql -l
[...]
                                 List of databases
   Name    |  Owner   | Encoding |  Collate   |   Ctype    |   Access privileges
-----------+----------+----------+------------+------------+-----------------------
 odoo      | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
 odoodb    | odoo     | UTF8     | en_US.utf8 | en_US.utf8 |
 prod      | odoo     | UTF8     | en_US.utf8 | en_US.utf8 |
 odoo_demo | odoo     | UTF8     | en_US.utf8 | en_US.utf8 |
 postgres  | postgres | UTF8     | en_US.utf8 | en_US.utf8 |
 template0 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
 template1 | postgres | UTF8     | en_US.utf8 | en_US.utf8 | =c/postgres          +
           |          |          |            |            | postgres=CTc/postgres
```

And you can work as you want on any of them by changing the `DB_NAME`.


## Backup and restore with dumps

### Create a local dump using automated invoke task

Dump generation is automated by invoke, so the only thing you
have to do is :

```
invoke database.local-dump
```

And a *.pg dump will be generated on your project folder.

Moreover you can select which database you want to dump and change the
destination folder using :

```
invoke database.local-dump --db-name=odoodb --path=~/my_dumps
```

The generated dump will be named as username_projectname_datetime.pg

### Create a local dump and share it on odoo-dump-bags

Dumps are not only great for backups, they are also the easiest way to share a
database with someone else. So if you want to share one of your local database
with your colleagues, the process is totally automated and secured, so all you
have to do is:

```
 invoke database.dump-and-share --db-name=prod-test
```

This will create a dump on your computer (similar as above), then encrypt it
using GPG, and finally push it on https://dump-bag.odoo.camptocamp.ch.

When your colleague did download it, please do not forget to remove it from the
dump bag with :

```
invoke database.empty-my-dump-bag
```

### Create a dump manually

If you have the same `pg_dump` version on your computer than the one used in the
db container (9.5 at time of writing), you can just use your local `pg_dump`
directly on the outgoing port of the db container (see [how to find the
port](how-to-connect-to-docker-psql.md)). Example:

```
$ pg_dump -h localhost -p 32768 --format=c -U odoo --file db.pg odoodb
```

Note : When using `odoo` DB User (role), keep in mind its password is `odoo`

If you have an older version of `postgres-client`, `pg_dump` will refuse to
make a dump. An option is to update your `postgres-client`.  Here is another option using a  `postgres:9.5` one-off container (the `db` container
must be running):

```bash
$ export HOST_BACKUPS=/path/of/hosts/backups  # Where you want to save the backups
$ export PROJECT_NAME=project_name (the prefix of containers, volumes, networks, usually the root folder's name)

$ docker run --rm --net=${PROJECT_NAME}_default --link ${PROJECT_NAME}_db_1:db -e PGPASSWORD=odoo -v $HOST_BACKUPS:/backup postgres:9.5 pg_dump -Uodoo --file /backup/db.pg --format=c odoodb -h db
```

### Restore a dump using container

You can restore any dump without worrying too much by commands from the odoo
container.

First you will have to create an empty database with odoo user as its owner and
giving it a name :
```
docker-compose run --rm odoo createdb -O odoo my_restored_database
```

Then you can use the `pg_restore` command from the odoo container passing the
path of your dump file:
```
docker-compose run --rm odoo pg_restore -p 5432 -d my_restored_database < ~/my_dumps/username_projectname_datetime.pg
```


### Restore using local command

You should always prefer the method above.

If you have the same `pg_restore` version on your computer than the one used in the
db container (9.5 at time of writing), you can just use your local `pg_restore`
directly on the outgoing port of the db container (see [how to find the
port](how-to-connect-to-docker-psql.md)). Example:

```
$ createdb -h localhost -p 32768 -O odoo prod
$ pg_restore -h localhost -p 32768 -O -U odoo -j2 -d prod
```

If you have an older version of `postgres-client`, `pg_restore` will refuse to
restore the dump. An option is to update your `postgres-client`.  Here is another option using a  `postgres:9.5` one-off container (the `db` container
must be running):

```bash
$ export HOST_BACKUPS=/path/of/hosts/backups  # From where you want to restore the backup
$ export PROJECT_NAME=project_name (the prefix of containers, volumes, networks, usually the root folder's name)

$ docker run --rm --net=${PROJECT_NAME}_default --link ${PROJECT_NAME}_db_1:db -e PGPASSWORD=odoo  postgres:9.5 createdb -h db -O odoo prod
$ docker run --rm --net=${PROJECT_NAME}_default --link ${PROJECT_NAME}_db_1:db -e PGPASSWORD=odoo -v $HOST_BACKUPS:/backup postgres:9.5 pg_restore -h db -O -U odoo --file /backup/db.pg -j2 -d prod
```

## Drop a database

Sometimes a database might broken or you simply want to recreate a fresh instance
from scratch, so to drop the `odoodb` database simply use:

```
docker-compose run --rm odoo dropdb odoodb
```

If somehow your image is broken, you can also use your local dropdb command,
but you need to know which port is exposed. So you should ensure your db
container is started:

```
docker-compose up -d db
```

Then you can retrieve the exposed port using:

```
docker-compose port db 5432 | cut -d : -f 2
```

And finally drop it using the port (replace 32768 in this example with the
result from above) and the db name:

```
dropdb -h localhost -p 32768 -U odoo odoodb
```
