import sqlite3

conexion = sqlite3.connect("test.db") #conectar a la BBDD 

#para poder modificar datos obtenidos
conexion.row_factory =sqlite3.Row

#crear el cursor para ejecutar comando SQL
cursor = conexion.cursor() 

#Ejecutar la sentencia SQL
respuesta = cursor.execute("SELECT * FROM datospeople;")

#print(respuesta.fetchall())

resultado = [dict(fila) for fila in respuesta.fetchall()]
print (resultado)