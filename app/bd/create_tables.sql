/*Para crear la BBDD de producción en "DB Browser for SQLite"*/

CREATE TABLE "comentario" (
	"id"	INTEGER,
	"id_pelicula"	TEXT NOT NULL,
	"id_usuario"	INTEGER NOT NULL,
	"comentario"	TEXT NOT NULL,
	"fecha"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_usuario") REFERENCES "usuario"("id")
);


CREATE TABLE "usuario" (
	"id"	INTEGER,
	"username"	TEXT NOT NULL UNIQUE,
	"nombre_a_mostrar"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);