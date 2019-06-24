<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# Releases

## Versioning pattern

Our new versions numbering went from 3 to 5 digits, that we'll represent here with:

    R.r.x.y.z

* **R.r** is the Odoo version, i.e. either 10.0, 11.0, 12.0, etc
* **x** is the major project version number. It will stay 0 until going into
  production and will then be incremented to 1. It can be used for major
  evolutions.
* **y** is the minor project version number, This is the number to increment
  for the first release and any new feature added to the project.
* **z** is the patch number, incremented for corrections on production releases
  ONLY.

Most of the developments are done on the `master` branch and a new release on
`master` implies a new `minor` (R.r.x.**Y**.z) version increment.

Should there be an issue with a released image after the tag has been set, a
patch branch is created from the tag and a new release is done from this
branch; the patch number (R.r.x.y.**Z**) is incremented.

For bigger developments done on another branch than `master`, e.g. integrate a
new logistics flow, customized website, etc.. where different PRs are used
targeting this branch, the `major` version (R.r.**X**.y.z) is to increment
when this new dev is going to be merged on `master`


## Release process

In the following order, at the end of a sprint, the release manager will:

* Merge all pending pull requests when possible, and for each corresponding card in Jira set the "Fix Version" field accordingly as well as change the status to "Waiting deploy"

* Ensure that the migration scripts are complete and working (see [upgrade-scripts.md](upgrade-scripts.md#run-a-version-upgrade-again) on how to execute a specific version scripts).

* For projects already used in Production, ensure migration is working in FULL mode. (see [how-to-use-a-prod-db-in-dev.md](how-to-use-a-prod-db-in-dev.md) to get a dump for projects hosted on cloud platform).

* Increase the version number (see [invoke.md](invoke.md#releasebump) for more information)

  ```bash
  invoke release.bump --feature  # increment y number in R.r.x.y.z
  # or --patch to increment z number in R.r.x.y.z
  # or --major to increment x number in R.r.x.y.z
  ```

* The "bump" command also pushes the pending-merge branches to a new branch named after the tag (`pending-merge-<project-id>-<version>`), if needed, this push can be manually called again with

  ```bash
  invoke release.push-branches
  ```

* Do the verifications: migration scripts, [changelog](../HISTORY.rst) (remove empty sections, ...)

* The new version number 'x.y.z' is copied to your clipboard in order to speedup the next commands

* Commit the changes to [changelog](../HISTORY.rst), VERSION, ... on master with message 'Release x.y.z'

* Add a tag with the new version number, copying the changelog information in the tag description

  ```
  git tag -a R.r.x.y.z  # here, copy the changelog in the annotated tag
  git push --tags && git push
  ```

When the tag is pushed on GitHub, Travis will build a new Docker image (as
long as the build is green!) and push it on the registry as `camptocamp/demo_odoo:R.r.x.y.z`

If everything went well it is worth informing the project manager that a new release is ready to be tested on the Minions.


## Patch process

### Quick checklist

1. Create a branch `patch-R.r.x.y.next-z` based from the source tag `R.r.x.y.z` to
   correct
2. Push the branch to the camptocamp repository
3. Create a working branch based on `patch-R.r.x.y.next-z` which include your fix
4. Push your working branch on your fork repository and create a pull request
   on `patch-R.r.x.y.next-z`
5. Ask for reviews, get reviewed, merge
6. Create a release `R.r.x.y.next-z`
7. **Merge the branch `patch-R.r.x.y.next-z` in master (very important to have the
   fix for the next release!)**

You can refer to the more detailed documentation below.

### Short story

Example of branches involving Paul as the Release manager and Liza and Greg as
developers, the current version is `12.0.1.3.2`:

* Liza works on a new feature so she creates a branch for master:

    ```
    git checkout origin/master -b impl-stock-split
    git push liza/impl-stock-split
    ```

* Greg works on a new feature too:
    ```
    git checkout origin/master -b impl-crm-claim-email
    git push greg/impl-crm-claim-email
    ```
* The end of sprint is close, both propose their branches as pull requests in
    `master`, builds are green!
* Paul merges the pull requests, prepares a new release and when he's done, he
    tags `master` with `12.0.1.4.0`
* Paul tests the image `camptocamp/demo_odoo:12.0.1.4.0` and oops, it seems he
    goofed as the image doesn't even start
* Paul corrects the - hopefully - minor issue and prepare a new release for
    `12.0.1.4.1`.
* Liza works on another shiny feature:
    ```
    git checkout origin/master -b impl-blue-css
    git push liza/impl-blue-css
    ```
* And Greg is assigned to fix a bug on the production server (now in `12.0.1.4.1`),
    so he will do 2 things:
    * create a patch branch **from** the production version:
        ```
        git checkout 12.0.1.4.1 -b patch-claim-typo
        git push greg/patch-claim-typo
        ```
    * ask Paul to create a new patch branch `patch-12.0.1.4.2`, on which he will
        propose his pull request
* Paul prepare a new release on the `patch-12.0.1.4.2` branch. Once released, Paul merges `patch-12.0.1.4.2` in `master`.
* At the end of the sprint, Paul prepares the next release `12.0.1.5.0` with the new Liza's feature and so on.

### Detailed instruction

1. Create remote patch branch

    * Figure out target version `number` in format `R.r.x.y.z` (`12.0.1.4.0`) for which
        you need to make patch. It can be version released on production or
        integration or specified by PM. Or maybe other case.
    * Create patch branch from target with name `patch-R.r.x.y.next_z`
        (`patch-12.0.1.4.1`). Where `next_z = z + 1` (`1 = 0 + 1`).
        ```git
        git checkout R.r.x.y.z -b patch-R.r.x.y.next_z
        ```
        example
        ```git
        git checkout 12.0.1.4.0 -b patch-12.0.1.4.1
        ```
    * Push new empty branch to repo.
        ```git
        git push origin patch-R.r.x.y.next_z
        ```
        example
        ```git
        git push origin patch-12.0.1.4.1
        ```
        Where `origin` should be camptocamp project repo

    Alternative you can create `patch-R.r.x.y.next_z` branch on github directly.

2. Create local patch branch

    * Create your local patch branch.
    * Do required changes for patch.
    * Commit your changes.
    * Push your changes to your remote fork repo.
    * Create PR to patch remote project branch.
        ```git
        camptocamp/generated/patch-R.r.x.y.next_z <- <user_name>/generated/<your_patch_branch>
        ```
    * Request PR review in chat to speedup merge.
    * Merge after reviewers approve your changes.

3. Create patch release

    * After merge your PR to remote patch-branch do release.
        Your current branch should be `patch-R.r.x.y.next_z`.
        See [Release process](#release-process) section.

4. **Merge patch-branch to master**

    * **Merge `patch-R.r.x.y.next_z` to `master` to incorporate patch changes
        into master branch.**
