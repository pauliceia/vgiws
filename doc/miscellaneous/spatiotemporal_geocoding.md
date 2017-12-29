## Spatiotemporal Geocoding


The addresses and the streets can be added in DB using the GeoJSON format default of the VGIWS.

The GeoJSONs described in the next sections are examples, so can be modified as you want, adding others attributes. For more detail see [Dynamic Attribute](../api/feature/dynamic_attribute.md). For more detail how to add elements, see [Element](../api/feature/element.md).

**Remember yourself:**
- The 'fk_changeset_id' key has to contain the id of the changeset created to add the feature. In the examples are 200, so change it.
- The id of a feature is created AFTER the GeoJSON is sent to server. After the data is saved in DB, it is returned the id generated. Because of that, the 'id' key is represented with a -1.


### Insert a address

Use the method: ```PUT /api/point/create```, sending the follow GeoJSON:

```javascript
{
    'type': 'FeatureCollection',
    'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
    'features': [
        {
            'tags': [{'k': 'addr:housenumber', 'v': '10'},
                     {'k': 'start_date', 'v': '1910/12/25'},
                     {'k': 'end_date', 'v': '1917/05/13'}],
            'type': 'Feature',
            'properties': {'id': -1, 'fk_changeset_id': 200},
            'geometry': {
                'type': 'MultiPoint',
                'coordinates': [[-23.546421, -46.635722]]
            },
        }
    ]
}
```


### Insert a street

Use the method: ```PUT /api/line/create```, sending the follow GeoJSON:

```javascript
{
    'type': 'FeatureCollection',
    'crs': {"properties": {"name": "EPSG:4326"}, "type": "name"},
    'features': [
        {
            'type': 'Feature',
            'geometry': {
                'coordinates': [[[338.261003, 7384.32995],
                                 [330.933908, 7334.48247],
                                 [337.895545, 7386.25192]]],
                'type': 'MultiLineString'
            },
            'tags': [{'k': 'addr:street', 'v': 'Rua São Francisco Marto'},
                     {'k': 'start_date', 'v': '1900/03/25'},
                     {'k': 'end_date', 'v': '1916/06/24'}],
            'properties': {'id': -1, 'fk_changeset_id': 200}
        }
    ]
}
```
