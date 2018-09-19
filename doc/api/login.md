## Login

This section describes the functions to do a login.


### GET /api/auth/login/

This method do a basic login with a user.
- Parameters:
- Examples:
     - Do a basic login: GET http://localhost:8888/auth/login/
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
    - 409 (Conflict): The email is not validated.
    - 500 (Internal Server Error): Problem when do a login. Please, contact the administrator.
- Notes:


### GET /api/auth/google/\<TOKEN>

This method do a social login using a Google account.
- Parameters:
- Examples:
     - Do a social login: GET http://localhost:8888/auth/google/EXAMPLE-OF-TOKEN
- Send:
- Response: a page to do a social login.
- Error codes:
    - 400 (Bad Request): Invalid token.
    - 403 (Forbidden): Forbidden request.
    - 409 (Conflict): It is necessary to pass a 'token' in front of URL.
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
    - 409 (Conflict): It is necessary to pass a 'token' in front of URL.
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
