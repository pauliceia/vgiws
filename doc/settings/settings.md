## Settings

There is a file ("vgiws/settings/settings.py") that contains the configurations about the system.


### Bounding Box Settings

Inside the settings.py file, there is a dictionary that contains the spatial restriction of the system.
By default it is the Bounding Box (BB) of the São Paulo city.

The developer can change the BB for other about another city, such as Rio de Janeiro or Belo Horizonte.

The default dictionary is something like this:

```
__SPATIAL_BB__ = {
    "xmin": 313389.67,
    "ymin": 7343788.61,
    "xmax": 360663.23,
    "ymax": 7416202.05,
    "EPSG": 29193,
}
```

The BB can be found by QGIS in Layer Properties > Metadata > Extent.

