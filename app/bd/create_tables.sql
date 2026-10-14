/*Para crear la BBDD de producción en "DB Browser for SQLite"*/

CREATE TABLE "comentario" (
	"id"	INTEGER,
	"id_pelicula"	TEXT NOT NULL,
	"persona"	TEXT NOT NULL,
	"comentario"	TEXT,
	"fecha"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);


CREATE TABLE "usuario" (
	"id"	INTEGER,
	"nombre"	TEXT NOT NULL UNIQUE,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);