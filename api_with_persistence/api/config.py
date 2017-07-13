"""
The following lines show the code that declares variables that determine the
configuration for Flask and SQLAlchemy.

We will specify this module created as an argument to a function that will
create a Flask app.
"""

import os

base_dir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
PORT = 5000
HOST = "127.0.0.1"
SQLALCHEMY_ECHO  = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "postgresql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER="user_name", DB_PASS="password", DB_ADDR="127.0.0.1", DB_NAME="messages")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
