<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# How to build quickly a migration project

## Step list to do:

:warning: _This step list is a first version, must be checked, confirmed and fixed next time we will use it.
For any question ping #bs-migrations in slack

- [ ] Retrieve customer dump with link on [Migrated database confluence](https://confluence.camptocamp.com/confluence/display/BS/Migrated+database#Migrateddatabase-Howtorestoreamigrateddatabase)
- [ ] `unzip upgraded_$DUMP_NAME.pg.zip`
- [ ] `lpass logout` :warning: _to not re-create entry in lastpass_
- [ ] `export MIGRATION_VERSION='XX.0'`
- [ ] `git clone git@github.com:camptocamp/demo_odoo.git demo_odoo_$MIGRATION_VERSION` _to not be in conflict with the submodule_
- [ ] `cd demo_odoo_$MIGRATION_VERSION`
- [ ] `git checkout -b $MIGRATION_VERSION`
- [ ] `git push --set-upstream origin $MIGRATION_VERSION`
- [ ] Retrieve the mandatory submodule you can use this command to put in all the actual module to one `gitmodules_tmp` file
```shell
git config --file .gitmodules --get-regexp path | awk '{ print $2 }' > gitmodules_tmp
```
- [ ] `cat odoo/migration.yml | grep "          -" | sort -u | grep -v 'anthem' | grep -v 'version' | grep -v 'psql' | grep -v 'stop-after-init' | cut -c12-200 > module_installed` _to retrieve installed module in the migration.yml_ :warning: *For common migration file number of space in the grep will be ok but be careful of the result*
- [ ] `DO_SYNC=1 invoke project.sync --version=stable && invoke project.sync` _to upgrade the project with the last odoo-template_
- [ ] Check the list of the local directory you should keep
- [ ] Check the list custom [requirements](../odoo/requirements.txt) you should keep
- [ ] Use this task [invoke.md](invoke.md#migrateconvert-project) with the previous list to add in `--paths-to-keep=`
    * Most of cases, the command will be: `invoke migrate.convert-project --paths-to-keep=odoo/local-src,odoo/data/images/company_main_logo.png,gitmodules_tmp,module_installed`
- [ ] check in previous `gitmodules_tmp` the dependency to add in `.gitmodules` and check if all submodules is needed
- [ ] Update submodule repositories with [Add a new addons repository with invoke](how-to-add-repo.md#use-invoke-task)
- [ ] `docker-compose build`
- [ ] `docker-compose run --rm odoo createdb odoodb`
- [ ] `docker ps --filter "name=demo_odoo"` _retrieve the docker port to restore the db_
- [ ] `psql --file dump.sql -h localhost -p $DOCKER_PORT -d odoodb -U odoo` _to restore the migrated dump_
- [ ] `docker-compose run --rm odoo createdb odoodb_migration -T odoodb` _do a template to use if you have issue in the start_
- [ ] Modify the [migration.yml](../odoo/migration.yml) with the installable modules list you can use :
```shell
while read p; do
  list=$(find . -type d  -name $p)
  if [ $list ]; then
    echo "          - $p";
  else
    echo "          # - $p       # Not available yet";
  fi
done <module_installed
```
Don't forget to do this properly with the correct section
- [ ] Search in the OCA if there is any migration PR for unavailable modules
- [ ] Search if the unavailable core module was not renamed if yes put this in [pre.py](../odoo/songs/migration/pre.py) in `rename_modules` method
- [ ] Add the list of module to uninstall (we don't want + not available yet) in [uninstall.py](../odoo/songs/migration/uninstall.py#L8)
- [ ] `docker-compose run --rm -e MARABUNTA_MODE=migration -e DB_NAME=odoodb odoo rundatabasemigration > /tmp/log_database_migration_demo_odoo_$(date +"%Y_%m-%d_%H_%M").log 2>&1 ` _start the database migration and put the log in one tmp file. You can follow the log in other terminal with_ `tail -f /tmp/log_database_migration_demo_odoo_$(date +"%Y_%m-%d_%H_%M").log`
- [ ] `docker-compose run --rm -e DB_NAME=odoodb-sample -e MARABUNTA_MODE=sample odoo odoo --stop-after-init` _need for the next task_
- [ ] `invoke migrate.check-modules odoodb_migration odoodb odoodb-sample` _to check the modules list like you can see in_ [invoke migrate check modules task](invoke.md#migratecheck-modules)
- [ ] you will retrieve databases modules json
* Modules in migrated database _(noting to do just info)_
* Modules in full database _(noting to do just info)_
* Modules in migrated database, but not in full database
    * - [ ] add to uninstall.py
* Modules in full database, but not in sample database
    * - [ ] if `installed` add on migration.yml
    * - [ ] if `to upgrade` add to uninstall.py
* Modules in sample database, but not in full database
    * - [ ] add on migration.yml cause auto installed with the comment `# auto installed module`
- [ ] Check the error and report in the card
- [ ] If the run is ok check the instance interface
