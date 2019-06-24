<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# How to integrate an open pull request of an external repository

First, ensure that you have installed all `tasks/requirements.txt`.

External addons repositories such as the OCA ones are integrated in the project
using git submodules (see [How to add a new addon repository](./how-to-add-repo.md)).
When we need to integrate a pull request that is not yet merged in the base branch
of that external repository we want to use, we create a consolidated branch that
we push on the fork at github.com/camptocamp.

The list of all pending merges for a project is kept in `pending-merges.d/`.

This directory contains a `.yml` file containing a `git-aggregator` config for
each of the registered submodules, if there are any pending merges at all.

Each submodule has its own pending merges config in a separate file.
Naming pattern is `pending-merges.d/<submodule-name>.yml`, except for `odoo`
source itself, which would be referred to as `pending-merges.d/src.yml`.


## Adding a new pending merge

Beware with pending merge branches. It is easy to override a previously pushed
branch and have a submodule referencing a commit that no longer exists.

1. Run:

  ```bash
  invoke submodule.add-pending <your-pr-link>
  ```

  This will add a corresponding entry in a proper submodule's file found under
  `pending-merges.d/` refresh a list of remotes and create a file from a
  template if it is necessary.

  Example of pending merges file:

  ```yaml
  # Given that this file is for `sale-workflow` repo,
  # it resides in `pending-merges.d/sale-workflow.yml`
  ../odoo/external-src/sale-workflow:
    remotes:
      OCA: https://github.com/OCA/sale-workflow.git
      camptocamp: https://github.com/camptocamp/sale-workflow.git
    merges:
      - OCA 12.0
      # comment explaining what the PR does (42 is the number of the PR)
      - OCA refs/pull/42/head
    target: camptocamp merge-branch-XXXX-master
  ```

  TIP: if your goal is to integrate a pull request,
  you can use a shorthand like `upstream/repo-name#<pr-number>`.
  For instance, to integrate the PR `https://github.com/OCA/sale-workflow/pull/42`:

  ```bash
  invoke submodule.add-pending OCA/sale-workflow#42
  ```

2. Rebuild and push the consolidation branch for the modified branch:

  ```bash
  invoke submodule.merges odoo/external-src/sale-workflow
  ```
  TIP: you will be prompted for execution of this step after you're done with step 1.

3. Commit the changes and create a pull request for the change.

  Notice that `.gitmodules` file is being synchronized if either:

  - pending merge is being added to the repo w/o pending merges at the moment
    in this case, submodule's remote is set to `camptocamp`

  - after removal of last pending merge (excluding `OCA 12.0` or alike)
    then remote is being set to current repo's parent (assuming that's a fork)
    to resolve the parent, a call Github API is issued


## Removing a pending merge

Similar to the procedure for adding a pending merge `remove-pending` task
allows you to delete a pending merge.

1. Call `invoke submodule.remove-pending <your-pr-link>`
2. Make a decision whether to update your submodule (again, you'll be prompted)
3. Commit changes in the submodule

If the file contains no more pending merges nor patches it's deleted.


## Checking pending merge status

Check pending PRs

```bash
invoke submodule.show-prs [path/to/repo]
```

Check only closed

```bash
invoke submodule.show-closed-prs [path/to/repo]
```

Check closed and get rid of them

```bash
invoke submodule.show-closed-prs --purge-closed [path/to/repo]
```

In all the cases if you omit the repo path
you'll check in all submodules with pending merges.


## Merging only one distinct commit (cherry-pick)

Sometimes you only want to merge one commit into the consolidated branch (after
merging pull requests or not). To do so you have to add a `shell_command_after` block
in the corresponding section. Here is an example:

  ```yaml
  ../odoo/external-src/enterprise:
    remotes:
      odoo: git@github.com:odoo/enterprise.git
      camptocamp: git@github.com:camptocamp/enterprise.git
    merges:
      - odoo <branch-name or initial commit>
    target: camptocamp merge-branch-XXXX-master
    shell_command_after:
      # Commit from ? Doing what ?
      -  git am "$(git format-patch -1 6563606f066792682a16936f704d0bdf4bc8429f -o ../patches)"
  ```

In the previous example the commit numbered 6563606... is searched in all the remotes of the section,
then a patch file is made and apply to the consolidated branch.
A file containing the patch will be saved in the patches directory and needs to be added in the commit
of the project.

Note: you can add this construction from your CLI, there's an invoke task for you:
`invoke submodule.add-pending https://github.com/upstream/repo/[tree]/<commit SHA>`

In the example above, this command should be sufficient:
`invoke submodule.add-pending https://github.com/odoo/enterprise/tree/6563606`.


## Notes

### Consolidation branches

For each repository, we maintain a branch named
`merge-branch-<project-id>-master` (look in `pending-merges.d/<repo-name>.yml` for the
exact name) which must be updated each time the pending merges
reference file has been modified.

When a release is bumped a new branch
`merge-branch-<project-id>-<version>` to ensure we keep a stable branch.

For the sake of keeping multiple consolidated branches available at the same time
when you are developing (and you push a branch for a pull request for instance)
you'll get a new branch matching the pattern

`merge-branch-0000-<current branch name>-<SHA of HEAD>`.


NOTE: invoke tasks will create and update (and push if necessary) these branches automatically for you.
