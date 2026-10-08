#Separamos la lógica MVC (Modelo-Vista-Controlador)
#Clase "Conexion" para conectarnos a la base de datos

import sqlite3

def formato(respuesta):
    lista_final=[]
    for fila in respuesta.fetchall():
        lista_final.append(dict(fila))
        print(lista_final)

class Conexion:
    def __init__(self,sql_query,parametro=[]): #Inicializo clase y lista vacía [] por default. 
        #conectar a la BBDD
        self.con=sqlite3.connect("test.db") 
        #row factory para poder formatearlo 
        self.con.row_factory = sqlite3.Row  
        #creo el objeto de clase "cursor" para poder ejecutar las consultas contra SQlite a través de este método.  
        self.cur = self.con.cursor()
        #Le paso la query "sql_query" y "parametro" en el caso que quiera hacer un INSERT / UPDATE, por ejemplo, en una lista. 
        self.res = self.cur.execute(sql_query,parametro)


#Ejecutar la sentencia SQL
conexionSelect = Conexion('SELECT * FROM datospeople;')

respuesta = conexionSelect.res
formato(respuesta)
conexionSelect.con.close()
#print(respuesta.fetchall())

#resultado = [dict(fila) for fila in respuesta.fetchall()]
#print (resultado)


##-------##

#Ejecutar sentencia BY

#Ejecutar la sentencia SQL
#"""conexionSelectBy = Conexion("SELECT * from datospeople WHERE id = 3;")

#respuesta2 = conexionSelectBy.res
#formato(respuesta2)
#conexionSelectBy.con.close()
#"""

#Ejecutar la sentencia SQL para insertar un valor
conexionInsert = Conexion('INSERT INTO datospeople(name,lastname,dni,email) VALUES (?,?,?,?);',["Alonso","Sánchez","1717171717F","alonso5@mail.com"])
respuesta3 = conexionInsert.res
conexionInsert.con.commit() #para confirmar el guardado en la BBDD
conexionInsert.con.close()