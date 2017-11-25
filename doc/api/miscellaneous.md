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
        "version": "0.0.1",
        "status": {"database": "online"}
    }
    ```
- Error codes:
- Notes: