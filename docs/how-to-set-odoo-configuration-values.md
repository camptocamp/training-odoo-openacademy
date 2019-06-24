<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# How to set Odoo configuration values

The template for the configuration (`openerp.cfg`) is in [the base Docker project image]


Most of the values here are set by environment variables, which looks like:

```
workers = { default .Env.WORKERS "4" }
```

In this example, the number of workers is taken from the `WORKERS` environment
variable and the default values is 4.

Having environment variables is useful to have a different configuration
between different environments (dev, test, ...). This is why the `addons_path`
is directly set in the template and not in environment variables: we always
want the same value for all the environments.

The values of the environment variables can be changed in the
`docker-compose.yml` file, or directly in `docker-compose run -e VARIABLE=value
odoo`.

Read the documentation of [the base Docker project
image](https://github.com/camptocamp/docker-odoo-project) for more information
about the `DEMO` flag and other special variables.
