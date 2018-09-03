## Import


### POST /api/import/shp/?\<params>

This method imports a ShapeFile as feature table of a layer.
- Parameters:
    - f_table_name (mandatory) (text): the name of the layer/feature table used to save the ShapeFile (e.g. points);
    - file_name (mandatory) (text): the file name of the zip with the extension (e.g. points.zip);
    - changeset_id (mandatory) (integer): the created changeset;
- Examples:
    - Import a ShapeFile: ```POST http://localhost:8888/api/import/shp/?f_table_name=points&file_name=points.zip&changeset_id=1001```
- Send:
    - Send the binary of the zip file.
- Response:
- Error codes:
     - 400 (Bad Request): Invalid file name: \<FILE_NAME\>. It is necessary to be a zip.
     - 400 (Bad Request): Invalid ZIP! It is necessary to exist a ShapeFile (.shp) inside de ZIP.
     - 400 (Bad Request): It is necessary to pass the f_table_name, file_name and changeset_id in request.
     - 400 (Bad Request): It is necessary to pass one binary zip file in the body of the request.
     - 400 (Bad Request): Feature table name can not have special characters.
     - 400 (Bad Request): Feature table name can not start with number.
     - 403 (Forbidden): Just the owner of the layer or administrator can create/update a feature table or do a import.
     - 404 (Not Found): Not found any layer with the passed f_table_name. It is needed to create a layer with the f_table_name before of using this function.
     - 404 (Not Found): Not found .prj inside the zip.
     - 409 (Conflict): File is not a zip file.
     - 409 (Conflict): It was not possible to find the EPSG of the Shapefile.
     - 409 (Conflict): Invalid .prj.
     - 500 (Internal Server Error): Problem when to import the Shapefile. OGR was not able to import.
     - 500 (Internal Server Error): Problem when import a resource. Please, contact the administrator.
- Notes:
    - It is necessary create a new layer without a feature table before to import the ShapeFile.
    - Inside the zip must have just the ShapeFile.
