Harvard China Forum
=========

Created with guide from Miguel Grinberg's tutorial on Flask here: http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world.

Installation
------------

The `setup.py` script will create this virtual environment (installing all the packages needed).

The sqlite database must also be created before the application can run --- just run the `db_create.py` script.

Running
-------

To run the application in the development web server just execute `run.py` with the Python interpreter from the flask virtual environment (remember to chmod).

Using
-------

Users are able to login via authorized Google Accounts

There is a pass phrase required to publish; this pass phrase is hard coded inside the python code.

currently, the pass phrase is hc4Z0IE (will look into more secure methods going into the future).