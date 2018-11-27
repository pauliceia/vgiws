/*
	function get_first_projcs_from_prj_in_wkt
*/
DROP FUNCTION IF EXISTS get_first_projcs_from_prj_in_wkt(prj_wkt TEXT);

CREATE or REPLACE FUNCTION get_first_projcs_from_prj_in_wkt(prj_wkt TEXT) 
RETURNS TEXT AS $$
DECLARE
	position_first_quote INT;
	position_next_quote INT;
	prj TEXT;
	projcs TEXT;
BEGIN
	-- # find the first reference of '"'
	-- position_first_quote = prj_wkt.find('"')
	EXECUTE format('SELECT POSITION(''"'' in ''%s'');', prj_wkt) INTO position_first_quote;	

	-- # get the prj starting by '"'
	-- prj = prj_wkt[position_first_quote+1:]
	EXECUTE format('SELECT SUBSTRING(''%s'', %s);', prj_wkt, position_first_quote+1) INTO prj;

	-- # find the next reference of '"'
	-- position_next_quote = prj.find('"')
	EXECUTE format('SELECT POSITION(''"'' in ''%s'');', prj) INTO position_next_quote;	

	-- # get the projcs
	-- projcs = prj[0:position_next_quote]
	EXECUTE format('SELECT SUBSTRING(''%s'', 1, %s-1);', prj, position_next_quote) INTO projcs;

	-- # remove the underscore
	-- projcs = projcs.replace("_", " ")
	EXECUTE format('SELECT REPLACE(''%s'', ''_'', '' '');', projcs) INTO projcs;
	
	-- return projcs
	RETURN projcs;
END;
$$ LANGUAGE plpgsql;

-- test get_first_projcs_from_prj_in_wkt
-- SELECT get_first_projcs_from_prj_in_wkt('PROJCS["Hartebeesthoek94 / Lo15",GEOGCS["Hartebeesthoek94",DATUM["Hartebeesthoek94');


/*
	function get_first_projcs_from_prj_in_wkt
*/
DROP FUNCTION IF EXISTS get_epsg_from_prj(prj_wkt TEXT);

CREATE or REPLACE FUNCTION get_epsg_from_prj(prj_wkt TEXT) 
--RETURNS TABLE (srid INT, auth_name VARCHAR(256), srtext VARCHAR(2048)) AS $$
RETURNS SETOF spatial_ref_sys AS $$
DECLARE
	projcs TEXT;
BEGIN

	projcs := (SELECT get_first_projcs_from_prj_in_wkt(prj_wkt));

	/*
	RAISE NOTICE 'prj_wkt = %', prj_wkt;

	RAISE NOTICE 'projcs = %', projcs;

	FOR table_record IN 
		SELECT srid, auth_name, srtext FROM spatial_ref_sys
		WHERE LOWER(srtext) LIKE LOWER('%' || projcs || '%')
		ORDER BY srid 
	LOOP
		RAISE NOTICE 'table_record.srid = %', table_record.srid;
		RAISE NOTICE 'table_record.auth_name = %', table_record.auth_name;
		RAISE NOTICE 'table_record.srtext = %', table_record.srtext;
	END LOOP;
	*/

	RETURN QUERY 
		SELECT * FROM spatial_ref_sys
		WHERE LOWER(srtext) LIKE LOWER('%' || projcs || '%')
		ORDER BY srid;
END;
$$ LANGUAGE plpgsql;


-- test get_first_projcs_from_prj_in_wkt
SELECT * FROM get_epsg_from_prj('PROJCS["Hartebeesthoek94 / Lo15",GEOGCS["Hartebeesthoek94",DATUM["Hartebeesthoek94');





SELECT srid, auth_name, srtext FROM spatial_ref_sys
WHERE LOWER(srtext) LIKE LOWER('%WGS 84%')
ORDER BY srid;

SELECT srid, auth_name, srtext FROM spatial_ref_sys
WHERE LOWER(srtext) LIKE LOWER('%WGS%84%')
ORDER BY srid;


SELECT REPLACE('abcjisjji__kos\--osdko__akosk+_laspk', '_', ' ');


