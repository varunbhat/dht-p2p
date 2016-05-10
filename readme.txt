=================================
Installation procedure
=================================

Requirements
=============
* Python 3.4 installation - Installation Link: https://www.python.org/downloads/
* virtualenv


Preparations
============

Preapre the virtualenv using

> virtualenv -v /usr/bin/python3 env
> . env/bin/activate
> pip install -r requirements.txt


Run the sourcecode
===================

Run the source code:

Bootstrap Server
----------------
Start the bootstrap server using the following command

> ./Bootstrap.py

Run the Main file using

> ./iot -p <PORT>

Run the client to send the requests

> python clients.py [sensors] [location]




