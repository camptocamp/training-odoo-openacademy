<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# How to connect to psql in Docker

We'll describe 3 ways to connect to `psql` in the Docker container.

## Use the psql client of the Odoo container

In the Odoo container, there is a `psql` client so you can start an one-off
container running it:

```
docker-compose run --rm odoo psql
```

It will automatically connect on the current database, but you can
specify another database if wanted:

```
docker-compose run --rm odoo psql other_db
```

## Use the random docker port of the db container and your local `psql` client

```
PGPASSWORD=odoo psql -h localhost -p $(docker-compose port db 5432 | cut -d : -f 2) -U odoo odoodb
```

## Set an explicit fixed port

Edit `docker-compose.yml` or create your own configuration file, but put a fixed port for the Postgres server:

```
db:
  ...
  ports:
    - "5440:5432"
```

And connect to this fixed port:

```
PGPASSWORD=odoo psql -h localhost -p 5440 -U odoo odoodb
```
