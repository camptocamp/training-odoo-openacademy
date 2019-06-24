<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# Backup and restore Docker Volumes

## Backup the db and filestore (as volumes)

```bash
$ export HOST_BACKUPS=/path/of/hosts/backups  # Where you want to save the backups
$ export DATAODOO_VOLUME=project_data-odoo  # Exact name to find with 'docker volume ls'
$ export DATADB_VOLUME=project_data-db  # Exact name to find with 'docker volume ls'

$ docker run --rm -v "$DATAODOO_VOLUME:/data/odoo" -v $HOST_BACKUPS:/backup debian tar cvzf /backup/backup-dataodoo.tar.gz /data/odoo
$ docker run --rm -v "$DATADB_VOLUME:/var/lib/postgresql/data" -v $HOST_BACKUPS:/backup debian tar cvzf /backup/backup-datadb.tar.gz /var/lib/postgresql/data
```

## Restore the db and filestore (as volumes)

```bash
$ export HOST_PROJECT=/path/of/hosts/project  # Where your docker-compose.yml is
$ export HOST_BACKUPS=/path/of/hosts/backups  # Where you want to save the backups
$ export DATAODOO_VOLUME=project_data-odoo  # Exact name to find with 'docker volume ls'
$ export DATADB_VOLUME=project_data-db  # Exact name to find with 'docker volume ls'

$ cd $HOST_PROJECT
$ docker-compose stop

$ docker volume rm $DATAODOO_VOLUME
$ docker volume rm $DATADB_VOLUME

$ docker run --rm -v "$DATAODOO_VOLUME:/data/odoo" -v $HOST_BACKUPS:/backup debian bash -c "tar xvzf /backup/backup-dataodoo.tar.gz"
$ docker run --rm -v "$DATADB_VOLUME:/var/lib/postgresql/data" -v $HOST_BACKUPS:/backup debian bash -c "tar xvzf /backup/backup-datadb.tar.gz"
```

## Backup and restore with dumps

This section has been moved to [backup-and-restore-with-dumps](docker-and-databases.md#backup-and-restore-with-dumps).
