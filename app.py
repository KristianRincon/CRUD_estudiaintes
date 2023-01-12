from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'coltis_materias'
app.config['MYSQL_PORT'] = 3308
mysql = MySQL(app)


@app.route("/")
def saludo():
    return render_template("index.html")


@app.route("/admin/estudiantes")
# va a recibir un parametro adicional que si no le doy un valor empieza con un diccionario vacio
def estudiantes(datos=dict()):

    try:
        sql = """
                SELECT codigo, nombres, apellidos, correo, telefono
                FROM estudiante
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        # la key del diccionario es estudiantes y el valor es la consulta de todos los datos
        datos["estudiantes"] = cursor.fetchall()
        cursor.close()

    except:
        datos["error"] = "Error al consultar los estudiantes"
    # modelo es la variable que va a recibir los datos en la plantilla estudiantes
    return render_template("estudiantes.html", modelo=datos)


@app.route("/admin/estudiantes/nuevo", methods=["POST"])
def nuevo_estudiante():
    # Lo que esta en estudiantes.html en el input se obtiene y se almacena en una variable para luego insertar esos datos en la bd
    codigo = request.form["codigo"]
    nombre = request.form["nombres"]
    apellido = request.form["apellidos"]
    correo = request.form["correo"]
    telefono = request.form["telefono"]

    # Creamos un diccionario para los errores
    datos = dict()

    try:
        sql = f"""
                INSERT INTO estudiante (codigo, nombres, apellidos, correo, telefono)
                VALUES ('{codigo}','{nombre}','{apellido}',
                        '{correo}','{telefono}');
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        filas = cursor.rowcount
        mysql.connection.commit()
        cursor.close()
        if filas != 1:
            # para enviar el error se realiza mediante el diccionario con un key y un valor
            datos["error"] = "Numero de filas afectadas no es correcto"
        else:
            datos["exito"] = f"Estudiante '{nombre} {apellido}' fue registrado exitosamente"

    except:
        datos["error"] = "Error al insertar los datos del estudiante"

    return estudiantes(datos)

# se envia la variable id al metodo para que sea dinamica la seleccion del estudiante en la ruta y asi saber el estudiante a editar


@app.route("/admin/estudiantes/editar/<id>")
def editar(id: str):
    datos = dict()
    try:
        # si el id viene nulo o vacio lanza la excepción
        if id == None or len(id) == 0:
            raise Exception("El codigo no puede estar vacio")

        # Consultar la informacion del estudiante con codigo = id
        sql = f"""
            SELECT codigo, nombres, apellidos, correo, telefono
            FROM estudiante
            WHERE codigo = '{id}'
        """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        # Cargar la información del estudiante en la plantilla
        # la key del diccionario es estudiantes (que a su vez es una tupla con la info del estudiante) y el valor es la consulta de un solo dato
        datos["estudiante"] = cursor.fetchone()
        cursor.close()

        # Mostrar la plantilla

        return render_template("estudiantes_editar.html", modelo=datos)
    except Exception as ex:
        datos["error"] = str(ex)
        return estudiantes(datos)


@app.route("/admin/estudiantes/actualizar", methods=["POST"])
def actualizar_estudiante():
    # Lo que esta en estudiantes.html en el input se obtiene y se almacena en una variable para luego insertar esos datos en la bd
    codigo = request.form["codigo"]
    nombre = request.form["nombres"]
    apellido = request.form["apellidos"]
    correo = request.form["correo"]
    telefono = request.form["telefono"]

    datos = dict()

    try:
        sql = f"""
                UPDATE estudiante
                SET nombres = '{nombre}',
                apellidos = '{apellido}',
                correo = '{correo}',
                telefono = '{telefono}'
                WHERE codigo = '{codigo}';
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        filas = cursor.rowcount
        mysql.connection.commit()
        cursor.close()
        # si el numero de filas afectadas es diferente de 1 muestra un error
        if filas != 1:
            # para enviar el error se realiza mediante el diccionario con un key y un valor
            datos["error"] = "Numero de filas afectadas no es correcto"
        else:
            datos["exito"] = f"Estudiante '{nombre} {apellido}' fue actualizado exitosamente"

    except:
        datos["error"] = "Error al actualizar los datos del estudiante"

    return estudiantes(datos)


@app.route("/admin/estudiantes/eliminar/<id>")
def eliminar(id: str):
    datos = dict()
    try:
        # si el id viene nulo o vacio lanza la excepción
        if id == None or len(id) == 0:
            raise Exception("El codigo no puede estar vacio")

        # Consultar la informacion del estudiante con codigo = id
        sql = f"""
            DELETE
            FROM estudiante
            WHERE codigo = '{id}'
        """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        # con rowcount pregunto cuantas filas se insertaron, eliminaron, modificaron, etc
        filas = cursor.rowcount
        mysql.connection.commit()
        cursor.close()
        if filas != 1:
            # para enviar el error se realiza mediante el diccionario con un key y un valor
            datos["error"] = "Numero de filas afectadas no es correcto"
        else:
            datos["exito"] = f"Estudiante fue  eliminado exitosamente"
    except Exception as ex:
        datos["error"] = str(ex)

    return estudiantes(datos)


@app.route("/admin/materias")
# va a recibir un parametro adicional que si no le doy un valor empieza con un diccionario vacio
def materias(datosM=dict()):

    try:
        sql = """
                SELECT id, nombre, creditos
                FROM materia
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        # la key del diccionario es materias y el valor es la consulta de todos los datos
        datosM["materias"] = cursor.fetchall()
        cursor.close()

    except:
        datosM["error"] = "Error al consultar las materias"
    # modeloM es la variable que va a recibir los datos en la plantilla materias
    return render_template("materias.html", modeloM=datosM)


