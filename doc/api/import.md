## Import

### POST /api/import/shp/?\<params>

This method imports a ShapeFile as feature table of a layer.
- Parameters:
    - f_table_name (mandatory) (text): the name of the layer/feature table used to save the ShapeFile (e.g. points).
    - file_name (mandatory) (text): the file name of the zip with the extension (e.g. points.zip).
- Examples:
    - Import a ShapeFile: ```DELETE http://localhost:8888/api/import/shp/?f_table_name=points&file_name=points.zip```
- Send:
    - Send the binary of the zip file.
- Response:
- Error codes:
     - 400 (Bad Request): Invalid file name: \<FILE_NAME\>. It is necessary to be a zip.
     - 400 (Bad Request): Invalid ZIP! It is necessary to exist a ShapeFile (.shp) inside de ZIP.
     - 500 (Internal Server Error): Problem when import a resource. Please, contact the administrator.
- Notes:
    - It is necessary create a new layer without a feature table before to import the ShapeFile.
    - Inside the zip must have just the ShapeFile.
