#!/usr/bin/env sh

set -o errexit -o pipefail -x

mkdir -p results

tox | tee results/test.out
