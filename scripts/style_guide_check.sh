#!/bin/sh
#
# Ensure the codebase is pep8 compliant

flake8 --exclude 'migrations' movies
