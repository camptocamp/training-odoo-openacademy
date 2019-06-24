<!--
This file has been generated with 'invoke project.sync'.
Do not modify. Any manual change will be lost.
Please propose your modification on
https://github.com/camptocamp/odoo-template instead.
-->
# Automated Docker Images

## Travis deployment

When Travis runs, it builds a Docker image and runs the tests inside it.
If the tests pass, it uploads the image to DockerHub and generate a new test
instance on the [test platform](./odoo-test-platform.md).

## Rancher templates

### Test instances

See [Odoo Test Plaftorm](./odoo-test-platform.md)

### Integration and production instances

The Rancher templates for the integration and production instances are grouped in a project
for the platform:

* https://github.com/camptocamp/odoo-cloud-platform-ch-rancher-templates

## Docker images

Docker images for Odoo are generated and pushed to [Docker Hub](https://hub.docker.com) by Travis when builds are successful.
This push is done in [travis/publish.sh](../travis/publish.sh) which is called by [travis.yml](../.travis.yml) in `after_success` section.

This script will tag docker image with:
 * latest: When the build was triggered by a commit on master
 * `git tag name`: When the build was triggered after a new tag is pushed.
 * a tag generated with the git commit, used by the test instances

To be able to push an image, Travis must have access to your project on Docker Hub.
Please be sure that the [Hub user has been created and configured in
Travis](https://confluence.camptocamp.com/confluence/display/BS/Technical+details+on+creating+new+project)

**From there, each travis successful build on master or on tags will build a docker image and push it to Docker Hub**
