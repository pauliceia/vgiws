#!/usr/bin/env python
# -*- coding: utf-8 -*-


####################################################################################################
# SOCIAL LOGIN
####################################################################################################

# A dictionary with the settings about Facebook App

# Login -  https://developers.facebook.com/docs/facebook-login/
# (1) Acessar Aplicativos: https://developers.facebook.com/apps/
# (2) Clicar no aplicativo ou acessar um
# (3) Ir em Settings > Basic
# (4) Vai aparecer o ID do Aplicativo (api_key) e Chave Secreta (secret)
__FACEBOOK_SETTINGS__ = {
    "facebook_api_key": "",
    "facebook_secret": "",
}

# (1) Acessar: https://console.developers.google.com/
# (2) Abrir o projeto pauliceia (ou criar um novo)
# (3) No menu lateral (API e serviços) clicar em credenciais
# (4) Para criar uma nova credencial clicar em "Criar credencial" e escolher as opções
# (5) Em produção precisa colocar uma URL com a Politica de Privacidade do site (Credenciais > Tela de consentimento OAuth > URL de privacidade)
__GOOGLE_SETTINGS__ = {
    "google_oauth": {
        "key": "",
        "secret": "",
    }
}

####################################################################################################
# JSON Web Token
####################################################################################################

# JSON Web Token. To generate a new secret code use:  https://gist.github.com/didip/823887
__JWT_SECRET__ = ""
__JWT_ALGORITHM__ = ''

####################################################################################################
# MAIL
####################################################################################################

# Inform an email to send notifications by email
# PS: It is needed to enable less secure apps. If you are using Gmail: https://myaccount.google.com/lesssecureapps
__TO_MAIL_ADDRESS__ = ""
__PASSWORD_MAIL_ADDRESS__ = ""

# Inform the SMTP server
__SMTP_ADDRESS__ = 'smtp.gmail.com'
__SMTP_PORT__ = 587

__EMAIL_SIGNATURE__ = """--

Best regards

Team
"""

####################################################################################################
# OTHERS
####################################################################################################

# Hint: How to generate a new cookie secret use: https://gist.github.com/didip/823887
__COOKIE_SECRET__ = ""
