#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to put the configurations of the system.
"""


import os
from datetime import datetime


# Put the reference of the function called "get" (os.environ.get) in os_environ_get
os_environ_get = os.environ.get


CURRENT_YEAR = str(datetime.now().year)
AUTHOR = "Rodrigo M. Mariano"


VERSION = "0.0.0"
TITLE_APP = "Web Service for Pauliceia Project"


# All public IP
IP_APP = "0.0.0.0"
PORT_APP = int(os_environ_get("PORT", 8888))


URL_APP = "https://" + IP_APP + ":" + str(PORT_APP)


# Page of login
# LOGIN_URL = "/auth/login/"
LOGIN_URL = "/"


# By default is False, so run the application normally
# True is just for Debug
# DEBUG_MODE = False
DEBUG_MODE = True


# LIST_HOSTS_ALLOW = [
#     "http://localhost:8888"
# ]
