<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# How to setup a migration project

Summary:

* [Build steps](#build-steps)
* [Tools/Scripts to help the developer](#toolsscripts-to-help-the-developer)
* [Requirements/dependencies](#requirementsdependencies)

---

## Build steps

1. [Reset state for all modules](#reset-state-for-all-modules)
2. [Fix attachments path](#fix-attachments-path)
3. [Rename modules](#rename-modules)
4. [Update moved models](#update-moved-models)
5. [Update moved fields](#update-moved-fields)
6. [Remove custom views/filters/exports](#remove-custom-viewsfiltersexports)
7. [Restore initial state for all modules](#restore-initial-state-for-all-modules)
8. [Install/Update all modules](#installupdate-all-modules)
9. [Uninstall modules](#uninstall-modules)
10. [Clean the database](#clean-the-database)
11. [Clean unavailable modules](#clean-unavailable-modules)

All these steps are launched from dedicated Marabunta migration files:

* [migration_core.yml](../odoo/migration_db/migration_core.yml)
* [migration_external.yml](../odoo/migration_db/migration_external.yml)
* [migration_local.yml](../odoo/migration_db/migration_local.yml)
* [migration_cleanup.yml](../odoo/migration_db/migration_cleanup.yml)

### Defining the uninstalled modules

To allow scripts to correctly handle the module uninstallation,
you need to configure the following list in inside
[migration_db/addons_to_uninstall.py](../odoo/migration_db/addons_to_uninstall.py).


### Reset state for all modules

In migrated database:

* all core modules installed in source version have the state `installed`
* all OCA/specific modules installed in source version have the state `to upgrade`
* all new core modules to install have the state `to install`

We can't install/update a module unavailable in target code source.
And for few modules, we need to play scripts to fix/migrate data before updating modules.

So, we need to change the state of all these modules to non-existing state such
as Odoo will load its registry without trying to install/update modules
(raising no error), and thus allowing to play our own scripts without problems
in pre steps.

This is why in each migration phase (core/external/local/cleanup) we are disabling
modules to install/upgrade in `pre` and re-enabling them at the end once the
`anthem` commands (which loads the Odoo registry) have been called.

_Implementation_: [migration_db/songs/generic/disable_addons_upgrade.sql](../odoo/migration_db/songs/generic/disable_addons_upgrade.sql)

### Fix attachments path

In migrated database, we have 2 types of attachments:

* attachments stored directly in database in binary mode
* attachments stored in filestore

For filestore attachments,
it's necessary to customize the file path depending of the hosting.

With S3/SWIFT hosting,
the bucket/container name must be added at the beginning of the path.

_Implementation_: [migration_db/songs/generic/core.py](../odoo/migration_db/songs/generic/core.py)
in function `fix_path_on_attachments`.

### Rename modules

Some specific/OCA modules can be renamed between source and target version.
In this case, the module metadata must be updated before launching
the update of all modules to avoid build failures or loss of data.

By using `openupgradelib.openupgrade.update_module_names` you don't need to
update the models contained in the renamed modules, when the module is renamed,
all the models, fields, etc. will be renamed too. You will use it mainly in the
following places:

* [migration_db/songs/external/](../odoo/migration_db/songs/external/)
* [migration_db/songs/local/](../odoo/migration_db/songs/local/)

### Update moved models

Some models can be moved in other modules between source and target version.
So we need to update the models metadata before launching
the update of all modules to avoid build failures or loss of data.

You are encouraged to use `openupgradelib.openupgrade.rename_xmlids` in
conjunction with `openupgradelib.openupgrade.rename_models` (if needed)
functions in the following places:

* [migration_db/songs/external/](../odoo/migration_db/songs/external/)
* [migration_db/songs/local/](../odoo/migration_db/songs/local/)

### Update moved fields

For the fields moved in another module between source and target version,
you must update the fields metadata before launching
the update of all modules to avoid build failures or loss of data.

You are encouraged to use `openupgradelib.openupgrade.update_module_moved_fields`
function in the following places:

* [migration_db/songs/external/](../odoo/migration_db/songs/external/)
* [migration_db/songs/local/](../odoo/migration_db/songs/local/)

### Remove custom views/filters/exports/cron

Some records like views, filters and exports are created by users.

Problem is: Odoo does not migrate them,
hence you will end up with a lot of possibly broken records of the average user
(admin user is always a special case).

The best way to fix this is to remove all custom views, filters and exports.
The ones that were created by modules will be re-created by updating `base` module.

_Implementation_: [migration_db/songs/generic/core.py](../odoo/migration_db/songs/generic/core.py)
in functions:

* `remove_all_custom_views`
* `remove_all_custom_filters`
* `remove_all_custom_exports`

### Restore initial state for all modules

In first step of the build, we define non-existing state for modules to install/update.

Before updating all modules we want to restore initial state for these modules.

For modules we will uninstall later in the build,
we directly define the `uninstalled` state to avoid to update them for nothing.
And also, because some of these modules are now unavailable.

_Implementation_:

* [migration_db/songs/generic/enable_addons_upgrade.sql](../odoo/migration_db/songs/generic/enable_addons_upgrade.sql)
* [migration_db/songs/generic/uninstall.py](../odoo/migration_db/songs/generic/uninstall.py)
  * Function `update_state_for_uninstalled_modules`

### Install/Update all modules

In the migration build, new modules we want to install must be listed in one
of the following files depending on their origin:

* [migration_db/migration_core.yml](../odoo/migration_db/migration_core.yml)
* [migration_db/migration_external.yml](../odoo/migration_db/migration_external.yml)
* [migration_db/migration_local.yml](../odoo/migration_db/migration_local.yml)

in section `addons/upgrade`.

Addons which were already installed in the previous version will be upgraded
anyway, so it is not mandatory to list them in the files above.

At the end of the build,
be sure that the list of installed modules is the same
for a migrated database
than for a « from scratch » database (with marabunta mode `sample`).

### Uninstall modules

In target version,
if we don't want to keep some modules previously installed in source version,
we must uninstalled them to allow Odoo to remove all their metadata/data.

The source code for these modules is not required to uninstall them.

_Implementation_: [migration_db/songs/generic/uninstall.py](../odoo/migration_db/songs/generic/uninstall.py)
in function `uninstall_modules`.

### Clean the database

In migration process, a lot of metadata/data persist in database
even if the origin module have been uninstalled.

The following data can be cleaned:

* models
* columns/fields
* tables
* models data
* menus

See module `database_cleanup` to see what is exactly cleaned for each item.

_Implementation_: [migration_db/songs/generic/cleanup.py](../odoo/migration_db/songs/generic/cleanup.py)
in function `database_cleanup`.

### Clean unavailable modules

A lot of available modules not installed in source version
are still in the modules list of the target version,
but are now unavailable (because not updated for the new version).

These modules must be deleted from the list of modules.

_Implementation_: [migration_db/songs/generic/cleanup.py](../odoo/migration_db/songs/generic/cleanup.py)
in function `clean_unavailable_modules`.

## Tools/Scripts to help the developer

### Check fields

In migration build,
if a field is moved from a module to another,
the column/data can be lost during the process.

A script is available to check if the migrated database contains fields
which must be moved into another module.

This script will help you to know which fields you must move
to be sure to not lose datas during the process
(you will add this fields in the step [Update moved fields](#update-moved-fields)).

To launch the script, it's necessary to:

* be in `dev` environment
* launch the build with environment variable: `MIGRATION_CHECK_FIELDS`

:warning: **Be careful**, this script is here to help the developper,
but to be sure that no data have been lost, the best way is to test the migration.

_Implementation_:

* [migration_db/songs/generic/check_fields.py](../odoo/migration_db/songs/generic/check_fields.py)

### Invoke task to help to determine modules to install/uninstall

See documentation of task:
* [invoke.md](invoke.md#migratecheck-modules)

## Requirements/dependencies

* Uncomment the `openupgradelib` import in [requirement.txt](../odoo/requirement.txt)
* Install the module `database_cleanup` in [migration_db/migration_external.yml](../odoo/migration_db/migration_external.yml)
  * Repository OCA for this module is `server-tools`
