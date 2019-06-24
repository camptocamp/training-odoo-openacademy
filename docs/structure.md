<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# Structure

At the root level, there are mainly files related to docker-compose, Travis, Rancher and the project documentation.

When we build a Docker image, all the things below are copied *inside* the image. When developing, they are shared with volumes so we can work without having to make a new build every time we modify one file.

The implementation of odoo is in the [subfolder odoo](../odoo) which is broken down as:

**[Dockerfile](../odoo/Dockerfile)**

The Dockerfile used to build the Odoo custom image for this project.
It can be customized to [install dependencies](./how-to-add-dependency.md)

**[data/](../odoo/data)**

Directory used to hold files that'll be used by scenario / upgrade scripts to load data in Odoo. It might be images, CSV files, ... The files concerning the installation go in `install`, the ones used for loading a sample dataset go in `sample`.

**[songs/](../odoo/songs)**

Contains the setup and upgrade stripts used for the setup and the migration of the databases.
It itself contains the following subdirectories: **install** which holds the installation scripts, **sample** for the steps used only when using an excerpt of the data for dev/test and **upgrade** will be used for migration steps between releases after the go-live.

**[src/](../odoo/src)**

This is where the Odoo (/OCA) source code is located.
That's a git submodule.

**[external-src/](../odoo/external-src)**

This is where external addons repositories (such as OCA's ones) are added using
git submodules. Each new repository must be added to the `Dockerfile` , see
[How to add a new addons repository](./docs/how-to-add-repo.md).

**[local-src/](../odoo/local-src)**

Customization addons local to this customer are stored here, directly in this
git repository.
