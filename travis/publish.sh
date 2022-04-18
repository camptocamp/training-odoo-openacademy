#!/bin/bash -e
# This file has been generated with 'invoke project.sync'.
# Do not modify. Any manual change will be lost.
# Please propose your modification on
# https://github.com/camptocamp/odoo-template instead.

local_dir="$(dirname "$0")"

function deploy {
    local tag=$1

    echo "Pushing image to GitHub Packages ghcr.io/${TRAVIS_REPO_SLUG}:${tag}"
    docker tag ${GENERATED_IMAGE} ghcr.io/${TRAVIS_REPO_SLUG}:${tag}
    docker push ghcr.io/${TRAVIS_REPO_SLUG}:${tag}
}

if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
  echo ${GITHUB_PACKAGE_TOKEN} | docker login ghcr.io --username "${GITHUB_PACKAGE_USER}" --password-stdin
  docker_tag=r-$TRAVIS_BRANCH-$TRAVIS_COMMIT

  if [ "$TRAVIS_BRANCH" == "master" ]; then
    echo "Pushing image to GitHub Packages ghcr.io/${TRAVIS_REPO_SLUG}:latest"
    docker tag ${GENERATED_IMAGE} ghcr.io/${TRAVIS_REPO_SLUG}:latest
    docker push "ghcr.io/${TRAVIS_REPO_SLUG}:latest"

    deploy ${docker_tag}

  elif [ ! -z "$TRAVIS_TAG" ]; then
    echo "Pushing image to GitHub Packages ghcr.io/${TRAVIS_REPO_SLUG}:${TRAVIS_TAG}"
    docker tag ${GENERATED_IMAGE} ghcr.io/${TRAVIS_REPO_SLUG}:${TRAVIS_TAG}
    docker push "ghcr.io/${TRAVIS_REPO_SLUG}:${TRAVIS_TAG}"

  elif [ ! -z "$TRAVIS_BRANCH" ]; then
    deploy ${docker_tag}

  else
    echo "Not deploying image"
  fi
fi
