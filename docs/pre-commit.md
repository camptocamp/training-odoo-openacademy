<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# pre-commit

This project uses [pre-commit](https://pre-commit.com) to run some checks when
you run a `git commit` command.

Install it on your workstation:

    $ pip install pre-commit --user

Then, at the root of the project:

    $ pre-commit install

It will install all the hooks declared in the configuration file
`.pre-commit-config.yaml`.

## Tools used

Pre-commit will use these tools on the modified files:

* [flake8](http://flake8.pycqa.org) to check the code style (cfg file: `./.flake8` )
* [pyupgrade](https://github.com/asottile/pyupgrade) to upgrade the code with
  new syntaxes (e.g. `%` string formatting will be upgraded to use `.format(...)`)
* [black](https://black.readthedocs.io) to automatically format the code (cfg file: `./pyproject.toml`)
* [isort](https://isort.readthedocs.io) to sort the import statements automatically (cfg file: `./.isort.cfg`)

## How it works

Each time you execute `git commit`, `pre-commit` will perform some commands
(called hooks) to check the good health of the change you are committing (only
files modified in the commit are checked).
If a hook fails (e.g. `flake8`), the commit operation doesn't occur, and you
have to fix your code before committing again.

Some hooks, such as `black`, `pyupgrade`, are
configured to format the code directly, so it's normal that your first commit
operation may fail if your code didn't meet the format expected by these tools.
If this happens, you can run `git diff` to check the code reformatted, and just
re-run your previous `git commit` command as before to make the commit really
happens this time.
In other words the developer didn't need anymore to focus on formatting the
code, these tools will handle this, ensuring that the whole code base will
follow the same format.

/!\ If for some reason you want to bypass a `pre-commit` hook when committing,
set the `SKIP` environment variable with the list of hooks separated by a
comma:

    $ SKIP=black,flake8 git ci -m "I rule the world!"

Of course, this should not happen in a wonderful world!

## Is the whole repository concerned by pre-commit?

`pre-commit` itself only run its hooks on the files of the root repository, so
submodules are not impacted.

That said, some hooks like `black` and `flake8` are configured to exclude
some directories from their scope (`.git`, `.eggs`, `.venv`, ...).

## Integration of pre-commit on existing projects

Before syncing the project with `odoo-template`, the `.sync.yml` file needs to
be updated manually to include the new configuration files:

```yaml
 sync:
   include:
     - ./.cookiecutter.context.yml
+    - ./.flake8
+    - ./.isort.cfg
+    - ./.pre-commit-config.yaml
+    - ./pyproject.toml
     - ./tasks/*
     - ./docs/*
     - ./travis/docker-compose.yml
```

Then sync the project to get the `pre-commit` integration.

You also have to update manually the `.travis.yml` file to integrate
`black` which requires Python 3.6 and change the way others tools are run
(compare with the `.travis.yml` file available in `odoo-template`).

To get Travis CI green when integrating the first time our `pre-commit`
configuration in a project, you have to apply all the hooks manually on all the
existing code base.

Do not forget to initialize `pre-commit` for this project:

    $ pre-commit install

Then run the hooks:

    $ pre-commit run --all-files

Commit, you will see `pre-commit` running again all the checks:

    $ git ci -a -m "Running pre-commit hooks on existing sources"

Push, and you are done.

NB: some manual intervention may be necessary at each step. For instance, isort
may fail if there is comments in the import statements, or be in conflict
with black (if you fix one, the other fails...). In such case you will have to
find the optimal solution to make them happy.
