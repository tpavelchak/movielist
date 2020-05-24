# Movie List application
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

Python application that provides a plain list of all movies of Studio Ghibli company using the Ghibli API.

## Getting started

### Development Environment Setup

* Install python 3.6 or newer.

* Clone the repo. `git clone git@github.com:tpavelchak/movielist.git`

* Go to the project's root directory. `cd movielist/`

#### Start Application Using Virtual Environment

* Install and activate a virtual environment using those instructions [virtualenv / virtualenvwrapper](https://alysivji.github.io/setting-up-pyenv-virtualenvwrapper.html)

* Install all needed dependencies using command `pip install -r requirements.txt`

* Run command `python manage.py migrate` to apply DB migrations.

* Run `python manage.py runserver` to start the project.

#### Start Application Using Docker

* Install [Docker for Mac](https://docs.docker.com/docker-for-mac/) or [Docker for Windows](https://docs.docker.com/docker-for-windows/).

* Run command `docker-compose up -d`

### Running Tests

Tests can be run by the command `python manage.py test` in case of using a virtual environment. Run the command `docker-compose run web python manage.py test` in case of using docker.

## Coding style

The codebase is [PEP8](https://www.python.org/dev/peps/pep-0008/) compliant.
We can use command `./scripts/style_guide_check.sh` to verify it.