## Attributes

The attributes of the features can be mapped by a key=value schema, similar with [OSM tag](http://wiki.openstreetmap.org/wiki/Tags).
There are some standard features described in [OSM Map Features](http://wiki.openstreetmap.org/wiki/Map_Features) that can be used.
There are also others specifics attributes for Pauliceia project, described below.


### Authors

How to describe the data author:

| Key                            | Value                          | Element              | Comment                                                      |
| ------------------------------ | ------------------------------ | -------------------- | ------------------------------------------------------------ |
| original_author                | text (e.g. "J. R. R. Tolkien") | node, way or area    | The original author of the data                              |
| feeder_author                  | text (e.g. "Jorge")            | node, way or area    | The user that feeding the system, who make changes in data   |


### Sources

How to describe the data source following the schema: source:<source_name>:\<number>:\<attribute>, being:
- <source_name>: the name of the source.
- \<number>: it is possible add more than one source with the some name (more than one video, photo and etc.).
- \<attribute>: the attribute of the source.

Examples:

| Key                            | Value                                                             | Element              | Comment                                            |
| ------------------------------ | ----------------------------------------------------------------- | -------------------- | -------------------------------------------------- |
| source:youtube                 | text (e.g. "https://www.youtube.com/")                            | node, way or area    | Web link for a video                               |
| source:youtube:description     | text (e.g. "A historical video")                                  | node, way or area    | A textual description of web link                  |
| source:google_photos           | text (e.g. "https://www.google.com/photos/about/?hl=pt-BR")       | node, way or area    | Web link for a photos or album of photos           |
| source:dropbox                 | text (e.g. "https://www.dropbox.com/pt_BR/")                      | node, way or area    | Web link for a dropbox repository                  |
| source:instagram:01            | text (e.g. "https://www.instagram.com/?hl=pt-br")                 | node, way or area    | The first web link for a photo                     |
