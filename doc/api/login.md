## Login

This section describes the functions to do a login.


### GET /api/auth/login

This method do a basic login with a user.
- Parameters:
- Examples:
     - Do a basic login: GET http://localhost:8888/auth/login/
- Send (in Body):
- Send (in Header):
    - First encrypt the password with a hash algorithm called SHA512.
    - Concatenate the email and password in one string separated by ":" (e.g. "email:encrypted_password")
    - Encode the string above using the base64 encode. It will return, for example, the string "38749sjq983uj23849j"
    - Concatenate the string "Basic " with the encoded string. It will return, for example, something like this: "Basic 38749sjq983uj23849j"
    - Put this string in the Authorization header.
- Response (in Header):
    - The Authorization header has a valid Token to access the platform.
- Error codes:
    - 404 (Not Found): Not found any user.
    - 409 (Conflict): The email has not been validated.
    - 500 (Internal Server Error): Problem when do a login. Please, contact the administrator.
- Notes:


### PUT /api/auth/change_password

This method change the password of a user.
- Parameters:
- Examples:
     - Change the password: PUT http://localhost:8888/api/auth/change_password
- Send (in Body):
    ```javascript
    {
        'properties': {
            'current_password': 'ENCRYPTED_CURRENT_PASSWORD',
            'new_password': 'ENCRYPTED_NEW_PASSWORD'
        },
        'type': 'ChangePassword'
    }
    ```
- Send (in Header):
    - Send an "Authorization" header with a valid Token.
- Response (in Header):
- Error codes:
    - 400 (Bad Request): It is needed to pass the encrypted current_password and new_password.
    - 401 (Unauthorized): A valid `Authorization` header is necessary!
    - 404 (Not Found): Not found any user.
    - 409 (Conflict): Current password is invalid.
    - 409 (Conflict): The email has not been validated.
    - 500 (Internal Server Error): Problem when changing the password. Please, contact the administrator.
- Notes:
    - The passwords need to be encrypted using a hash algorithm called SHA512.


### GET /api/auth/google/

This method do a social login using a Google account.
- Parameters:
- Examples:
     - Do a social login: GET http://localhost:8888/auth/google/
- Send:
- Response: a page to do a social login.
- Error codes:
    - 400 (Bad Request): Invalid token.
    - 403 (Forbidden): Forbidden request.
    - 500 (Internal Server Error): Problem when do a login. Please, contact the administrator.
- Notes:


### GET /api/auth/facebook/

This method do a social login using a Facebook account.
- Parameters:
- Examples:
     - Do a social login: GET http://localhost:8888/auth/facebook/
- Send:
- Response: a page to do a social login.
- Error codes:
    - 400 (Bad Request): Invalid token.
    - 403 (Forbidden): Forbidden request.
    - 500 (Internal Server Error): Problem when do a login. Please, contact the administrator.
- Notes:


<!-- ### GET /api/auth/logout/ -->

<!-- This method logout a user. -->
<!-- - Parameters: -->
<!-- - Examples: -->
<!-- - Do logout: http://localhost:8888/auth/logout/ -->
<!-- - Send: -->
<!-- - Response: -->
<!-- - Error codes: -->
<!-- - 404 (Not Found): Not found any user to logout. -->
<!-- - Notes: -->
