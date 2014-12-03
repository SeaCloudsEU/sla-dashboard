# SeaClouds SLA Dashboard #

## Description ##

Simple SLA dashboard.

Shows agreements, status and violations.

## Technical description ##

sla-dashboard application is composed by the following directories:

* sladashboard: the app related to the application itself. The settings
    file maybe need to be modified: read below.
* slagui: the sla dashboard GUI project.
* slaclient: this project contains all the code needed to connect to
    SLA Manager REST interface, and the conversion from xml/json to python
    objects.
* bin: some useful scripts


## Software requirements ##

Python version: 2.7.x

The required python packages are listed in requirements.txt

Installing the requirements inside a virtualenv is recommended.

SLA Manager (java backend) needs to be running in order to use the dashboard.

## Installing ##
----------

    #
    # Install virtualenv
    #
    $ pip install virtualenv


    #
    # Create virtualenv.
    # E.g.: VIRTUALENVS_DIR=~/virtualenvs
    #
    $ virtualenv $VIRTUALENVS_DIR/sla-dashboard

    #
    # Activate virtualenv
    #
    $ . $VIRTUALENVS_DIR/sla-dashboard/bin/activate

    #
    # Change to application dir and install requirements
    #
    $ cd $SLA_DASHBOARD
    $ pip install -r requirements.txt

    #
    # Create needed tables for sessions, admin, etc
    #
    $ ./manage.py syncdb

## Settings ##

* sladashboard/settings.py:
    - SLA_MANAGER_URL : The URL of the SLA Manager REST interface.
    - DEBUG: Please, set this to FALSE in production

* sladashboard/urls.py:
    - dashboard root url: the slagui project is accessed by default
        in $server:$port/slagui. Change "slagui" with the desired path.


## Running ##

NOTE: this steps are not suitable in production mode.

    #
    # Activate virtualenv
    #
    $ . $VIRTUALENVS_DIR/sla-dashboard/bin/activate

    #
    # Cd to application dir
    #
    $ cd $SLA_DASHBOARD

    #
    # Start server listing in port 8000 (change listening address and port as desired)
    #
    $ ./manage.py runserver 0.0.0.0:8000

    #
    # Test
    #
    curl http://localhost:8000/slagui/agreements/

## REST Facade Example ##

Initial conditions:

* Brooklyn is running and nuro application is deployed.
* Sla-core is running and loaded with `nuro-template` template:


    cd $SLA_CORE && bin/restoreDatabase.sh && bin/load-nuro-samples.sh

To create an agreement from that template and start the enforcement:

    cd $SLA_DASHBOARD
    SLA_DASHBOARD_URL=http://localhost:8000 bin/load-nuro-samples.sh \
        nuro-template random-client $appid $moduleid

, where $appid and $moduleid are the ids of the brooklyn application and
brooklyn php module, respectively.

Check agreement creation in $SLA_DASHBOARD_URL/slagui/agreements

##License##

Licensed under the [Apache License, Version 2.0][1]

[1]: http://www.apache.org/licenses/LICENSE-2.0
