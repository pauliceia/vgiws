DROP FUNCTION IF EXISTS verify_if_geometry_is_inside_other_geometry(table_name regclass, xmin FLOAT, ymin FLOAT, xmax FLOAT, ymax FLOAT, EPSG INT);

CREATE or REPLACE FUNCTION verify_if_geometry_is_inside_other_geometry(table_name regclass, xmin FLOAT, ymin FLOAT, xmax FLOAT, ymax FLOAT, EPSG INT)
RETURNS BOOLEAN AS $$
DECLARE
	bb_default_city GEOMETRY;
	union_f_table GEOMETRY;
	result BOOLEAN;
BEGIN
	-- create a bounding box of the default city (by default is SP city)
	EXECUTE format('SELECT  ST_Transform(
			    ST_MakeEnvelope (
				%s, %s,
				%s, %s,
				%s
			    )
			, 4326) as geom', xmin, ymin, xmax, ymax, EPSG) INTO bb_default_city;

	-- get the union of a feature table (shapefile)
	EXECUTE format('SELECT ST_Transform(ST_Union(geom), 4326) as geom FROM %s', table_name) INTO union_f_table;


	-- check if the shapefile is inside the bounding box
	IF (LOWER(ST_GeometryType(union_f_table)) = 'geometrycollection') THEN
		-- result := (ST_Within(ST_Buffer(ST_MakeValid(union_f_table), 0), bb_default_city));
		result := (ST_Within(ST_Buffer(union_f_table, 0), bb_default_city));

	ELSE
		--result := (ST_Within(ST_MakeValid(union_f_table), bb_default_city));
		result := (ST_Within(ST_Buffer(ST_MakeValid(union_f_table), 0), bb_default_city));

	END IF;

	raise notice 'ST_GeometryType = %s', LOWER(ST_GeometryType(union_f_table));


	RETURN result;
END;
$$ LANGUAGE plpgsql;


-- SELECT verify_if_geometry_is_inside_other_geometry('deinfo_centrais_cooperativas', 313389.67, 7343788.61, 360663.23, 7416202.05, 29193);






/*

CREATE or REPLACE FUNCTION verify_if_geometry_is_inside_other_geometry(table_name regclass, xmin FLOAT, ymin FLOAT, xmax FLOAT, ymax FLOAT, EPSG INT)
RETURNS BOOLEAN AS $$
DECLARE
	result BOOLEAN;
BEGIN

	EXECUTE format('SELECT ST_Within(union_f_table.geom, bb_default_city.geom) as row_to_json
		FROM
		(
			-- get the union of a feature table (shapefile)
			SELECT ST_Transform(ST_Union(geom), 4326) as geom FROM %s
		) union_f_table,
		(
			-- create a bounding box of the default city (by default is SP city)
			SELECT  ST_Transform(
			    ST_MakeEnvelope (
				%s, %s,
				%s, %s,
				%s
			    )
			, 4326) as geom
		) bb_default_city', table_name, xmin, ymin, xmax, ymax, EPSG) INTO result;

	RETURN result;
END;
$$ LANGUAGE plpgsql;


SELECT verify_if_geometry_is_inside_other('deinfo_centrais_cooperativas', 313389.67, 7343788.61, 360663.23, 7416202.05, 29193);




CREATE or REPLACE FUNCTION verify_if_geometry_is_inside_other() RETURNS boolean AS $$
DECLARE
    result boolean;
BEGIN

	result := (SELECT ST_Within(union_f_table.geom, bb_default_city.geom) as row_to_json
			FROM
			(
				-- get the union of a feature table (shapefile)
				SELECT ST_Transform(ST_Union(geom), 4326) as geom FROM deinfo_centrais_cooperativas
			) union_f_table,
			(
				-- create a bounding box of the default city (by default is SP city)
				SELECT  ST_Transform(
				    ST_MakeEnvelope (
					313389.67, 7343788.61,
					360663.23, 7416202.05,
					29193
				    )
				, 4326) as geom
			) bb_default_city);

    RETURN result;
END;
$$ LANGUAGE plpgsql;


SELECT verify_if_geometry_is_inside_other();





SELECT ST_Within(ST_Buffer(union_f_table.geom, 0), bb_default_city.geom) as row_to_json
FROM
(
	-- get the union of a feature table (shapefile)
	SELECT ST_Transform(ST_Union(geom), 4326) as geom FROM deinfo_centrais_cooperativas
) union_f_table,
(
	-- create a bounding box of the default city (by default is SP city)
	SELECT  ST_Transform(
	    ST_MakeEnvelope (
		313389.67, 7343788.61,
		360663.23, 7416202.05,
		29193
	    )
	, 4326) as geom
) bb_default_city;

SELECT ST_GeometryType(ST_Transform(ST_Union(geom), 4326)) as geom FROM deinfo_centrais_cooperativas






SELECT ST_Within(ST_Buffer(union_f_table.geom, 0), bb_default_city.geom) as row_to_json
FROM
(
    -- get the union of a feature table (shapefile)
    SELECT ST_Transform(ST_Union(geom), 4326) as geom FROM deinfo_centrais_cooperativas
) union_f_table,
(
-- create a bounding box of the default city (by default is SP city)
SELECT  ST_Transform(
    ST_MakeEnvelope (
	313389.67, 7343788.61,
	360663.23, 7416202.05,
	29193
    )
, 4326) as geom
) bb_default_city;

SELECT ST_GeometryType(ST_Transform(ST_Union(geom), 4326)) as geom FROM deinfo_centrais_cooperativas
*/