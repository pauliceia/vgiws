## Miscellaneous


### GET /api/capabilities/

This method return the capabilities of the server.
- Parameters:
- Examples:
     - Get the capabilities: http://localhost:8888/api/capabilities/
- Send:
- Response: a JSON that contain the capabilities of the server. Example:
    ```javascript
    {
        "version": "0.0.2",
        "status": {"postgresql": "online", "neo4j": "online"}
    }
    ```
- Error codes:
- Notes:


### GET /api/session/user/

This method return the current user logged.
- Parameters:
- Examples:
     - Get the current user logged: http://localhost:8888/api/session/user/
- Send:
- Response: a JSON that contain the current user logged. Example:
    ```javascript
    {
        'login': {
            'user': {'username': None, 'email': 'test@fake.login', 'id': 1},
            'type_login': 'fakelogin'
        }
    }
    ```
- Error codes:
    - 404 (Not Found): Not found any user.
- Notes: