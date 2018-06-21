## Miscellaneous


### GET /api/user_by_token/

This method return the current logged user.
- Parameters:
- Examples:
     - Get the current logged user: http://localhost:8888/api/user_by_token/
- Send (in Body):
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response: a JSON that contains the resource. Example:
    ```javascript
    {
        'properties': {
            'username': 'rodrigo', 'is_the_admin': True, 'user_id': 1002,
            'email': 'rodrigo@admin.com', 'terms_agreed': True, 'name': 'Rodrigo',
            'is_email_valid': True, 'receive_notification_by_email': False
        },
        'type': 'User'
    }
    ```
- Error codes:
    - 400 (Bad Request): Invalid Token.
    - 401 (Unauthorized): It is necessary an Authorization header valid.
- Notes:


### GET /api/validate_email/\<token>

This method validate a email account by \<token>.
- Parameters:
- Examples:
     - Validate email account: http://localhost:8888/api/validate_email/3XUE89Q98Q3E83HXH38D
- Send (in Body):
- Send (in Header):
- Response:
- Error codes:
    - 400 (Bad Request): Invalid Token.
- Notes:


<!-- ### GET /api/capabilities/ -->

<!-- This method return the capabilities of the server. -->
<!-- - Parameters: -->
<!-- - Examples: -->
<!-- - Get the capabilities: http://localhost:8888/api/capabilities/ -->
<!-- - Send: -->
<!-- - Response: a JSON that contain the capabilities of the server. Example: -->
<!-- ```javascript -->
<!-- { -->
<!-- "version": "0.0.2", -->
<!-- "status": {"postgresql": "online", "neo4j": "online"} -->
<!-- } -->
<!-- ``` -->
<!-- - Error codes: -->
<!-- - Notes: -->
