<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# How to initialize a migration project

## Initialization steps

### Create the new branch

First step is to create the new branch for the new version.

In the past, the branch was created from master and took the name of the new version.
By example `14.0` for a migration to version 14.

Now, we create a project from scratch and retrieve only the needed material to propose a clean database for the
migration process:

* Use of cookiecutter normally to create a new project with the same parameters than the previous version (see .cookicutter)
    * `cookiecutter git@github.com:camptocamp/odoo-template.git`
    * Say `yes` to the migration question (because it is !)
* Then checkout and enter the new branch with the desired new version on this new project (you should have the right remote reporitory to point to but double check it)
    * git checkout -b 14.0
    * git push --set-upstream origin 14.0
    * invoke submodule.init
    * invoke submodule.update

! this is a "bare instance".

For next steps:

* Don't commit directly on that new branch, but propose a pull request on it.
* Use different commit for each action to help reviewers understand your changes.

### Retrieve some of the needed configuration from the previous version

While database is sent to upgrade platform you can continue with project setup. And also it's a good practice to test if build can be done successfully.
* docker-compose build odoo
* docker-compose run --rm -p 8069:8069 odoo odoo --workers=0

Then you need to check and update company info, this is configured at setup step listed in migration.yml
* in `songs/install/pre.py`:
  * Get the admin password (the hash) from previous version to the new one 
  * Check that company configuration is same as the previous one
* Copy the old logo to the new project if not changed (ask for the new one if needed)
  * Then commit it as `Update company, logo and password from previous project version`
* Retrieve the `migration.yml` addons installed and put them in the `odoo/migration_db/addons_to_uninstall.py` file inside the `UNINSTALL_MODULES_LIST` variables
  * Don't add the default modules added in the base configuration (including `database_cleanup`)
  * put local modules in the section `# Specific modules not migrated yet, but we don't know if we want`
  * put OCA modules in the section `# OCA modules not available yet, but we don't know if we want`
  * keep the submodule path comment of modules please (i.e. `# OCA/server-tools`)
  * Then commit it as `Add modules from previous project version to uninstall`

It's a bare instance, you are ready to start your migration !

A very useful command to migrate a specific addon by first retrieving its commits history is:

`$ git format-patch --keep-subject --stdout origin/14.0..origin/master -- odoo/local-src/{ADDON} | git am -3 --keep`

### After Go-Live

* Move the master branch to a new one called by the previous version of the project (i.e. `master` to `XX.0`)
* Rename the new version branch to master (i.e. `XX.0` to `master`)
* Et voilà

Finally, we have a branch for the old version and master for the new version.
