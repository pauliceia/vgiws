#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Responsible module to create controllers.
"""

from base64 import b64decode
from os import path as os_path

from tornado.auth import GoogleOAuth2Mixin, FacebookGraphMixin
from tornado.gen import coroutine
from tornado.escape import json_encode
from tornado.web import HTTPError

from ..base import BaseHandler, BaseHandlerSocialLogin
from settings.accounts import __GOOGLE_SETTINGS__, __FACEBOOK_SETTINGS__
from modules.common import auth_non_browser_based


# Get the main folder (vgiws)
PROJECT_PATH = os_path.sep.join(os_path.abspath(__file__).split(os_path.sep)[:-3])


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


class AuthChangePasswordHandler(BaseHandler):

    urls = [r"/api/auth/change_password/", r"/api/auth/change_password"]

    @auth_non_browser_based
    def put(self):
        # get the body of the request
        resource_json = self.get_the_json_validated()

        p = resource_json["properties"]

        # check is exist the parameters inside the body
        if "current_password" not in p or "new_password" not in p:
            raise HTTPError(400, "It is needed to pass the encrypted current_password and new_password.")

        # get the email of the current user
        current_user = self.get_current_user_()
        email = current_user["properties"]["email"]

        # try to change the password
        self.change_password(email, p["current_password"], p["new_password"])


# class GoogleLoginHandler(BaseHandlerSocialLogin):
#     """
#     https://developers.google.com/identity/sign-in/web/server-side-flow
#     """
#
#     urls = [r"/api/auth/google/(.*)"]
#
#     # Set path to the Web application client_secret_*.json file you downloaded from the
#     # Google API Console: https://console.developers.google.com/apis/credentials
#     CLIENT_SECRET_FILE = PROJECT_PATH + "/settings/client_secret_542969957780-f97gr8l92maeoq7vmapb2auufsp4phaq.apps.googleusercontent.com.json"
#
#     def get(self, auth_code):
#
#         if auth_code == "":
#             raise HTTPError(409, "It is necessary to pass a 'token' in front of URL.")  # 400 - Conflict
#
#         # print("\n\nself.request.headers: ", self.request.headers, "\n\n")
#         # If this request does not have `X-Requested-With` header, this could be a CSRF
#         if "X-Requested-With" not in self.request.headers:
#             raise HTTPError(403, "Forbidden request.")  # 403 - Forbidden
#         # if not request.headers.get('X-Requested-With'):
#         #     abort(403)
#
#         try:
#             # Exchange auth code for access token, refresh token, and ID token
#             credentials = client.credentials_from_clientsecrets_and_code(
#                 self.CLIENT_SECRET_FILE,
#                 ['https://www.googleapis.com/auth/userinfo.profile', 'profile', 'email'],
#                 auth_code)
#         except FlowExchangeError as error:
#             raise HTTPError(400, "Invalid token.")  # 400 - Bad Request
#
#         # Call Google API
#         http_auth = credentials.authorize(Http())
#         drive_service = discovery.build('oauth2', 'v2', http=http_auth, cache_discovery=False)
#
#         # Get profile info from ID token
#         # user_id = credentials.id_token['sub']
#         # email = credentials.id_token['email']
#
#         # Get user information
#         user = drive_service.userinfo().get().execute()
#
#         # print("\n\n")
#         # print("id: ", user["id"])
#         # print("name: ", user["name"])
#         # print("email: ", user["email"])
#         # print("user_info: ", user)
#
#         self.social_login(user)


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

            self.social_login(user, "facebook")

        else:
            yield self.authorize_redirect(
                    redirect_uri=redirect_uri,
                    client_id=self.settings["facebook_api_key"],
                    extra_params={"scope": "email"}
            )


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

            self.social_login(user, "google")

        else:
            yield self.authorize_redirect(
                redirect_uri=redirect_uri,
                client_id=self.settings['google_oauth']['key'],
                scope=['profile', 'email'],
                response_type='code',
                extra_params={'approval_prompt': 'auto'}
            )
