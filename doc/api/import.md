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
    - 400 (Bad Request): `f_table_name`, `file_name` and `changeset_id` are required parameters in request.
    - 400 (Bad Request): A binary zip file is required in the body of the request.
    - 400 (Bad Request): f_table_name can not have special characters.
    - 400 (Bad Request): f_table_name can not start with number.
    - 403 (Forbidden): The layer owner or administrator user are who can create or delete this resource.
    - 404 (Not Found): Not found any layer with the passed f_table_name. You need to create a layer with the f_table_name before of using this function.
    - 404 (Not Found): Not found .prj inside the zip.
    - 404 (Not Found): Invalid zip file! Not found a ShapeFile file (i.e. [.shp|.prj|.dbf|.shx]) inside de zip file.
    - 409 (Conflict): File is not a zip file.
    - 409 (Conflict): It was not possible to find one EPSG from the .prj.
    - 409 (Conflict): There is not a list of codes in the result. So it is an invalid .prj.
    - 409 (Conflict): Conflict of f_table_name. The table name is a reserved word. Please, rename it.
    - 409 (Conflict): Shapefile is not inside the default city of the project.
    - 500 (Internal Server Error): Problem when importing the Shapefile file. OGR was not able to import it.
    - 500 (Internal Server Error): Problem when importing the Shapefile file. Fiona was not able to read it. One reason can be that the Shapefile file has an empty column name, then name it inside the `.dbf` file.
    - 500 (Internal Server Error): Some geometries of the Shapefile are with problem. Please, check them and try to import again later.
    - 500 (Internal Server Error): Problem when to import a resource. Please, contact the administrator.
    - 503 (Service Unavailable): Problem with the prj2epsg web service.
- Notes:
    - It is necessary create a new layer without a feature table before to import the ShapeFile.
    - Inside the zip must have just the ShapeFile.
