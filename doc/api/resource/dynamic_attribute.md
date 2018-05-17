## Dynamic Attribute

The attributes of the features can be mapped by a key=value schema, similar with [OSM tag](http://wiki.openstreetmap.org/wiki/Tags).
There are some standard features described in [OSM Map Features](http://wiki.openstreetmap.org/wiki/Map_Features) that can be used.
There are also others specifics attributes for Pauliceia project, described below.


### Address

The attributes of addresses can be described by the **addr=*** key of the [OSM address standard](http://wiki.openstreetmap.org/wiki/Key:addr). Some valid dynamic attributes:

| Key                            | Value                               | Feature                   | Comment                                                      |
| ------------------------------ | ----------------------------------- | ------------------------- | ------------------------------------------------------------ |
| addr:street                    | text (e.g. "Rua São Francisco")     | point, line, polygon      | The street of a address                                      |
| addr:housenumber               | text (e.g. "760")                   | point, line, polygon      | The number of a address                                      |
| addr:city                      | text (e.g. "São Paulo")             | point, line, polygon      | The city of a address                                        |
| addr:postcode                  | text (e.g. "22345-224")             | point, line, polygon      | The postcode of a address                                    |


### Attribute Translation

The attributes can be described in different languages. To do it, it is recommended to follow the [OSM rules](http://wiki.openstreetmap.org/wiki/Wiki_Translation). Basically follow the schema: \<attribute>:\<language>.

| Key                            | Value                               | Feature                        | Comment                                                      |
| ------------------------------ | ----------------------------------- | ------------------------------ | ------------------------------------------------------------ |
| description                    | text (e.g. "Good morning")          | all                            | A description text on english (default)                      |
| description:pt-br              | text (e.g. "Bom dia")               | all                            | A description text on brazilian portuguese                   |
| description:jp                 | text (e.g. "Ohayo")                 | all                            | A description text on japanese                              |


### Authors

How to describe the data author:

| Key                            | Value                               | Feature                        | Comment                                                                          |
| ------------------------------ | ----------------------------------- | ------------------------------ | -------------------------------------------------------------------------------- |
| original_author                | text (e.g. "tolkien")               | all                            | The username of the original user of the data (e.g. the writer of the article)   |
| created_by                     | text (e.g. "jorge")                 | all                            | The username of the user who added the data in system                            |


### Date

How to describe the dates.

| Key                            | Value                               | Feature                        | Comment                                                      |
| ------------------------------ | ----------------------------------- | ------------------------------ | ------------------------------------------------------------ |
| start_date                     | date (e.g. "1930", "1917/05/13")    | point, line, polygon, layer    | The date that the data started to exist                      |
| end_date                       | date (e.g. "1900/03/25", "1890/03") | point, line, polygon, layer    | The date that the data finished to exist                     |

The date format accepts are YYYY, YYYY/MM or YYYY/MM/DD.


### Documents

Attach documents or files in a feature following the schema: doc:<source_name>:\<number>:\<attribute>, being:
- <source_name>: the name of the source.
- \<number>: it is possible add more than one source with the same name (more than one video, photo and etc.).
- \<attribute>: the attribute of the source.

| Key                            | Value                                                             | Feature                   | Comment                                            |
| ------------------------------ | ----------------------------------------------------------------- | ------------------------- | -------------------------------------------------- |
| doc:youtube                    | link (e.g. "https://www.youtube.com/")                            | point, line, polygon      | Web link for a video                               |
| doc:youtube:description        | text (e.g. "A historical video")                                  | point, line, polygon      | A textual description of web link                  |
| doc:google_photos              | link (e.g. "https://www.google.com/photos/about/?hl=pt-BR")       | point, line, polygon      | Web link for a photos or album of photos           |
| doc:dropbox                    | link (e.g. "https://www.dropbox.com/pt_BR/")                      | point, line, polygon      | Web link for a dropbox repository                  |
| doc:instagram:01               | link (e.g. "https://www.instagram.com/?hl=pt-br")                 | point, line, polygon      | The first web link for a photo                     |
| doc:instagram:02               | link (e.g. "https://www.instagram.com/?hl=pt-br")                 | point, line, polygon      | The second web link for a photo                    |


### Notification's attributes

To create a new notification, is necessary to insert at least three dynamic attributes: body, type and url, where:
- body: is the textual description of the notification;
- type: is the type of the notification. With it, the consumer can choose a icon or do other computation;
- url: is the url of the notification. Clicking in it, will redirect to a page with more information about the notification.

The **type=*** key can be one of these options:

| Key                            | Value                               | Feature                   | Comment                                                      |
| ------------------------------ | ----------------------------------- | ------------------------- | ------------------------------------------------------------ |
| type                           | award                               | notification              | Notification about a award gained                            |
| type                           | birthday                            | notification              | Notification received when is the user's birthday            |
| type                           | group                               | notification              | Notification about a group                                   |
| type                           | layer                               | notification              | Notification about a layer                                   |
| type                           | point                               | notification              | Notification when the user receive some punctuation          |
| type                           | project                             | notification              | Notification about a project                                 |
| type                           | review                              | notification              | Notification when there is some review on a layer            |


### Sources

How to describe the data source following the schema: source:<source_name>:\<attribute>, being:
- <source_name>: the name of the source.
- \<attribute>: the attribute of the source.

| Key                            | Value                                                        | Feature                   | Comment                                       |
| ------------------------------ | ------------------------------------------------------------ | ------------------------- | --------------------------------------------- |
| source:book :title            | text (e.g. "Book of addresses")                              | point, line, polygon      | Title of a book                               |
| source:newspaper :title        | text (e.g. "Jornal about SP in 1880")                        | point, line, polygon      | Title of a newspaper                          |
| source:article:title           | text (e.g. "Article about crimes in 1930")                   | point, line, polygon      | Title of a article                            |
| source:article:link            | link (e.g. "http://www.scielo.br")                           | point, line, polygon      | Web link of a article                         |
| source:article:bibtex          | text (e.g. "@article{aquino2017sumat, title={Suma T.}, ...") | point, line, polygon      | Reference of the article on Bibtex            |
| source:article:apa             | text (e.g. "Aquino (2017). Suma T. Journal, 10(2), 11-21.")  | point, line, polygon      | Reference of the article on APA               |


### Themes

How to describe the themes on layers:

| Key                            | Value                               | Feature                   | Comment                                                      |
| ------------------------------ | ----------------------------------- | ------------------------- | ------------------------------------------------------------ |
| theme                          | text (e.g. "generic", "crime")      | layer                     | The theme of a layer                                         |


<!-- ### Map vectorization -->

<!-- How to describe when the data is provide by map vectorization: -->

<!-- | Key                            | Value                               | Feature                   | Comment                                                      | -->
<!-- | ------------------------------ | ----------------------------------- | ------------------------- | ------------------------------------------------------------ | -->
<!-- | map_vectorization              | boolean (e.g. "true" or "false")    | line, polygon             | If the data was created by a map vectorization               | -->
