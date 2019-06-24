#!/bin/bash -e
# This file has been generated with 'invoke project.sync'.
# Do not modify. Any manual change will be lost.
# Please propose your modification on
# https://github.com/camptocamp/odoo-template instead.

local_dir="$(dirname "$0")"

function deploy {
    local tag=$1

    echo "Pushing image to docker hub ${DOCKER_HUB_REPO}:${tag}"
    docker tag ${GENERATED_IMAGE} ${DOCKER_HUB_REPO}:${tag}
    docker push ${DOCKER_HUB_REPO}:${tag}

    echo "Creating a minion for ${tag} on ${TRAVIS_BRANCH}"
    $local_dir/minion-client.py \
      ${tag} \
      ${RANCHER_MINION_SERVER} \
      ${minion_server_token} \
      $local_dir/minion-files/docker-compose.yml \
      $local_dir/minion-files/rancher-compose.yml \
      $local_dir/minion-files/rancher.list

}

if [ "$TRAVIS_PULL_REQUEST" == "false" ]; then
  docker login --username="$DOCKER_USERNAME" --password="$DOCKER_PASSWORD"
  docker_tag=r-$TRAVIS_BRANCH-$TRAVIS_COMMIT

  if [ "$TRAVIS_BRANCH" == "master" ]; then
    echo "Pushing image to docker hub ${DOCKER_HUB_REPO}:latest"
    docker tag ${GENERATED_IMAGE} ${DOCKER_HUB_REPO}:latest
    docker push "${DOCKER_HUB_REPO}:latest"

    deploy ${docker_tag}

  elif [ ! -z "$TRAVIS_TAG" ]; then
    echo "Pushing image to docker hub ${DOCKER_HUB_REPO}:${TRAVIS_TAG}"
    docker tag ${GENERATED_IMAGE} ${DOCKER_HUB_REPO}:${TRAVIS_TAG}
    docker push "${DOCKER_HUB_REPO}:${TRAVIS_TAG}"

  elif [ ! -z "$TRAVIS_BRANCH" ]; then
    deploy ${docker_tag}

  else
    echo "Not deploying image"
  fi
fi
