
from modules import generate_random_string
from modules.common import generate_encoded_jwt_token

from util.tester import RequestTester, get_string_in_hash_sha512


class TestAPIUser(RequestTester):

    def setUp(self):
        self.set_urn('/api/user')

    # user - get

    def test__get_api_user__return_all_users(self):
        expected_at_least = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': True,
                                   'username': 'admin', 'id': 1001, 'email': 'admin@admin.com',
                                   'name': 'Administrator', 'is_the_admin': True,
                                   'created_at': '2017-01-01 00:00:00', 'login_date': '2017-01-01T00:00:00',
                                   'is_email_valid': True, 'picture': '', 'social_id': '', 'social_account': ''}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': True,
                                   'username': 'rodrigo', 'id': 1002, 'email': 'rodrigo@admin.com',
                                   'name': 'Rodrigo', 'is_the_admin': True,
                                   'created_at': '2017-03-03 00:00:00', 'login_date': '2017-03-03T00:00:00',
                                   'is_email_valid': True, 'picture': '', 'social_id': '', 'social_account': ''}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': True,
                                   'username': 'miguel', 'id': 1003, 'email': 'miguel@admin.com',
                                   'name': 'Miguel', 'is_the_admin': False,
                                   'created_at': '2017-05-08 00:00:00', 'login_date': '2017-05-08T00:00:00',
                                   'is_email_valid': True, 'picture': '', 'social_id': '', 'social_account': ''}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': False,
                                   'username': 'rafael', 'id': 1004, 'email': 'rafael@admin.com',
                                   'name': 'Rafael', 'is_the_admin': False,
                                   'created_at': '2017-06-09 00:00:00', 'login_date': '2017-06-09T00:00:00',
                                   'is_email_valid': True, 'picture': '', 'social_id': '', 'social_account': ''}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': False,
                                   'username': 'gabriel', 'id': 1005, 'email': 'gabriel@admin.com',
                                   'name': 'Gabriel', 'is_the_admin': False,
                                   'created_at': '2017-09-20 00:00:00', 'login_date': '2017-09-20T00:00:00',
                                   'is_email_valid': False, 'picture': '', 'social_id': '', 'social_account': ''}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': False,
                                   'username': 'fernanda', 'id': 1006, 'email': 'fernanda@admin.com',
                                   'name': None, 'is_the_admin': False,
                                   'created_at': '2017-01-19 00:00:00', 'login_date': '2017-01-19T00:00:00',
                                   'is_email_valid': True, 'picture': '', 'social_id': '', 'social_account': ''}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': False, 'terms_agreed': True,
                                   'username': 'ana', 'id': 1007, 'email': 'ana@admin.com',
                                   'name': None, 'is_the_admin': False,
                                   'created_at': '2017-01-18 00:00:00', 'login_date': '2017-01-18T00:00:00',
                                   'is_email_valid': True, 'picture': '', 'social_id': '', 'social_account': ''}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': False, 'terms_agreed': False,
                                   'username': 'bea', 'id': 1008, 'email': 'bea@admin.com',
                                   'name': None, 'is_the_admin': False,
                                   'created_at': '2017-01-30 00:00:00', 'login_date': '2017-01-30T00:00:00',
                                   'is_email_valid': False, 'picture': '', 'social_id': '', 'social_account': ''}
                }
            ]
        }

        self.get(expected_at_least=expected_at_least)

    def test__get_api_user__return_user_by_user_id(self):
        expected = {
            'features': [
                {'properties': {'name': 'Rodrigo', 'login_date': '2017-03-03T00:00:00', 'terms_agreed': True,
                                'receive_notification_by_email': True, 'id': 1002, 'username': 'rodrigo',
                                'is_email_valid': True, 'is_the_admin': True, 'email': 'rodrigo@admin.com',
                                'created_at': '2017-03-03 00:00:00', 'picture': '', 'social_id': '', 'social_account': ''},
                 'type': 'User'}
            ],
            'type': 'FeatureCollection'
        }

        self.get(expected, id="1002")

    def test__get_api_user__return_users_by_name(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': True,
                                   'username': 'miguel', 'id': 1003, 'email': 'miguel@admin.com',
                                   'name': 'Miguel', 'is_the_admin': False,
                                   'created_at': '2017-05-08 00:00:00', 'login_date': '2017-05-08T00:00:00',
                                   'is_email_valid': True, 'picture': '', 'social_id': '', 'social_account': ''}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': False,
                                   'username': 'rafael', 'id': 1004, 'email': 'rafael@admin.com',
                                   'name': 'Rafael', 'is_the_admin': False,
                                   'created_at': '2017-06-09 00:00:00', 'login_date': '2017-06-09T00:00:00',
                                   'is_email_valid': True, 'picture': '', 'social_id': '', 'social_account': ''}
                },
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': False,
                                   'username': 'gabriel', 'id': 1005, 'email': 'gabriel@admin.com',
                                   'name': 'Gabriel', 'is_the_admin': False,
                                   'created_at': '2017-09-20 00:00:00', 'login_date': '2017-09-20T00:00:00',
                                   'is_email_valid': False, 'picture': '', 'social_id': '', 'social_account': ''}
                },
            ]
        }

        self.get(expected, name="êL")

    def test__get_api_user__return_users_by_email(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': False,
                                   'username': 'rafael', 'id': 1004, 'email': 'rafael@admin.com',
                                   'name': 'Rafael', 'is_the_admin': False,
                                   'created_at': '2017-06-09 00:00:00', 'login_date': '2017-06-09T00:00:00',
                                   'is_email_valid': True, 'picture': '', 'social_id': '', 'social_account': ''}
                }
            ]
        }

        self.get(expected, email="rafael@admin.com")

    def test__get_api_user__return_users_by_username(self):
        expected = {
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'User',
                    'properties': {'receive_notification_by_email': True, 'terms_agreed': True,
                                   'username': 'miguel', 'id': 1003, 'email': 'miguel@admin.com',
                                   'name': 'Miguel', 'is_the_admin': False,
                                   'created_at': '2017-05-08 00:00:00', 'login_date': '2017-05-08T00:00:00',
                                   'is_email_valid': True, 'picture': '', 'social_id': '', 'social_account': ''}
                }
            ]
        }

        self.get(expected, username="miguel")

    def test__get_api_user__return_zero_resources(self):
        expected = {'type': 'FeatureCollection', 'features': []}

        self.get(expected, id="999")
        self.get(expected, id="998")

    # user - create, update and delete

    def test__post_put_delete_api_user(self):
        # create a fake email to avoid the error when exist the same email in DB
        username = generate_random_string()
        email = username + "@roger.com"
        password = 'roger'

        ##################################################
        # create a user
        ##################################################
        resource = {
            'type': 'User',
            'properties': {
                'id': None, 'email': email, 'password': get_string_in_hash_sha512(password),
                'username': username, 'name': 'Roger',
                'terms_agreed': True, 'receive_notification_by_email': False
            }
        }
        resource_id = self.post(resource, add_suffix_to_uri="/create")
        resource["properties"]["id"] = resource_id

        ##################################################
        # validate the email
        ##################################################
        token = generate_encoded_jwt_token({'user_id': resource_id})

        # check if the user is with an invalidated email
        user = self.get(id=resource_id)
        self.assertEqual(user["features"][0]["properties"]["is_email_valid"], False)

        # then, the user validate his email
        self._get(URI=f'/api/validate_email/{token}')

        # check if the user is with an validated email
        user = self.get(id=resource_id)
        self.assertEqual(user["features"][0]["properties"]["is_email_valid"], True)

        ##################################################
        # login with the created user
        ##################################################
        self.auth_login(email, password)

        ##################################################
        # update the user with himself/herself
        ##################################################
        resource["properties"]["name"] = "Roger Jose"
        resource["properties"]["receive_notification_by_email"] = True
        self.put(resource)

        ##################################################
        # check if the resource was modified
        ##################################################
        del resource["properties"]["password"]  # remove the password, because it is not needed to compare

        expected = {'type': 'FeatureCollection', 'features': [resource]}
        self.get(expected_at_least=expected, id=resource_id)

        ##################################################
        # logout with the created user and log in with a admin user (who can update/delete a user)
        ##################################################
        self.auth_logout()
        self.auth_login("admin@admin.com", "admin")

        ##################################################
        # update the user with a admin
        ##################################################
        resource["properties"]["name"] = "Roger"
        resource["properties"]["receive_notification_by_email"] = False
        self.put(resource)

        ##################################################
        # check if the resource was modified
        ##################################################
        expected = {'type': 'FeatureCollection', 'features': [resource]}
        self.get(expected_at_least=expected, id=resource_id)

        ##################################################
        # delete the user with an administrator
        ##################################################
        # remove the resource
        self.delete(argument=resource_id)

        # check if the user was deleted
        expected = {'type': 'FeatureCollection', 'features': []}
        self.get(expected, id=resource_id)

        self.auth_logout()


class TestAPIUserErrors(RequestTester):

    def setUp(self):
        self.set_urn('/api/user')

    # user errors - get

    def test__get_api_user__400_bad_request(self):
        for item in ["abc", 0, -1, "-1", "0"]:
            self.get(id=item, status_code=400, expected_text="Invalid parameter.")

    # user errors - create

    def test__post_api_user___400_bad_request__attribute_already_exist(self):
        # try to create a resource with email that already exist
        resource = {
            'type': 'User',
            'properties': {'email': "rodrigo@admin.com", 'password': 'roger', 'username': 'roger', 'name': 'Roger',
                           'terms_agreed': True,  'receive_notification_by_email': False}
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=400,
            expected_text="Attribute already exists. (error: Key (email)=(rodrigo@admin.com) already exists.)"
        )

        # try to create a resource with username that already exist
        resource = {
            'type': 'User',
            'properties': {'username': 'rodrigo', 'email': "new@email.com", 'password': 'roger', 'name': 'Roger',
                           'terms_agreed': True,  'receive_notification_by_email': False}
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=400,
            expected_text="Attribute already exists. (error: Key (username)=(rodrigo) already exists.)"
        )

    def test__post_api_user___400_bad_request__attribute_in_JSON_is_missing(self):
        # try to create a user without username
        resource = {
            'type': 'User',
            'properties': {'email': "new@email.com", 'password': 'roger', 'name': 'Roger',
                           'receive_notification_by_email': False}
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=400,
            expected_text=("Some attribute in the JSON is missing. "
                           "Look at the documentation! (error: 'username' is missing)")
        )

        # try to create a user without email
        resource = {
            'type': 'User',
            'properties': {'username': 'new', 'password': 'roger', 'name': 'Roger',
                           'receive_notification_by_email': False}
        }
        self.post(
            resource, add_suffix_to_uri="/create", status_code=400,
            expected_text=("Some attribute in the JSON is missing. "
                           "Look at the documentation! (error: 'email' is missing)")
        )

    # user errors - update

    def test__put_api_user__400_bad_request__attribute_already_exist(self):
        self.auth_login("admin@admin.com", "admin")

        # try to create a resource with email that already exists
        resource = {
            'type': 'User',
            'properties': {'id': 1005, 'email': "admin@admin.com", 'username': 'gabriel', 'name': 'Gabriel',
                           'terms_agreed': True, 'receive_notification_by_email': False}
        }
        self.put(
            resource, status_code=400,
            expected_text="Attribute already exists. (error: Key (email)=(admin@admin.com) already exists.)"
        )

        # try to create a resource with username that already exists
        resource = {
            'type': 'User',
            'properties': {'id': 1005, 'username': 'admin', 'email': "gabriel@admin.com", 'name': 'Gabriel',
                           'terms_agreed': True, 'receive_notification_by_email': False}
        }
        self.put(
            resource, status_code=400,
            expected_text="Attribute already exists. (error: Key (username)=(admin) already exists.)"
        )

        self.auth_logout()

    def test__put_api_user__400_bad_request__attribute_in_JSON_is_missing(self):
        self.auth_login("admin@admin.com", "admin")

        # try to update a user without user id
        resource = {
            'type': 'User',
            'properties': {'email': "gabriel@admin.com", 'name': 'Gabriel',
                           'receive_notification_by_email': False}
        }
        self.put(
            resource, status_code=400,
            expected_text=("Some attribute in the JSON is missing. "
                           "Look at the documentation! (error: 'id' is missing)")
        )

        # try to update a user without username
        resource = {
            'type': 'User',
            'properties': {'id': 1005, 'email': "gabriel@admin.com", 'name': 'Gabriel',
                           'receive_notification_by_email': False}
        }
        self.put(
            resource, status_code=400,
            expected_text=("Some attribute in the JSON is missing. "
                           "Look at the documentation! (error: 'username' is missing)")
        )

        # try to update a user without email
        resource = {
            'type': 'User',
            'properties': {'id': 1005, 'username': 'gabriel', 'name': 'Gabriel',
                           'receive_notification_by_email': False}
        }
        self.put(
            resource, status_code=400,
            expected_text=("Some attribute in the JSON is missing. "
                           "Look at the documentation! (error: 'email' is missing)")
        )

        self.auth_logout()

    def test__put_api_user__401_unauthorized(self):
        # try to update a user
        resource = {
            'type': 'User',
            'properties': {'email': "gabriel@admin.com", 'name': 'Gabriel', 'receive_notification_by_email': False}
        }
        self.put(
            resource, status_code=401,
            expected_text="A valid `Authorization` header is necessary!"
        )

    def test__put_api_user__403_forbidden(self):
        self.auth_login("rafael@admin.com", "rafael")

        # try to update a user with an invalid user
        resource = {
            'type': 'User',
            'properties': {'id': 1005, 'email': "admin@admin.com", 'username': 'gabriel', 'name': 'Gabriel',
                           'terms_agreed': True, 'receive_notification_by_email': False}
        }
        self.put(
            resource, status_code=403,
            expected_text="Just the own user or an administrator can update a user."
        )

        self.auth_logout()

    def test__put_api_user__404_not_found(self):
        self.auth_login("admin@admin.com", "admin")

        # try to update a non-existent user
        resource = {
            'type': 'User',
            'properties': {'id': 999, 'email': "admin@admin.com", 'username': 'gabriel', 'name': 'Gabriel',
                           'terms_agreed': True, 'receive_notification_by_email': False}
        }
        self.put(
            resource, status_code=404,
            expected_text="Not found any resource."
        )

        self.auth_logout()

    # user errors - delete

    def test__delete_api_user__400_bad_request(self):
        self.auth_login("admin@admin.com", "admin")

        for item in ["abc", 0, -1, "-1", "0"]:
            self.delete(argument=item, status_code=400, expected_text="Invalid parameter.")

        self.auth_logout()

    def test__delete_api_user__401_unauthorized(self):
        for item in ["abc", 0, -1, "-1", "0", "1001"]:
            self.delete(
                param=item, status_code=401,
                expected_text="A valid `Authorization` header is necessary!"
            )

    def test__delete_api_user__403_forbidden(self):
        self.auth_login("miguel@admin.com", "miguel")

        # try to delete the user with an invalid user
        self.delete(
            param=1001, status_code=403,
            expected_text="Just administrator can delete other user."
        )

        self.auth_logout()

    def test__delete_api_user__404_not_found(self):
        self.auth_login("admin@admin.com", "admin")

        for item in [5000, 5001]:
            self.delete(argument=item, status_code=404, expected_text="Not found any resource.")

        self.auth_logout()


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
