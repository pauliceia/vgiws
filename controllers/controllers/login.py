#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create controllers.
"""

from base64 import b64decode

from ..base import *

from tornado.auth import GoogleOAuth2Mixin, FacebookGraphMixin
from tornado.gen import coroutine

from settings.accounts import __FACEBOOK_SETTINGS__, __GOOGLE_SETTINGS__


# authentication

# class AuthLogoutHandler(BaseHandler):
#
#     urls = [r"/auth/logout/", r"/auth/logout"]
#
#     def get(self):
#         self.logout()


# TODO: CREATE A OAUTH2

# class AuthLoginHandler(BaseHandler):
#     # Login
#     # http://www.tornadoweb.org/en/stable/guide/security.html
#     # http://guillaumevincent.com/2013/02/12/Basic-authentication-on-Tornado-with-a-decorator.html
#     # https://github.com/tornadoweb/tornado/tree/stable/demos/blog
#
#     urls = [r"/auth/login/", r"/auth/login"]
#
#     def get(self):
#         errormessage = self.get_argument("error", "")
#
#         self.render("example/auth/login.html", errormessage=errormessage)
#
#     def post(self):
#         email = self.get_argument("email", "")
#         password = self.get_argument("password", "")
#
#         result = self.do_login(email, password)
#
#         if result:
#             self.set_current_user(email=email, type_login="normal", new_user=True)
#             # user_cookie = self.get_current_user()
#
#             self.set_and_send_status(status=200, reason="Logged in system")
#             return
#             # super(BaseHandler, self).redirect(self.__AFTER_LOGGED_REDIRECT_TO__)
#         else:
#             self.set_and_send_status(status=404, reason="Login is invalid. Correct them and try again.")
#             return


class FakeAuthLoginHandler(BaseHandler):
    """
    A fake login to tests
    """

    urls = [r"/auth/login/fake/", r"/auth/login/fake"]

    @just_run_on_debug_mode
    def get(self):
        user_json = {
            'type': 'User',
            'properties': {'id': -1, 'email': 'test@fake.login', 'username': 'test', 'password': '', 'name': "Fake login",
                           'terms_agreed': True, 'can_add_layer': True, 'receive_notification_by_email': True}
        }

        encoded_jwt_token = self.login(user_json)

        self.set_header('Authorization', encoded_jwt_token)

        # Default: self.set_header('Content-Type', 'application/json')
        self.write(json_encode({}))

"""
JWT
https://tableless.com.br/entendendo-tokens-jwt/
https://github.com/jpadilla/pyjwt
http://blog.apcelent.com/json-web-token-tutorial-with-example-in-python.html
https://steelkiwi.com/blog/jwt-authorization-python-part-1-practise/
"""

class AuthLoginHandler(BaseHandler):

    urls = [r"/auth/login/", r"/auth/login"]

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

        # Default: self.set_header('Content-Type', 'application/json')

        self.set_header('Authorization', encoded_jwt_token)

        self.write(json_encode({}))


class GoogleLoginHandler(BaseHandler, GoogleOAuth2Mixin):
    """
        Tornado Auth:
        http://www.tornadoweb.org/en/stable/auth.html
    """

    urls = [r"/auth/google/", r"/auth/google"]

    redirect_uri = "http://localhost:8888/auth/google/"

    @coroutine
    def get(self):

        self.application.settings['google_oauth'] = __GOOGLE_SETTINGS__['google_oauth']

        if self.get_argument('code', False):
            access = yield self.get_authenticated_user(
                            redirect_uri=self.redirect_uri,
                            code=self.get_argument('code'))
            user = yield self.oauth2_request(
                            "https://www.googleapis.com/oauth2/v1/userinfo",
                            access_token=access["access_token"])

            # for key in user:
            #     print(key, ": ", user[key])
            # print(user)

            # self.set_current_user(email=user["email"], type_login="google", new_user=True)

            # to social login, create a blank password
            user_json = {
                'type': 'User',
                'tags': [{'k': 'type_login', 'v': 'google'}],
                'properties': {'id': -1, 'email': user["email"], 'username': '', 'password': ''}
            }

            self.login(user_json)

            # user_cookie = self.get_current_user()
            #
            # self.set_and_send_status(status=200, reason="Logged in system")
            super(BaseHandler, self).redirect(self.__AFTER_LOGGED_IN_REDIRECT_TO__)
        else:
            yield self.authorize_redirect(
                redirect_uri=self.redirect_uri,
                client_id=self.settings['google_oauth']['key'],
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'}
            )


class FacebookLoginHandler(BaseHandler, FacebookGraphMixin):
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

    urls = [r"/auth/facebook/", r"/auth/facebook"]

    redirect_uri = "http://localhost:8888/auth/facebook/"

    @coroutine
    def get(self):

        self.application.settings['facebook_api_key'] = __FACEBOOK_SETTINGS__['facebook_api_key']
        self.application.settings['facebook_secret'] = __FACEBOOK_SETTINGS__['facebook_secret']

        if self.get_argument("code", False):
            user = yield self.get_authenticated_user(
                    redirect_uri=self.redirect_uri,
                    client_id=self.settings["facebook_api_key"],
                    client_secret=self.settings["facebook_secret"],
                    code=self.get_argument("code"),
                    extra_fields=['email']
            )

            # for key in user:
            #     print(key, ": ", user[key])
            # print(user)

            # self.set_current_user(email=user["email"], type_login="facebook", new_user=True)

            # to social login, create a blank password
            user_json = {
                'type': 'User',
                'tags': [{'k': 'type_login', 'v': 'facebook'}],
                'properties': {'id': -1, 'email': user["email"], 'username': '', 'password': ''}
            }

            self.login(user_json)

            # user_cookie = self.get_current_user()
            #
            # self.set_and_send_status(status=200, reason="Logged in system")
            super(BaseHandler, self).redirect(self.__AFTER_LOGGED_IN_REDIRECT_TO__)
        else:
            yield self.authorize_redirect(
                    redirect_uri=self.redirect_uri,
                    client_id=self.settings["facebook_api_key"],
                    extra_params={"scope": "user_posts,email"}
            )


# login and logout with success

# class AuthLoginSuccessHandler(BaseHandler):
#
#     # nl = need login
#     urls = [r"/auth/login/success/", r"/auth/login/success"]
#
#     def get(self):
#         self.render("example/auth/login_success.html")


# class AuthLogoutSuccessHandler(BaseHandler):
#
#     # nl = need login
#     urls = [r"/auth/logout/success/", r"/auth/logout/success"]
#
#     def get(self):
#         self.render("example/auth/logout.html")


# other handlers

# class MainHandlerNeedLogin(BaseHandler):
#
#     # nl = need login
#     urls = [r"/main/nl/", r"/main/nl"]
#
#     @authenticated
#     def get(self):
#         username = xhtml_escape(self.current_user)
#         self.render("example/main/mainneedlogin.html", username=username)


# class MainHandlerDontNeedLogin(BaseHandler):
#
#     # dnl = don't need login
#     urls = [r"/main/dnl/", r"/main/dnl"]
#
#     def get(self):
#         username = xhtml_escape(self.current_user)
#         self.render("example/main/maindontneedlogin.html", username=username)


