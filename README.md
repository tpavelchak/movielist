Movie List application
=====================
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)

## Getting started

### Development Environment Setup

1. Install python 3.6 or newer.

2. Clone the repo.
   1. `git clone git@github.com:tpavelchak/movielist.git`

3. Install and activate virtual environment using those instructions [virtualenv / virtualenvwrapper](https://alysivji.github.io/setting-up-pyenv-virtualenvwrapper.html)

4. Install all needed dependencies using command `pip install -r requirements.txt`

5. Run command `python manage.py migrate` to apply DB migrations.

6. Run `python manage.py runserver` to start project.

### Running Tests
Tests can be run using `python manage.py test`.

## Coding style

THe codebase is [PEP8](https://www.python.org/dev/peps/pep-0008/) compliant.
We can use command `./scripts/style_guide_check.sh` to verify it.