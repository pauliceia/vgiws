#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to put the configurations of the system.
"""


# import os
from os import environ
from datetime import datetime


CURRENT_YEAR = str(datetime.now().year)

AUTHOR = "Rodrigo M. Mariano"

VERSION = "0.0.4"

TITLE_APP = "VGI Web Service for Historical Data"

# All public IP
IP_APP = "0.0.0.0"
PORT_APP = int(environ.get("PORT", 8888))

URL_APP = "https://" + IP_APP + ":" + str(PORT_APP)

# Page of login
# LOGIN_URL = "/auth/login/"
LOGIN_URL = "/"

# By default is False, so run the application normally
# True is just for Debug
DEBUG_MODE = False
# DEBUG_MODE = True

# A list of hosts that have permission to access the application
# HOSTS_ALLOWED = ["http://localhost:8888", "http://localhost:8080"]
