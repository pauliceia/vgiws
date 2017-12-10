// ************************************************************
// clean database
// ************************************************************
MATCH (n) DETACH DELETE n;


// ************************************************************
// create a constraint for the field 'key' to be unique
// ************************************************************
CREATE CONSTRAINT ON (theme:Theme) ASSERT theme.key IS UNIQUE;


// >>> here start a big CREATE command

// ************************************************************
// master node
// ************************************************************
CREATE (generic:Theme {key:"generic"})


// ************************************************************
// cultural_place (child of master)
// ************************************************************
CREATE (cultural_place:Theme {key:"cultural_place"})
// children of cultural_place
CREATE (theater:Theme {key:"theater"})
CREATE (cinema:Theme {key:"cinema"})

// connections
CREATE (generic)-[:can_be]->(cultural_place)
CREATE (cultural_place)-[:can_be]->(theater)
CREATE (cultural_place)-[:can_be]->(cinema)

// ************************************************************
// crime (child of master)
// ************************************************************
CREATE (crime:Theme {key:"crime"})

// children of crime
CREATE (assalt:Theme {key:"assalt"})
CREATE (robbery:Theme {key:"robbery"})

// connections
CREATE (generic)-[:can_be]->(crime)
CREATE (crime)-[:can_be]->(assalt)
CREATE (crime)-[:can_be]->(robbery)


// ************************************************************
// building (child of master)
// ************************************************************
CREATE (building:Theme {key:"building"})

// children of building
CREATE (school:Theme {key:"school"})
CREATE (hospital:Theme {key:"hospital"})

// connections
CREATE (generic)-[:can_be]->(building)
CREATE (building)-[:can_be]->(school)
CREATE (building)-[:can_be]->(hospital);

// >>> here finish the big CREATE command






// ************************************************************
// code tests
// ************************************************************

// get a tree graph
/*
MATCH path = (generic:Theme {key: "generic"})-[:can_be*]-(:Theme)
WITH collect(path) as paths
CALL apoc.convert.toTree(paths) yield value
RETURN value;
*/













