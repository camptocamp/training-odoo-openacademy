<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# How to use a PROD DB in DEV mode

## Get a dump locally

If you already have a local dump on your computer, you can skip this section.
If the project is not hosted on our cloud-platform, you should ask a dump to the support team or the project manager.

### From odoo-dump-bag

1. > Use [invoke task](../docs/invoke.md#databasedownload_dump) **or** Connect to https://dump-bag.odoo.camptocamp.ch and retrieve the dump using `aws`.


2. > Then skip to the next section.

### Generate a dump

This is to be used only in case you can't get a dump from odoo-dump-bag

1. Connect to production replication server on odoo-platform-none-db-replication

    Make sure you're in C2C VPN and open a terminal.

    ```
    odoo-platform-none-db-replication 5555
    ```

    This will create a connection to DB server on localhost:5555

    * Should you need a dump from Integration, use : `odoo-platform-none-int-db 5555`
    * Should you need a dump from Production, use : `odoo-platform-none-db 5555`

2. Create and download the dump

    Open a second terminal.

    ```
    pg_dump --format=c -h localhost -p 5555 -U old_dream_6085 old_dream_6085 -O --file /path/to/backups/demo_odoo-$(date +%Y-%m-%d).pg
    ```

    Replace DB NAME and user with the names of your project DB.

## Restore and use the production dump

Now that you have a production DB dump on your computer, you want to load it so you can start a Docker composition.

1. Create a new database :

    ```
    docker-compose run --rm odoo createdb -O odoo prod
    ```

    Should you already have a DB called prod you can either use another name or drop it using :

    ```
    docker-compose run --rm odoo dropdb prod
    ```

2. Load the production dump :

    ```
    docker-compose run --rm odoo pg_restore -p 5432 -d prod < /path/to/backups/demo_odoo-$(date +%Y-%m-%d).pg
    ```

3. Now you can start Odoo setting DB_NAME to prod :

    ```
    docker-compose run --rm -e DB_NAME=prod -p 8069:8069 odoo odoo --workers=0
    ```

## Notes

* [How to work with several databases](./docker-and-databases.md#working-with-several-databases)
* [How to backup and restore a dump](./docker-and-databases.md#backup-and-restore-with-dumps)
