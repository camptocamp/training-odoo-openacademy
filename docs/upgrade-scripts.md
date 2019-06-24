<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# Upgrade scripts

## Stack

The upgrade system uses the following tools:

* [Marabunta](https://github.com/camptocamp/marabunta)
* [Anthem](https://github.com/camptocamp/anthem)

Marabunta is an orchestrator for running the migrations. Anthem runs Python
scripts provided with an Odoo environment. More details below.

Those tools are integrated in the image and can be configured using environment
variables. See the [Docker Odoo Project
readme](https://github.com/camptocamp/docker-odoo-project/#environment-variables)
for details on the variables.

## Marabunta

Marabunta expects a file named `migration.yml` in the `odoo` directory.
This `yaml` file contains the upgrade instructions for every version.
It creates a `marabunta_version` table in the database, containing the
installed versions, and run the upgrade scripts when a version is missing.

The upgrade instructions are composed of:
 * A list of commands executed before the installation/upgrade of the addons
 * The installation/upgrade of a list of addons
 * A list of commands executed after the installation/upgrade of the addons

Further, we can configure *modes* which allow to run additional commands when a
mode is activated (e.g. the 'sample' mode would load some sample data).

See [an example of yaml
file](https://github.com/camptocamp/marabunta/blob/master/marabunta/parser.py#L14-L61)

## Anthem

Anthem is a replacement for `oerpscenario`, but the scripts are written with
straight Python.

Simple example:

```python

import anthem
from anthem.lyrics.records import create_or_update


@anthem.log
def setup_company(ctx):
    """ Configuring company """
    company = ctx.env.ref('base.main_company')
    company.name = 'Rainbow Holding'


@anthem.log
def create_partners(ctx):
    """ Creating partners """
    names = [('Khiank Mountaingut', '__scenario.partner_1'),
             ('Kher Fernthorn', '__scenario.partner_2'),
             ('Sheing Coaldigger' '__scenario.partner_3'),
             ]
    for name, xmlid in names:
        create_or_update('res.partner', xmlid, {'name': name})


def main(ctx):
    setup_company(ctx)
    create_partners(ctx)

```

As you can see, each function takes a `ctx` argument. The `ctx` contains an
Odoo environment (`env`) which can be used exactly as we would do in Odoo.

Also, Anthem includes predefined functions for the common tasks (load csv
files, upsert a record with a xmlid, ...), called `lyrics`.

## Use cases

### Calling a song in migration.yml

Anthem takes the function we want to run as argument.
The syntax of the argument is `module-path::function-name`, where *module-path*
is the Python path of the module. So let's say we have a `main` function in
`songs/install/post.py`, the argument would be: `songs.install.post::main`.

In the `migration.yml` file, it means we have to add a pre/post operation in
the current version:

```yaml
    - version: 12.0.0
      operations:
        post:
          - anthem songs.install.post::main
```

### Run a single Anthem's song

As demonstrated in the previous section, anthem takes the function we want to
run as argument. So we can run a container the command line to execute the
desired function:

```
$ docker-compose run --rm odoo anthem songs.sample.data_sample::create_partners
```

### Run a version upgrade again

By default, Marabunta won't execute a migration upgrade twice.
You can force it to execute an upgrade again with the `MARABUNTA_FORCE_VERSION`
environment variable:

```
$ docker-compose run --rm -e MARABUNTA_FORCE_VERSION=12.0.0 odoo
```

With the command above, odoo will be run at the end of the migration.
You could also run only `migrate` which will exit the container once done.

```
$ docker-compose run --rm -e MARABUNTA_FORCE_VERSION=12.0.0 odoo migrate
```

### Execute the upgrade for a given mode

Modes allow to run additional commands.

```yaml
  versions:
    - version: 12.0.0
      operations:
        pre:
          - anthem songs.install.pre::main
        post:
          - anthem songs.install.post::main
      addons:
        upgrade:
          - account
      modes:
        full:
          operations:
            pre:
              - anthem songs.install.pre_full::main
            post:
              - anthem songs.install.data_full::main
        sample:
          operations:
            post:
              - anthem songs.sample.data_sample::main
          addons:
            upgrade:
              - dev_addon
```

In the example above, we have 2 modes: `full` and `sample`. We use them to spawn
different types of instances, `sample` might be used for a development instance
or a test server, the full one for the production (possibly with a lot of
data).

Mode's commands are always executed after the main ones, the addons lists are merged.
The order of execution when no mode is used will be:

1. `anthem songs.install.pre::main`
2. `-i account` (or `-u` if it is already installed)
3. `anthem songs.install.post::main`

When the sample mode is used (`MARABUNTA_MODE=sample`):

1. `anthem songs.install.pre::main`
2. `-i account,dev_addon` (or `-u` if it is already installed)
3. `anthem songs.install.post::main`
4. `anthem songs.sample.data_sample::main`

When the full mode is used (`MARABUNTA_MODE=full`):

1. `anthem songs.install.pre::main`
1. `anthem songs.install.pre_full::main`
2. `-i account` (or `-u` if it is already installed)
3. `anthem songs.install.post::main`
4. `anthem songs.install.data_full::main`

Usually, the `MARABUNTA_MODE` will be set in the `docker-compose.yml`
composition files, but you can also set in when running a container:

```
$ docker-compose run --rm -e MARABUNTA_MODE=sample odoo
```

### Disable the migration

When you don't want the migration to run at all, you can disable it with:

```
$ docker-compose run --rm -e MIGRATE=False odoo
```

### Upgrade all modules

If you upgrade `odoo/src` and any other `odoo/external-src/*` repos,
you might want to update all the installed modules.
You should just declare `base` in the addons section, like this:

```yaml
  versions:
    - version: 12.0.1
      addons:
        upgrade:
          - base
```

### Load heavy files

If you have to import huge files (eg: stock.location)
you should delegate import to `importer.sh`.

```python
@anthem.log
def setup_locations(ctx):
    deferred_import(
        ctx,
        'stock.location',
        'data/install/stock.location.csv',
        defer_parent_computation=True)
[...]
@anthem.log
def location_compute_parents(ctx):
    deferred_compute_parents(ctx, 'stock.location')
```

```yaml
modes:
  full:
    operations:
      post:
        - anthem songs.install.data_full::main
        #### import heavy stuff
        - importer.sh songs.install.inventory::setup_locations /odoo/data/install/stock.location.csv
        - anthem songs.install.inventory::location_compute_parents
```

#### WARNING

If you want to import records w/ many parent/children relations (like product categories) it might fail.
The import is done in parallel so is not granted that you'll have parents imported before children. ATM ;)
