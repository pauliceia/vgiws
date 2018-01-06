## Login


### GET /auth/google/

This method do social login using a Google account.
- Parameters:
- Examples:
     - Do a social login: http://localhost:8888/auth/google/
- Send:
- Response: a page to do a social login.
- Error codes:
- Notes:


### GET /auth/facebook/

This method do social login using a Facebook account.
- Parameters:
- Examples:
     - Do a social login: http://localhost:8888/auth/facebook/
- Send:
- Response: a page to do a social login.
- Error codes:
- Notes:


### GET /auth/login/

This method do basic login with a user.
- Parameters:
- Examples:
     - Do a basic login: http://localhost:8888/auth/login/
- Send:
- Response:
- Error codes:
    - 500 (Internal Server Error): Problem when do a login. Please, contact the administrator.
- Notes:


### GET /auth/logout/

This method logout a user.
- Parameters:
- Examples:
     - Do logout: http://localhost:8888/auth/logout/
- Send:
- Response:
- Error codes:
    - 404 (Not Found): Not found any user to logout.
- Notes: