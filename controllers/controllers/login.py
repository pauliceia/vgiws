#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create controllers.
"""

from base64 import b64decode

from ..base import BaseHandler, BaseHandlerSocialLogin

from tornado.auth import GoogleOAuth2Mixin, FacebookGraphMixin
from tornado.gen import coroutine

from settings.accounts import __GOOGLE_SETTINGS__, __FACEBOOK_SETTINGS__


# class AuthLogoutHandler(BaseHandler):
#
#     urls = [r"/auth/logout/", r"/auth/logout"]
#
#     def get(self):
#         self.logout()


# class FakeAuthLoginHandler(BaseHandler):
#     """
#     A fake login to tests
#     """
#
#     urls = [r"/api/auth/login/fake/", r"/api/auth/login/fake"]
#
#     @just_run_on_debug_mode
#     def get(self):
#         user_json = {
#             'type': 'User',
#             'properties': {'id': -1, 'email': 'test@fake.login', 'username': 'test', 'password': '', 'name': "Fake login",
#                            'terms_agreed': True, 'can_add_layer': True, 'receive_notification_by_email': True}
#         }
#
#         encoded_jwt_token = self.login(user_json)
#
#         self.set_header('Authorization', encoded_jwt_token)
#
#         # Default: self.set_header('Content-Type', 'application/json')
#         self.write(json_encode({}))


class AuthLoginHandler(BaseHandler):

    urls = [r"/api/auth/login/", r"/api/auth/login"]

    def get(self):

        auth_header = self.request.headers.get('Authorization')

        if auth_header is None or not auth_header.startswith('Basic '):
            self.set_status(401)
            self.set_header('WWW-Authenticate', 'Basic realm=Restricted')
            self._transforms = []
            self.finish()
            return False

        auth_decoded = (b64decode(auth_header[6:])).decode()
        email, password = auth_decoded.split(':', 2)

        encoded_jwt_token = self.auth_login(email, password)
        self.set_header('Authorization', encoded_jwt_token)

        self.write(json_encode({}))


class GoogleLoginHandler(BaseHandlerSocialLogin, GoogleOAuth2Mixin):
    """
        Tornado Auth:
        http://www.tornadoweb.org/en/stable/auth.html
    """

    urls = [r"/api/auth/google/", r"/api/auth/google"]

    @coroutine
    def get(self):
        redirect_uri = self.__REDIRECT_URI_GOOGLE__

        self.application.settings['google_oauth'] = __GOOGLE_SETTINGS__['google_oauth']

        if self.get_argument('code', False):
            access = yield self.get_authenticated_user(
                            redirect_uri=redirect_uri,
                            code=self.get_argument('code'))
            user = yield self.oauth2_request(
                            "https://www.googleapis.com/oauth2/v1/userinfo",
                            access_token=access["access_token"])

            # print("\nuser: ", user, "\n")
            # for key in user:
            #     print(key, ": ", user[key])

            self.social_login(user)

        else:
            yield self.authorize_redirect(
                redirect_uri=redirect_uri,
                client_id=self.settings['google_oauth']['key'],
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'}
            )


class FacebookLoginHandler(BaseHandlerSocialLogin, FacebookGraphMixin):
    """
        Tornado Auth:
        http://www.tornadoweb.org/en/stable/auth.html

        How to create a new Facebook App:
        https://developers.facebook.com/docs/apps/register
        https://developers.facebook.com/docs/apps/register#developer-account

        In the Facebook App page in App Domains, add the domain of the server,
        in this case "localhost" and in the web site "http://localhost:8888/".
        https://developers.facebook.com/apps/461266394258303/settings/

        Permissions:
        https://developers.facebook.com/docs/facebook-login/permission
    """

    urls = [r"/api/auth/facebook/", r"/api/auth/facebook"]

    @coroutine
    def get(self):
        redirect_uri = self.__REDIRECT_URI_FACEBOOK__

        self.application.settings['facebook_api_key'] = __FACEBOOK_SETTINGS__['facebook_api_key']
        self.application.settings['facebook_secret'] = __FACEBOOK_SETTINGS__['facebook_secret']

        if self.get_argument("code", False):
            user = yield self.get_authenticated_user(
                    redirect_uri=redirect_uri,
                    client_id=self.settings["facebook_api_key"],
                    client_secret=self.settings["facebook_secret"],
                    code=self.get_argument("code"),
                    extra_fields=['email']
            )

            # print("\nuser: ", user, "\n")
            # for key in user:
            #     print(key, ": ", user[key])

            self.social_login(user)

        else:
            yield self.authorize_redirect(
                    redirect_uri=redirect_uri,
                    client_id=self.settings["facebook_api_key"],
                    extra_params={"scope": "email"}
            )
