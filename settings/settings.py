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

URL_APP = "http://" + IP_APP + ":" + str(PORT_APP)

# Page of login
# LOGIN_URL = "/auth/login/"
LOGIN_URL = "/"

# By default is False, so run the application normally
# True is just for Debug
DEBUG_MODE = False
# DEBUG_MODE = True

# A list of hosts that have permission to access the application
# HOSTS_ALLOWED = ["http://localhost:8888", "http://localhost:8080"]

# redirect uri google (production and debug)
__REDIRECT_URI_GOOGLE__ = "http://localhost:8888/api/auth/google"
__REDIRECT_URI_GOOGLE_DEBUG__ = "http://localhost:8888/api/auth/google"

# redirect uri facebook (production and debug)
__REDIRECT_URI_FACEBOOK__ = "http://localhost:8888/api/auth/facebook"
__REDIRECT_URI_FACEBOOK_DEBUG__ = "http://localhost:8888/api/auth/facebook"

# after login with social login, redirect to... (production and debug)
__AFTER_LOGIN_REDIRECT_TO__ = "http://localhost:8888"
__AFTER_LOGIN_REDIRECT_TO_DEBUG__ = "http://localhost:8888"
