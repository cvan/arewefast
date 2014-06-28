# arewefast

Are we fast?


# Prerequisites

Install PostgreSQL via [homebrew](http://brew.sh/):

    brew install postgresql
    ln -sfv /usr/local/opt/postgresql/*.plist ~/Library/LaunchAgents
    launchctl load ~/Library/LaunchAgents/homebrew.mxcl.postgresql.plist
    initdb /usr/local/var/postgres

If you run into problems initalising the database, you may need to do this:

    rm -rf /usr/local/var/postgres


# Installation

## Virtual environment

### virtualenv

If you don't already have [`virtualenv`](https://pypi.python.org/pypi/virtualenv) installed, do that now:

    curl -s https://raw.github.com/brainsik/virtualenv-burrito/master/virtualenv-burrito.sh | $SHELL

Open a new shell to test it out. You should have the `workon` and `mkvirtualenv` commands.

Create a new virtual environment for this project:

    mkvirtualenv arewefast --distribute --python=python2.7

This just created a clean environment named "arewefast" using Python 2.7. You can get out of the environment by restarting your shell or calling `deactivate`.

    workon arewefast

### virtualenvwrapper

[`virtualenvwrapper`](http://virtualenvwrapper.readthedocs.org/) lets you run hooks when creating, activating, and deleting virtual environments. These hooks can change settings, the shell environment, or anything else you want to do from a shell script.

Install:

    pip install virtualenvwrapper

# Packages

If you don't already have `pip` installed, do that now:

    sudo easy_install pip

If you do have `pip` installed, make sure you have an up-to-date version installed:

    pip install --upgrade pip

First change to the `arewefast` directory in the project root:

    cd arewefast

From inside your activated virtual environment, install the required Python packages:

    pip install -r requirements.txt

Set up PostgreSQL database:

    createdb arewfast
    python manage.py db init
    python manage.py db migrate

If you use [autoenv](https://github.com/kennethreitz/autoenv), this is a good start for your .env:

    workon arewefast
    export APP_SETTINGS='config.DevelopmentConfig'
    export DATABASE_URI='postgresql://localhost/arewefast'

Otherwise, you'll want to set the aforementioned environment variables when you run `python manage.py` and `python app.py`.

# Development

Run the development server:

    python app.py

When you have made changes to the models, create a migration to update the database schema:

    python manage.py db migrate

Then run the migration:

    python manage.py db upgrade

Poke around the database:

    psql arewefast

View the database tables:

    \dt

Run tests:

    make test
