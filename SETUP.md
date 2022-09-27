# Setup Guide

This document describes how to setup OSS PackRat for two different kinds of users: researchers and contributors!

# Researcher Setup
TODO

# Developer Setup
If you want to contribute to OSS PackRat, you'll first want to set the system up locally. This document will describe how to get yourself setup for local and Docker development.

## Dependencies
To get setup locally, you'll first want to make sure you have the right things installed. You'll need Python and Postgres. At the time of writing this, here are the versions we are using:
* Python 3.9.4
* Postgres 10.3
If you're using later versions than those, you're probably fine. Earlier versions of the above listed software may cause problems though.

## Clone the repo
Navigate to a folder/directory where you'd like to install the project and run

```
git clone git@github.com:erik-whiting/OSS-PackRat.git
```

Now the code should be on your local computer. All the instructions from here on will assume that your terminal is inside the project root. To do this, make sure to run `cd OSS-PackRat` after cloning the repository.

## Database Setup
The next thing you'll want to do is setup the database. There are a few convenient scripts in the `db` directory to help you get started. `create_database` creates a database named `OSSPackRat` (although, I believe Postgres is case insensitive by default). Additionally, there is also `create_database.ps1` script for Windows users.

There is also a script called `create_test_database`. This creates a database named `osspackrat_test` and is used by the test suite. You must build this database in order to run the database-specific tests in the test suite. There is also a `create_test_database.ps1` script for Windows users. Note that these scripts seed the test database with some dummy data.

Decide which scrript you want to use and run it from your command line of choice!

## Code Setup
This project uses Python virtual environments. This means that in order to be on the exact same page as other developers, you will need to build and activate your virtual environment when doing any dev work. It also means that you need to add the names of any 3rd party packages you add to the project in the `requirements.txt` file.

To initiate and activate your virtual environment, run:

```
$> python -m venv .env
$> .env/Scripts/activate
```
This will initiate and activate you virtual environment and you should see `(.env)` somewhere in your terminal (to deactivate, simpply run `deactivate` from the command line).

With your virtual environment now activated, the last thing you have to do is install the requirements. You can do this by running

```
pip install -r requirements.txt
```

# Docker Setup
TODO

