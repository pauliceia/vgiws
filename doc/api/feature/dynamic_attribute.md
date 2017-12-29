## Dynamic Attribute

The attributes of the features can be mapped by a key=value schema, similar with [OSM tag](http://wiki.openstreetmap.org/wiki/Tags).
There are some standard features described in [OSM Map Features](http://wiki.openstreetmap.org/wiki/Map_Features) that can be used.
There are also others specifics attributes for Pauliceia project, described below.


### Attribute Translation

The attributes can be described in different languages. To do it, it is recommended to follow the [OSM rules](http://wiki.openstreetmap.org/wiki/Wiki_Translation).

Examples:

| Key                            | Value                                                        | Element                   | Comment                                       |
| ------------------------------ | ------------------------------------------------------------ | ------------------------- | --------------------------------------------- |
| description                    | text on english (default) (e.g. "Good morning")              | all                       | Title of a book                               |
| description:pt-br              | text on brazilian portuguese (e.g. "Bom dia")                | all                       | Title of a newspaper                          |
| description:jp                 | text on japanese (e.g. "Ohayo")                              | all                       | Title of a article                            |


### Authors

How to describe the data author:

| Key                            | Value                               | Element                   | Comment                                                                          |
| ------------------------------ | ----------------------------------- | ------------------------- | -------------------------------------------------------------------------------- |
| original_author                | text (e.g. "tolkien")               | all                       | The username of the original user of the data                                    |
| created_by                     | text (e.g. "jorge")                 | all                       | The username of the user that is feeding the system, who make changes in data    |


### Date

How to describe the dates.

| Key                            | Value                               | Element                   | Comment                                                      |
| ------------------------------ | ----------------------------------- | ------------------------- | ------------------------------------------------------------ |
| start_date                     | date (e.g. "1930", "1917/05/13")    | point, line, polygon      | The date that the data started to exist                      |
| end_date                       | date (e.g. "1900/03/25", "1890/03") | point, line, polygon      | The date that the data finished to exist                     |

The date format accepts are YYYY, YYYY/MM or YYYY/MM/DD.


### Documents

Attach documents or files in a feature following the schema: doc:<source_name>:\<number>:\<attribute>, being:
- <source_name>: the name of the source.
- \<number>: it is possible add more than one source with the some name (more than one video, photo and etc.).
- \<attribute>: the attribute of the source.

Examples:

| Key                            | Value                                                             | Element                   | Comment                                            |
| ------------------------------ | ----------------------------------------------------------------- | ------------------------- | -------------------------------------------------- |
| doc:youtube                    | link (e.g. "https://www.youtube.com/")                            | point, line, polygon      | Web link for a video                               |
| doc:youtube:description        | text (e.g. "A historical video")                                  | point, line, polygon      | A textual description of web link                  |
| doc:google_photos              | link (e.g. "https://www.google.com/photos/about/?hl=pt-BR")       | point, line, polygon      | Web link for a photos or album of photos           |
| doc:dropbox                    | link (e.g. "https://www.dropbox.com/pt_BR/")                      | point, line, polygon      | Web link for a dropbox repository                  |
| doc:instagram:01               | link (e.g. "https://www.instagram.com/?hl=pt-br")                 | point, line, polygon      | The first web link for a photo                     |


### Sources

How to describe the data source following the schema: source:<source_name>:\<attribute>, being:
- <source_name>: the name of the source.
- \<attribute>: the attribute of the source.

Examples:

| Key                            | Value                                                        | Element                   | Comment                                       |
| ------------------------------ | ------------------------------------------------------------ | ------------------------- | --------------------------------------------- |
| source\:book:title             | text (e.g. "Book of addresses")                              | point, line, polygon      | Title of a book                               |
| source\:newspaper:title        | text (e.g. "Jornal about SP in 1880")                        | point, line, polygon      | Title of a newspaper                          |
| source:article:title           | text (e.g. "Article about crimes in 1930")                   | point, line, polygon      | Title of a article                            |
| source:article:link            | link (e.g. "http://www.scielo.br")                           | point, line, polygon      | Web link of a article                         |
| source:article:bibtex          | text (e.g. "@article{aquino2017sumat, title={Suma T.}, ...") | point, line, polygon      | Reference of the article on Bibtex            |
| source:article:apa             | text (e.g. "Aquino (2017). Suma T. Journal, 10(2), 11-21.")  | point, line, polygon      | Reference of the article on APA               |


### Themes

How to describe the themes on layers:

| Key                            | Value                               | Element                   | Comment                                                      |
| ------------------------------ | ----------------------------------- | ------------------------- | ------------------------------------------------------------ |
| theme                          | text (e.g. "generic", "crime")      | layer                     | The theme of a layer                                         |


<!-- ### Map vectorization -->

<!-- How to describe when the data is provide by map vectorization: -->

<!-- | Key                            | Value                               | Element                   | Comment                                                      | -->
<!-- | ------------------------------ | ----------------------------------- | ------------------------- | ------------------------------------------------------------ | -->
<!-- | map_vectorization              | boolean (e.g. "true" or "false")    | line, polygon             | If the data was created by a map vectorization               | -->
