/*Para crear la BBDD de producción en "DB Browser for SQLite"*/

CREATE TABLE "comentario" (
	"id"	INTEGER,
	"id_pelicula"	TEXT NOT NULL UNIQUE,
	"persona"	TEXT NOT NULL,
	"comentario"	TEXT,
	"fecha"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);


/*BBDD de Test*/ 

CREATE TABLE "datospeople" (
	"id"	INTEGER,
	"name"	TEXT NOT NULL,
	"lastname"	TEXT NOT NULL,
	"dni"	TEXT NOT NULL UNIQUE,
	"email"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);