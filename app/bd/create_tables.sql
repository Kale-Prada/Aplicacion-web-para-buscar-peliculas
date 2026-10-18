/*Para crear la BBDD de producción y sus tablas en "DB Browser for SQLite"*/


/* Sentencia SQL para crear la tabla de comentario. */

CREATE TABLE "comentario" (
	"id"	INTEGER,
	"id_pelicula"	TEXT NOT NULL,
	"id_usuario"	INTEGER NOT NULL,
	"comentario"	TEXT NOT NULL,
	"fecha"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("id_usuario") REFERENCES "usuario"("id")
);


/* Sentencia SQL para crear la tabla de usuario. */

CREATE TABLE "usuario" (
	"id"	INTEGER,
	"username"	TEXT NOT NULL UNIQUE,
	"nombre_a_mostrar"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);


/* Sentencia SQL para crear la tabla de calificaciones. */

CREATE TABLE "calificacion" (
	"id"	INTEGER,
	"id_pelicula"	TEXT NOT NULL,
	"username"	TEXT NOT NULL,
	"puntuacion"	INTEGER CHECK("puntuacion" >= 1 AND "puntuacion" <= 5),
	"fecha"	TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	UNIQUE("id_pelicula","username"),
	FOREIGN KEY("username") REFERENCES "usuario"("username")
);