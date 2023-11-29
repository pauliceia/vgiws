#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to put the configurations of the system.
"""

from os import getenv
from datetime import datetime


CURRENT_YEAR = str(datetime.now().year)

AUTHOR = "Rodrigo M. Mariano"

VERSION = "0.0.5"

TITLE_APP = "VGI Web Service for Historical Data"

# All public IP
IP_APP = "0.0.0.0"
PORT_APP = int(getenv("PORT", 8888))

URL_APP = "http://" + IP_APP + ":" + str(PORT_APP)

# Page of login
# LOGIN_URL = "/auth/login/"
LOGIN_URL = "/"

# By default is False, so run the application normally
# True is just for Debug
DEBUG_MODE = False

# By default is True, so publish the layers in geoserver
# False is just for Debug
PUBLISH_LAYERS_IN_GEOSERVER = True

# A list of hosts that have permission to access the application
# HOSTS_ALLOWED = ["http://localhost:8888", "http://localhost:8080"]

# temporary folder where will be save the import files temporarily
__TEMP_FOLDER__ = "/tmp/vgiws"


####################################################################################################
# SOCIAL LOGIN
####################################################################################################

# redirect uri google (production and debug)
__REDIRECT_URI_GOOGLE__ = "https://pauliceia.unifesp.br/api/vgi/api/auth/google"  # production
# __REDIRECT_URI_GOOGLE__ = "http://localhost/api/vgi/api/auth/google"  # test the platform offline
__REDIRECT_URI_GOOGLE_DEBUG__ = "http://localhost:8888/api/auth/google"  # debug VGIMWS

# redirect uri facebook (production and debug)
__REDIRECT_URI_FACEBOOK__ = "https://pauliceia.unifesp.br/api/vgi/api/auth/facebook"  # production
# __REDIRECT_URI_FACEBOOK__ = "http://localhost/api/vgi/api/auth/facebook"  # test the platform offline
__REDIRECT_URI_FACEBOOK_DEBUG__ = "http://localhost:8888/api/auth/facebook"  # debug VGIMWS

# after login with social login, redirect to... (production and debug)
__AFTER_LOGIN_REDIRECT_TO__ = "https://pauliceia.unifesp.br/portal/valid/social"  # production
# __AFTER_LOGIN_REDIRECT_TO__ = "http://localhost/portal/valid/social"  # test the platform offline
__AFTER_LOGIN_REDIRECT_TO_DEBUG__ = "http://localhost:8081/portal/valid/social"  # debug VGIMWS


####################################################################################################
# EMAIL
####################################################################################################

# URL to validate the email (production and debug)
__VALIDATE_EMAIL__ = "https://pauliceia.unifesp.br/portal/valid/email"  # production
# __VALIDATE_EMAIL__ = "http://localhost/portal/valid/email"  # test the platform offline
__VALIDATE_EMAIL_DEBUG__ = "http://localhost:8081/portal/valid/email"  # debug VGIMWS

# wait X second(s) after sending an e-mail in order to avoid blocking the SMTP server
__TIME_TO_WAIT_AFTER_SENDING_AN_EMAIL_IN_SECONDS__ = 1


####################################################################################################
# SPATIAL BOUNDING BOX
####################################################################################################
# by default, the spatial bounding box is the São Paulo city
# hint: it can be discovered by QGIS
__SPATIAL_BB__ = {
    "xmin": 313389.67,
    "ymin": 7343788.61,
    "xmax": 360663.23,
    "ymax": 7416202.05,
    "EPSG": 29193,
}
