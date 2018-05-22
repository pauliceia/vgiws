## Theme

The layer themes are saved in a Neo4j database. To access the Neo4j, use: ```http://localhost:7474/browser/```

### GET /api/theme/tree

This method gets the theme tree in JSON format.
- Parameters:
- Examples:
     - Get the theme tree: http://localhost:8888/api/theme/tree
- Send:
- Response: a JSON that contain the features selected. Example:
    ```javascript
    {
        'columns': ['value'],
        'data': [
            [
                {
                    'key': 'generic', '_id': 0, '_type': 'Theme',
                    'can_be': [
                        {
                            'key': 'cultural_place', '_id': 1, '_type': 'Theme',
                            'can_be': [{'key': 'theater', '_id': 2, '_type': 'Theme'},
                                       {'key': 'cinema', '_id': 3, '_type': 'Theme'}]
                        },
                        {
                            'key': 'crime', '_id': 4, '_type': 'Theme',
                            'can_be': [{'key': 'assalt', '_id': 5, '_type': 'Theme'},
                                       {'key': 'robbery', '_id': 6, '_type': 'Theme'}]
                        },
                        {
                            'key': 'building', '_id': 7, '_type': 'Theme',
                            'can_be': [{'key': 'school', '_id': 8, '_type': 'Theme'},
                                       {'key': 'hospital', '_id': 9, '_type': 'Theme'}],
                        }
                    ]
                }
            ]
        ]
    }
    ```
- Error codes:
    - 500 (Internal Server Error): Problem when get the theme tree. Please, contact the administrator.
    - 503 (Service Unavailable): Connection refused. Please, contact the administrator.
- Notes:
