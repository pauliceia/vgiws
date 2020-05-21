#!/usr/bin/env python
# -*- coding: utf-8 -*-

from util.tester import RequestTester


class TestAPIChangeset(RequestTester):

    def setUp(self):
        self.set_urn('/api/changeset')

    # changeset - get

    def test__get_api_changeset__return_all_changesets(self):
        expected = {
            'features': [
                {
                    'properties': {'created_at': '2017-01-05 00:00:00', 'user_id_creator': 1001, 'changeset_id': 1001,
                                   'closed_at': '2017-01-05 00:00:00', 'layer_id': 1001,
                                   'description': 'Creating layer_1001'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-03-05 00:00:00', 'user_id_creator': 1004, 'changeset_id': 1002,
                                   'closed_at': '2017-03-05 00:00:00', 'layer_id': 1002,
                                   'description': 'Creating layer_1002'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-04-12 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1003,
                                   'closed_at': '2017-04-12 00:00:00', 'layer_id': 1003,
                                   'description': 'Creating layer_1003'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-06-28 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1004,
                                   'closed_at': '2017-06-28 00:00:00', 'layer_id': 1004,
                                   'description': 'Creating layer_1004'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-08-05 00:00:00', 'user_id_creator': 1007, 'changeset_id': 1005,
                                   'closed_at': '2017-08-05 00:00:00', 'layer_id': 1005,
                                   'description': 'Creating layer_1005'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-09-04 00:00:00', 'user_id_creator': 1007, 'changeset_id': 1006,
                                   'closed_at': '2017-09-04 00:00:00', 'layer_id': 1006,
                                   'description': 'Creating layer_1006'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-01-08 00:00:00', 'user_id_creator': 1001, 'changeset_id': 1011,
                                   'closed_at': None, 'layer_id': 1001, 'description': 'An open changeset'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-04-13 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1013,
                                   'closed_at': None, 'layer_id': 1003, 'description': 'Creating an open changeset'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-01-08 00:00:00', 'user_id_creator': 1004, 'changeset_id': 1014,
                                   'closed_at': None, 'layer_id': 1002, 'description': 'An open changeset'},
                    'type': 'Changeset'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.get(expected)

    def test__get_api_changeset__return_changeset_by_changeset_id(self):
        expected = {
            'features': [
                {
                    'properties': {'created_at': '2017-04-12 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1003,
                                   'closed_at': '2017-04-12 00:00:00', 'layer_id': 1003,
                                   'description': 'Creating layer_1003'},
                    'type': 'Changeset'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.get(expected, changeset_id="1003")

    def test__get_api_changeset__return_changeset_by_layer_id(self):
        expected = {
            'features': [
                {
                    'properties': {'created_at': '2017-06-28 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1004,
                                   'closed_at': '2017-06-28 00:00:00', 'layer_id': 1004,
                                   'description': 'Creating layer_1004'},
                    'type': 'Changeset'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.get(expected, layer_id="1004")

    def test__get_api_changeset__return_changeset_by_user_id(self):
        expected = {
            'features': [
                {
                    'properties': {'created_at': '2017-04-12 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1003,
                                   'closed_at': '2017-04-12 00:00:00', 'layer_id': 1003,
                                   'description': 'Creating layer_1003'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-06-28 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1004,
                                   'closed_at': '2017-06-28 00:00:00', 'layer_id': 1004,
                                   'description': 'Creating layer_1004'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-04-13 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1013,
                                   'closed_at': None, 'layer_id': 1003, 'description': 'Creating an open changeset'},
                    'type': 'Changeset'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.get(expected, user_id_creator="1005")

    def test__get_api_changeset__return_all_open_changesets(self):
        expected = {
            'features': [
                {
                    'properties': {'created_at': '2017-01-08 00:00:00', 'user_id_creator': 1001, 'changeset_id': 1011,
                                   'closed_at': None, 'layer_id': 1001, 'description': 'An open changeset'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-04-13 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1013,
                                   'closed_at': None, 'layer_id': 1003, 'description': 'Creating an open changeset'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-01-08 00:00:00', 'user_id_creator': 1004, 'changeset_id': 1014,
                                   'closed_at': None, 'layer_id': 1002, 'description': 'An open changeset'},
                    'type': 'Changeset'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.get(expected, open=True)

    def test__get_api_changeset__return_all_closed_changesets(self):
        expected = {
            'features': [
                {
                    'properties': {'created_at': '2017-01-05 00:00:00', 'user_id_creator': 1001, 'changeset_id': 1001,
                                   'closed_at': '2017-01-05 00:00:00', 'layer_id': 1001,
                                   'description': 'Creating layer_1001'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-03-05 00:00:00', 'user_id_creator': 1004, 'changeset_id': 1002,
                                   'closed_at': '2017-03-05 00:00:00', 'layer_id': 1002,
                                   'description': 'Creating layer_1002'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-04-12 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1003,
                                   'closed_at': '2017-04-12 00:00:00', 'layer_id': 1003,
                                   'description': 'Creating layer_1003'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-06-28 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1004,
                                   'closed_at': '2017-06-28 00:00:00', 'layer_id': 1004,
                                   'description': 'Creating layer_1004'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-08-05 00:00:00', 'user_id_creator': 1007, 'changeset_id': 1005,
                                   'closed_at': '2017-08-05 00:00:00', 'layer_id': 1005,
                                   'description': 'Creating layer_1005'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-09-04 00:00:00', 'user_id_creator': 1007, 'changeset_id': 1006,
                                   'closed_at': '2017-09-04 00:00:00', 'layer_id': 1006,
                                   'description': 'Creating layer_1006'},
                    'type': 'Changeset'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.get(expected, closed=True)

    def test__get_api_changeset__return_all_open_changesets_by_layer_id(self):
        expected = {
            'features': [
                {
                    'properties': {'created_at': '2017-04-13 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1013,
                                   'closed_at': None, 'layer_id': 1003, 'description': 'Creating an open changeset'},
                    'type': 'Changeset'
                }
            ],
            'type': 'FeatureCollection'
        }

        self.get(expected, open=True, layer_id="1003")

    def test__get_api_changeset__return_all_closed_changesets_by_layer_id(self):
        expected = {
            'features': [
                {
                    'properties': {'created_at': '2017-06-28 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1004,
                                   'closed_at': '2017-06-28 00:00:00', 'layer_id': 1004,
                                   'description': 'Creating layer_1004'},
                    'type': 'Changeset'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.get(expected, closed=True, layer_id="1004")

    def test__get_api_changeset__return_all_open_changesets_by_user_id(self):
        expected = {
            'features': [
                {
                    'properties': {'created_at': '2017-01-08 00:00:00', 'user_id_creator': 1001, 'changeset_id': 1011,
                                   'closed_at': None, 'layer_id': 1001, 'description': 'An open changeset'},
                    'type': 'Changeset'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.get(expected, open=True, user_id_creator="1001")

    def test__get_api_changeset__return_all_closed_changesets_by_user_id(self):
        expected = {
            'features': [
                {
                    'properties': {'created_at': '2017-04-12 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1003,
                                   'closed_at': '2017-04-12 00:00:00', 'layer_id': 1003,
                                   'description': 'Creating layer_1003'},
                    'type': 'Changeset'
                },
                {
                    'properties': {'created_at': '2017-06-28 00:00:00', 'user_id_creator': 1005, 'changeset_id': 1004,
                                   'closed_at': '2017-06-28 00:00:00', 'layer_id': 1004,
                                   'description': 'Creating layer_1004'},
                    'type': 'Changeset'
                },
            ],
            'type': 'FeatureCollection'
        }

        self.get(expected, closed=True, user_id_creator="1005")

    def test__get_api_changeset__return_zero_resources(self):
        expected = {'features': [], 'type': 'FeatureCollection'}

        self.get(expected, changeset_id="999")
        self.get(expected, changeset_id="998")

    # changeset - create, close and delete

    def test__post_delete_api_changeset_create_and_close__delete_with_admin(self):
        ##################################################
        # Login
        ##################################################
        self.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # Create the changeset
        ##################################################
        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': 1003},
            'type': 'Changeset'
        }
        changeset_id = self.post_create(changeset)
        changeset["properties"]["changeset_id"] = changeset_id

        ##################################################
        # Close the changeset
        ##################################################
        self.set_urn('/api/changeset/close')

        close_changeset = {
            'properties': {'changeset_id': changeset_id, 'description': 'Creating layer_1003'},
            'type': 'ChangesetClose'
        }
        self.post(close_changeset)

        self.auth_logout()

        ##################################################
        # Delete the changeset
        ##################################################
        # login with an admin user to delete the changeset
        self.auth_login("rodrigo@admin.com", "rodrigo")

        self.set_urn('/api/changeset')

        self.delete(changeset_id=changeset_id)

        ##################################################
        # Logout
        ##################################################
        self.auth_logout()

    def test__post_delete_api_changeset_create_close_and_delete__with_admin(self):
        ##################################################
        # Login
        ##################################################
        self.auth_login("rodrigo@admin.com", "rodrigo")

        ##################################################
        # Create the changeset
        ##################################################
        changeset = {
            'properties': {'changeset_id': -1, 'layer_id': 1003},
            'type': 'Changeset'
        }
        changeset_id = self.post_create(changeset)
        changeset["properties"]["changeset_id"] = changeset_id

        ##################################################
        # Close the changeset
        ##################################################
        self.set_urn('/api/changeset/close')

        close_changeset = {
            'properties': {'changeset_id': changeset_id, 'description': 'Creating layer_1003'},
            'type': 'ChangesetClose'
        }
        self.post(close_changeset)

        ##################################################
        # Delete the changeset
        ##################################################
        self.set_urn('/api/changeset')

        self.delete(changeset_id=changeset_id)

        ##################################################
        # Logout
        ##################################################
        self.auth_logout()


class TestAPIChangesetErrors(RequestTester):

    def setUp(self):
        self.set_urn('/api/changeset')

    # changeset errors - get

    def test__get_api_changeset__400_bad_request(self):
        changesets_ids = ["abc", 0, -1, "-1", "0"]

        for changeset_id in changesets_ids:
            self.get(
                status_code=400, text_message="Invalid parameter.",
                changeset_id=changeset_id
            )

    # changeset errors - create

    def test__post_api_changeset_create__400_bad_request(self):
        ##################################################
        # Login
        ##################################################
        self.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # Try to create a changeset without an attribute
        ##################################################
        resource = {
            'properties': {'description': 'Creating layer_1003'},
            'type': 'Changeset'
        }
        self.post_create(
            resource,
            status_code=400,
            text_message="Some attribute in the JSON is missing. Look at the documentation! (error: 'layer_id' is missing)"
        )

        ##################################################
        # Logout
        ##################################################
        self.auth_logout()

    def test__post_api_changeset_create__401_unauthorized(self):
        ##################################################
        # Try to create a changeset without a logged user
        ##################################################
        resource = {
            'properties': {'changeset_id': -1, 'layer_id': 1003, 'description': 'Creating layer_1003'},
            'type': 'Changeset'
        }
        self.post_create(
            resource,
            status_code=401,
            text_message="A valid `Authorization` header is necessary!"
        )

    # changeset errors - delete

    def test__delete_api_changeset__400_bad_request(self):
        ##################################################
        # Login
        ##################################################
        self.auth_login("rodrigo@admin.com", "rodrigo")

        ##################################################
        # Try to delete changesets
        ##################################################
        changesets_ids = ["abc", 0, -1, "-1", "0"]

        for changeset_id in changesets_ids:
            self.delete(
                status_code=400,
                text_message="Invalid parameter.",
                changeset_id=changeset_id
            )

        ##################################################
        # Logout
        ##################################################
        self.auth_logout()

    def test__delete_api_changeset__401_unauthorized(self):
        ##################################################
        # Try to delete changesets
        ##################################################
        changesets_ids = ["abc", 0, -1, "-1", "0", "1001"]

        for changeset_id in changesets_ids:
            self.delete(
                status_code=401,
                text_message="A valid `Authorization` header is necessary!",
                changeset_id=changeset_id
            )

    def test__delete_api_changeset__403_forbidden(self):
        ##################################################
        # Login
        ##################################################
        self.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # Try to delete changesets
        ##################################################
        changesets_ids = ["abc", 0, -1, "-1", "0", "1001"]

        for changeset_id in changesets_ids:
            self.delete(
                status_code=403,
                text_message="The administrator is who can use this resource.",
                changeset_id=changeset_id
            )

        ##################################################
        # Logout
        ##################################################
        self.auth_logout()

    def test__delete_api_changeset__404_not_found(self):
        ##################################################
        # Login
        ##################################################
        self.auth_login("rodrigo@admin.com", "rodrigo")

        ##################################################
        # Try to delete changesets
        ##################################################
        changesets_ids = ["5000", "5001"]

        for changeset_id in changesets_ids:
            self.delete(
                status_code=404,
                text_message="Not found any resource.",
                changeset_id=changeset_id
            )

        ##################################################
        # Logout
        ##################################################
        self.auth_logout()


class TestAPIChangesetCloseErrors(RequestTester):

    def setUp(self):
        self.set_urn('/api/changeset/close')

    # changeset errors - close

    def test__post_api_changeset_close__400_bad_request(self):
        ##################################################
        # Login
        ##################################################
        self.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # Try to close changesets
        ##################################################
        invalid_changesets_ids = ["abc", 0, -1, "-1", "0"]

        for invalid_changeset_id in invalid_changesets_ids:
            close_changeset = {
                'properties': {'changeset_id': invalid_changeset_id, 'description': 'Creating layer_1003'},
                'type': 'ChangesetClose'
            }
            self.post(close_changeset, status_code=400, text_message="Invalid parameter.")

        ##################################################
        # Logout
        ##################################################
        self.auth_logout()

    def test__post_api_changeset_close__401_unauthorized(self):
        ##################################################
        # Try to close changesets
        ##################################################
        invalid_changesets_ids = ["abc", 0, -1, "-1", "0", "1001", 1001]

        for invalid_changeset_id in invalid_changesets_ids:
            close_changeset = {
                'properties': {'changeset_id': invalid_changeset_id, 'description': 'Creating layer_1003'},
                'type': 'ChangesetClose'
            }
            self.post(close_changeset,
                      status_code=401, text_message="A valid `Authorization` header is necessary!")

    def test__post_api_changeset_close__404_not_found(self):
        ##################################################
        # Login
        ##################################################
        self.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # Try to close changesets
        ##################################################
        invalid_changesets_ids = [
            {
                "changeset_id": "5000",
                "error_message": "Not found the changeset `5000`."
            },
            {
                "changeset_id": "5001",
                "error_message": "Not found the changeset `5001`."
            }
        ]

        for invalid_changeset in invalid_changesets_ids:
            close_changeset = {
                'properties': {
                    'changeset_id': invalid_changeset["changeset_id"],
                    'description': 'Creating layer_1003'
                },
                'type': 'ChangesetClose'
            }
            self.post(close_changeset,
                      status_code=404, text_message=invalid_changeset["error_message"])

        ##################################################
        # Logout
        ##################################################
        self.auth_logout()

    def test__post_api_changeset_close__409_conflict__changeset_has_already_been_closed(self):
        ##################################################
        # Login
        ##################################################
        self.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # Try to close a changeset
        ##################################################
        close_changeset = {
            'properties': {'changeset_id': 1002, 'description': 'Creating layer_1003'},
            'type': 'ChangesetClose'
        }
        self.post(close_changeset,
                  status_code=409,
                  text_message="Changeset `1002` has already been closed at `2017-03-05 00:00:00`.")

        ##################################################
        # Logout
        ##################################################
        self.auth_logout()

    def test__post_api_changeset_close__409_conflict__user_didnt_create_the_changeset(self):
        ##################################################
        # Login
        ##################################################
        self.auth_login("miguel@admin.com", "miguel")

        ##################################################
        # Try to close a changeset
        ##################################################
        close_changeset = {
            'properties': {'changeset_id': 1011, 'description': 'Creating layer_1003'},
            'type': 'ChangesetClose'
        }
        self.post(close_changeset,
                  status_code=409,
                  text_message="The user `1003` didn't create the changeset `1011`.")

        ##################################################
        # Logout
        ##################################################
        self.auth_logout()


# Putting the unittest main() function here is not necessary,
# because this file will be called by run_tests.py
