<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# Git-autoshare

A lot of time is wasted during environment setup and project deploy on cloning
of submodules. Especially odoo/odoo and odoo/enterprise

Git-autoshare fixes this problem by creating reference caches for the common
repos locally to avoid downloading them all the time

# Installation

  1. You can install git-autoshare with pip

  ```bash
  $ pip install git-autoshare
  ```

  2. Or install all the requirements for tasks from `odoo/tasks/requirements.txt`

# Configuration

## Config file

To properly work git-autoshare requires a configuration file that, by
default, should be at `~/.config/git-autoshare/repos.yml`. Example of the config
file:

```yml
github.com:
    odoo:
        orgs:
            - odoo
            - camptocamp
            - OCA
    # OCA
    account-analytic:
        orgs:
            - OCA
            - camptocamp
    enterprise:
        orgs:
            - odoo
            - camptocamp
        private: True
```

### Note

As OCA fork is called OCB you have to specify separately from odoo due to how
git-autoshare works

## Environment variables

If you want to change the location of caches or config file, you can specify
environment variable to do that:

### Cache

The cache directory is named git-autoshare where appdirs.user_cache_dir is
(usually `~/.cache/git-autoshare/`). This location can be configured with the
`GIT_AUTOSHARE_CACHE_DIR` environment variable.

### Config file

The default configuration file is named repos.yml where appdirs.user_config_dir
is (usually `~/.config/git-autoshare/`). This location can be configured with the
`GIT_AUTOSHARE_CONFIG_DIR` environment variable.

By default git-autoshare invokes git as `/usr/bin/git`. This can be configured
with the `GIT_AUTOSHARE_GIT_BIN` environment variable. If you are using `hub`,
you should set the path to your hub binary instead.

# Cron

As git-autoshare supports great feature to prefetch those repositories from
your config, you can keep them up-to-date with a cron job. Open a crontab editor

  ```bash
  $ crontab -e
  ```
This will open a crontab file with your default editor. You should schedule a job now.
Crontab support such syntax `minute hour day_of_month month day_of_week command`
example of a job to update repositories every week on monday at 11 a.m.

  ```bash
  0 11 * * 1 /home/<user>/.local/bin/git-autoshare-prefetch --quiet
  ```

:warning: Warnings:

The path must be absolute or you need to add `/home/<user>/.local/bin/`
in your CRON PATH

CRON doesn't load git config. Thus you should add private repositories at the end of
the `repos.yml` file in order that it will fail only after the cron ran. This allows
you to still run manually the `git autoshare-prefetch` manually.