@app.route("/admin/materias/nuevo", methods=["POST"])
def nueva_materia():
    id = request.form["id"]
    nombre = request.form["nombre"]
    creditos = request.form["creditos"]

    # Creamos un diccionario para los errores (o vaciamos el diccionario datosM)
    datosM = dict()

    try:
        sql = f"""
                INSERT INTO materia (id, nombre, creditos)
                VALUES ('{id}','{nombre}','{creditos}');
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        filas = cursor.rowcount
        mysql.connection.commit()
        cursor.close()
        if filas != 1:
            # para enviar el error se realiza mediante el diccionario con un key y un valor
            datosM["error"] = "Numero de filas afectadas no es correcto"

    except:
        datosM["error"] = "Error al insertar los datos de la materia"

    return materias(datosM)





@app.route("/matriculas")
def matriculas():
    return render_template("matriculas.html")


@app.route("/matriculas/buscar", methods=["POST"])

#datos inicializa como un diccionario vacio
def matriculas_buscar(codigo = None, datos = dict()):
    # "codigo" es el name que tiene el input de la plantilla matriculas el cual trae la info que se escribio en la caja de texto
    if codigo is None:
        codigo = request.form["codigo"]

    try:
        # Consultar datos del estudiante
        sql = f"""
            SELECT codigo, nombres, apellidos, correo, telefono
            FROM estudiante
            WHERE codigo = '{codigo}'
        """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        # Cargar la información del estudiante en la plantilla
        # la key del diccionario es estudiantes (que a su vez es una tupla con la info del estudiante) y el valor es la consulta de un solo dato
        datos["estudiante"] = cursor.fetchone()
        cursor.close()

        # Consultar las materias del estudiante
        sql = f"""
            SELECT ma.id, ma.nombre, ma.creditos
            FROM matricula m
            JOIN materia ma on (m.id_materia = ma.id)
            WHERE m.codigo = '{codigo}'
        """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        # Cargar la información del estudiante en la plantilla
        # la key del diccionario es estudiantes (que a su vez es una tupla con la info del estudiante) y el valor es la consulta de un solo dato
        datos["materias_estudiante"] = cursor.fetchall()
        cursor.close()

        # Consultar todas las materias del sistema
        sql = f"""
            SELECT id, nombre, creditos
            FROM materia
            ORDER BY nombre
        """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        # Cargar la información del estudiante en la plantilla
        datos["materias"] = cursor.fetchall()
        cursor.close()

    except:
        datos["error"] = "No se pudo cargar la informacion del estudiante"

    # Enviar la informacion al formulario
    return render_template("matriculas.html", modelo=datos)


@app.route("/matriculas/agregar", methods=["POST"])
def agregar_matricula():
    codigo = request.form["codigo"]
    materia = request.form["materia"]

    datos = dict()
    try:
        sql = f"""
                INSERT INTO matricula (codigo, id_materia)
                VALUES ('{codigo}', {materia});
            """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        filas = cursor.rowcount
        mysql.connection.commit()
        cursor.close()
        if filas != 1:
            # para enviar el error se realiza mediante el diccionario con un key y un valor
            datos["error"] = "Numero de filas afectadas no es correcto"
        else:
            datos["exito"] = f"materia fue registrada exitosamente"

    except Exception as ex:
        datos["error"] = "Error al insertar la matricula del estudiante"
        print(ex)

    #envia el codigo del estudiante a matricular y los datos recolectados hasta el momento
    return matriculas_buscar(codigo, datos)

@app.route("/matriculas/eliminar/<codigo>/<materia>")
def eliminar_matricula(codigo, materia):
    datos = dict()
    try:
        # si el id viene nulo o vacio lanza la excepción
        if codigo == None or len(codigo) == 0:
            raise Exception("El codigo no puede estar vacio")

        # Consultar la informacion del estudiante con codigo = id
        sql = f"""
            DELETE
            FROM matricula
            WHERE codigo = '{codigo}'
            AND id_materia = {materia}
        """
        cursor = mysql.connection.cursor()
        cursor.execute(sql)
        filas = cursor.rowcount
        mysql.connection.commit()
        cursor.close()
        if filas != 1:
            # para enviar el error se realiza mediante el diccionario con un key y un valor
            datos["error"] = "Numero de filas afectadas no es correcto"
        else:
            datos["exito"] = f"Matricula eliminada exitosamente"
    except Exception as ex:
        datos["error"] = str(ex)

    return matriculas_buscar(codigo, datos)

app.run(debug=True)
