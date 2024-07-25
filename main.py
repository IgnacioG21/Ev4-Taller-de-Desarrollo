# Importar modulos necesarios
from flask import Flask, render_template, redirect, request, Response, session
from flask_mysqldb import MySQL, MySQLdb

app = Flask(__name__,template_folder='templates')
# Conexión a base de datos
mysql = MySQL()
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'Ev4TDD'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor' # Señalar que el cursor es de tipo diccionario
mysql.init_app(app)

@app.route('/')                                 # Ruta de inicio de sesión (Inicio.html)
def Inicio():
    return render_template('Inicio.html')

@app.route('/JefeRRHH')                         # Ruta de Jefe de RRHH (JefeRRHH.html)
def JefeRRHH():
    # Verificar si el usuario está logueado correctamente o no
    if "Logueado" in session and session["Logueado"]:
        # Obtener el ID del usuario
        Usuario = session.get("ID")

        # Consultar el ID del usuario en la BDD
        sql_IdUsuario = "SELECT ID FROM USUARIOS WHERE ID = %s"
        Conexion = mysql.connection
        with Conexion.cursor() as Cursor:
            Cursor.execute(sql_IdUsuario, (Usuario,))
            IdUsuario = Cursor.fetchone()

        # Si el Id de usuario existe ejecutar...
        if IdUsuario:
            # Unir el Id de Usuario (Tabla Usuarios) con el Id del funcionario (Tabla Funcionario)
            Id_Funcionario = IdUsuario['ID']

            # Consultar BDD para obtener datos de funcionario
            sql_DatosJefeRRHH = "SELECT * FROM FUNCIONARIO WHERE ID = %s"
            sql_DatosLaborales = "SELECT * FROM DATOS_LABORALES WHERE ID_FUNCIONARIO = %s"
            sql_ContactoEmergencia = "SELECT * FROM CONTACTO_EMERGENCIA WHERE ID_FUNCIONARIO = %s"
            sql_CargaFamiliar = "SELECT * FROM CARGA_FAMILIAR WHERE ID_FUNCIONARIO = %s"
            sql_ListadoTrabajadores = """SELECT 
                FUNCIONARIO.RUT,
                FUNCIONARIO.NOMBRE,
                FUNCIONARIO.SEXO,
                DATOS_LABORALES.CARGO,
                DATOS_LABORALES.FECHA_INGRESO,
                DATOS_LABORALES.AREA,
                DATOS_LABORALES.DEPARTAMENTO
            FROM 
                FUNCIONARIO
            INNER JOIN 
                DATOS_LABORALES ON FUNCIONARIO.ID = DATOS_LABORALES.ID_FUNCIONARIO;""";

            with Conexion.cursor() as Cursor:
                # Obtener datos 
                Cursor.execute(sql_DatosJefeRRHH, (Id_Funcionario,))
                Datos_JefeRRHH = Cursor.fetchone()

                Cursor.execute(sql_DatosLaborales, (Id_Funcionario,))
                Datos_Laborales = Cursor.fetchone()

                Cursor.execute(sql_ContactoEmergencia, (Id_Funcionario,))
                Contacto_Emergencia = Cursor.fetchone()

                Cursor.execute(sql_CargaFamiliar, (Id_Funcionario,))
                Carga_Familiar = Cursor.fetchone()

                Cursor.execute(sql_ListadoTrabajadores)
                Listado_Trabajadores = Cursor.fetchall()

        if Datos_JefeRRHH:
            return render_template('JefeRRHH.html', Datos_JefeRRHH = Datos_JefeRRHH, Datos_Laborales = Datos_Laborales, Contacto_Emergencia = Contacto_Emergencia, Carga_Familiar = Carga_Familiar, Listado_Trabajadores = Listado_Trabajadores)
        else:
            return redirect('/')
    # Si el usuario no está logueado se redirige a la pagina de Login
    else:
        return redirect('/')
    

@app.route('/Funcionario')                      # Ruta de Funcionario (Funcionario.html)
def Funcionario():
    # Verificar si el usuario está logueado correctamente o no
    if "Logueado" in session and session["Logueado"]:
        # Obtener el ID del usuario
        Usuario = session.get("ID")

        # Consultar el ID del usuario en la BDD
        sql_IdUsuario = "SELECT ID FROM USUARIOS WHERE ID = %s"
        Conexion = mysql.connection
        with Conexion.cursor() as Cursor:
            Cursor.execute(sql_IdUsuario, (Usuario,))
            IdUsuario = Cursor.fetchone()

        # Si el Id de usuario existe ejecutar...
        if IdUsuario:
            # Unir el Id de Usuario (Tabla Usuarios) con el Id del funcionario (Tabla Funcionario)
            Id_Funcionario = IdUsuario['ID']

            # Consultar BDD para obtener datos de funcionario
            sql_DatosFuncionario = "SELECT * FROM FUNCIONARIO WHERE ID = %s"
            sql_DatosLaborales = "SELECT * FROM DATOS_LABORALES WHERE ID_FUNCIONARIO = %s"
            sql_DatosContacto = "SELECT * FROM CONTACTO_EMERGENCIA WHERE ID_FUNCIONARIO = %s"
            sql_DatosFamiliares = "SELECT * FROM CARGA_FAMILIAR WHERE ID_FUNCIONARIO = %s"

            with Conexion.cursor() as Cursor:
                # Obtener datos de funcionario
                Cursor.execute(sql_DatosFuncionario, (Id_Funcionario,))
                Datos_Funcionario = Cursor.fetchone()
                # Obtener datos laborales
                Cursor.execute(sql_DatosLaborales, (Id_Funcionario,))
                Datos_Laborales = Cursor.fetchone()
                # Obtener datos de contacto
                Cursor.execute(sql_DatosContacto, (Id_Funcionario,))
                Datos_Contacto = Cursor.fetchone()
                # Obtener datos de carga familiar
                Cursor.execute(sql_DatosFamiliares, (Id_Funcionario,))
                Datos_Familiares = Cursor.fetchone()

            # Renderizar plantilla de Funcionario y variable con los datos de este mismo
            if Datos_Funcionario:
                return render_template('Funcionario.html', Datos_Funcionario = Datos_Funcionario, Datos_Laborales = Datos_Laborales, Datos_Contacto = Datos_Contacto, Datos_Familiares = Datos_Familiares)
            else:
                return "No se encontraron datos registrados para este usuario."
            
    # Si el usuario no está logueado se redirige a la pagina de Login
    else:
        return redirect('/')

# Borrar Datos Funcionario
@app.route('/Funcionario/BorrarNombreFuncionario/<int:ID>')
def BorrarNombreFuncionario(ID):
    Conexion = mysql.connection

    try:
        with Conexion.cursor() as Cursor:
            sql_BorrarNombreFuncionario = "UPDATE FUNCIONARIO SET NOMBRE = '*' WHERE ID = %s"
            Cursor.execute(sql_BorrarNombreFuncionario, (ID,))
            Conexion.commit()
    except Exception as e:
        Conexion.rollback()
        raise e

    return redirect('/Funcionario')
    
@app.route('/Funcionario/BorrarSexoFuncionario/<int:ID>')
def BorrarSexoFuncionario(ID):
    Conexion = mysql.connection

    try:
        with Conexion.cursor() as Cursor:
            sql_BorrarSexoFuncionario = "UPDATE FUNCIONARIO SET SEXO = '*' WHERE ID = %s"
            Cursor.execute(sql_BorrarSexoFuncionario, (ID,))
            Conexion.commit()
    except Exception as e:
        Conexion.rollback()
        raise e

    return redirect('/Funcionario')

@app.route('/Funcionario/BorrarDireccion/<int:ID>')
def BorrarDireccion(ID):
    Conexion = mysql.connection

    try:
        with Conexion.cursor() as Cursor:
            sql_BorrarDireccion = "UPDATE FUNCIONARIO SET DIRECCION = '*' WHERE ID = %s"
            Cursor.execute(sql_BorrarDireccion, (ID,))
            Conexion.commit()
    except Exception as e:
        Conexion.rollback()
        raise e

    return redirect('/Funcionario')

@app.route('/Funcionario/BorrarTelefonoFuncionario/<int:ID>')
def BorrarTelefonoFuncionario(ID):
    Conexion = mysql.connection

    try:
        with Conexion.cursor() as Cursor:
            sql_BorrarTelefonoFuncionario = "UPDATE FUNCIONARIO SET TELEFONO = '*' WHERE ID = %s"
            Cursor.execute(sql_BorrarTelefonoFuncionario, (ID,))
            Conexion.commit()
    except Exception as e:
        Conexion.rollback()
        raise e

    return redirect('/Funcionario')

# Borrar Datos Contacto de Emergencia
@app.route('/Funcionario/BorrarNombreContacto/<int:ID>')
def BorrarNombreContacto(ID):
    Conexion = mysql.connection

    try:
        with Conexion.cursor() as Cursor:
            sql_BorrarNombreContacto = "UPDATE CONTACTO_EMERGENCIA SET NOMBRE = '*' WHERE ID_FUNCIONARIO = %s"
            Cursor.execute(sql_BorrarNombreContacto, (ID,))
            Conexion.commit()
    except Exception as e:
        Conexion.rollback()
        raise e

    return redirect('/Funcionario')

@app.route('/Funcionario/BorrarRelacion/<int:ID>')
def BorrarRelacion(ID):
    Conexion = mysql.connection

    try:
        with Conexion.cursor() as Cursor:
            sql_BorrarRelacion = "UPDATE CONTACTO_EMERGENCIA SET RELACION = '*' WHERE ID_FUNCIONARIO = %s"
            Cursor.execute(sql_BorrarRelacion, (ID,))
            Conexion.commit()
    except Exception as e:
        Conexion.rollback()
        raise e

    return redirect('/Funcionario')

@app.route('/Funcionario/BorrarTelefonoContacto/<int:ID>')
def BorrarTelefonoContacto(ID):
    Conexion = mysql.connection

    try:
        with Conexion.cursor() as Cursor:
            sql_BorrarTelefonoContacto = "UPDATE CONTACTO_EMERGENCIA SET TELEFONO = '*' WHERE ID_FUNCIONARIO = %s"
            Cursor.execute(sql_BorrarTelefonoContacto, (ID,))
            Conexion.commit()
    except Exception as e:
        Conexion.rollback()
        raise e

    return redirect('/Funcionario')

# Borrar Datos Carga Familiar
@app.route('/Funcionario/BorrarNombreCarga/<int:ID>')
def BorrarNombreCarga(ID):
    Conexion = mysql.connection

    try:
        with Conexion.cursor() as Cursor:
            sql_BorrarNombreCarga = "UPDATE CARGA_FAMILIAR SET NOMBRE = '*' WHERE ID_FUNCIONARIO = %s"
            Cursor.execute(sql_BorrarNombreCarga, (ID,))
            Conexion.commit()
    except Exception as e:
        Conexion.rollback()
        raise e

    return redirect('/Funcionario')

@app.route('/Funcionario/BorrarParentesco/<int:ID>')
def BorrarParentesco(ID):
    Conexion = mysql.connection

    try:
        with Conexion.cursor() as Cursor:
            sql_BorrarParentesco = "UPDATE CARGA_FAMILIAR SET PARENTESCO = '*' WHERE ID_FUNCIONARIO = %s"
            Cursor.execute(sql_BorrarParentesco, (ID,))
            Conexion.commit()
    except Exception as e:
        Conexion.rollback()
        raise e

    return redirect('/Funcionario')

@app.route('/Funcionario/BorrarSexoCarga/<int:ID>')
def BorrarSexoCarga(ID):
    Conexion = mysql.connection

    try:
        with Conexion.cursor() as Cursor:
            sql_BorrarSexoCarga = "UPDATE CARGA_FAMILIAR SET SEXO = '*' WHERE ID_FUNCIONARIO = %s"
            Cursor.execute(sql_BorrarSexoCarga, (ID,))
            Conexion.commit()
    except Exception as e:
        Conexion.rollback()
        raise e

    return redirect('/Funcionario')

@app.route('/Funcionario/BorrarRUTCarga/<int:ID>')
def BorrarRUTCarga(ID):
    Conexion = mysql.connection

    try:
        with Conexion.cursor() as Cursor:
            sql_BorrarRUTCarga = "UPDATE CARGA_FAMILIAR SET RUT = '*' WHERE ID_FUNCIONARIO = %s"
            Cursor.execute(sql_BorrarRUTCarga, (ID,))
            Conexion.commit()
    except Exception as e:
        Conexion.rollback()
        raise e

    return redirect('/Funcionario')

# Editar datos Funcionario
# Nombre de Funcionario
@app.route('/Funcionario/ActualizarNombreFuncionario/<int:ID>')
def ActualizarNombreFuncionario(ID):
    Conexion = mysql.connection
    sql_NombreFuncionario = "SELECT NOMBRE FROM FUNCIONARIO WHERE ID = %s"
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_NombreFuncionario, (ID,))
        Dato = Cursor.fetchone()

    return render_template('/Actualizar/FuncionarioNombre.html', Dato = Dato, ID = ID)

@app.route('/Funcionario/ActualizarNombreFuncionario1', methods=['POST'])
def ActualizarNombreFuncionario1():
    Nombre = request.form.get('NombreFuncionario')
    ID = int(request.form.get('ID'))
    sql_Actualizar = "UPDATE FUNCIONARIO SET NOMBRE = %s WHERE ID = %s"
    Datos = (Nombre, ID)

    Conexion = mysql.connection
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_Actualizar, Datos)
        Conexion.commit()
    
    return redirect('/Funcionario')

# Sexo de Funcionario
@app.route('/Funcionario/ActualizarSexoFuncionario/<int:ID>')
def ActualizarSexoFuncionario(ID):
    Conexion = mysql.connection
    sql_SexoFuncionario = "SELECT SEXO FROM FUNCIONARIO WHERE ID = %s"
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_SexoFuncionario, (ID,))
        Dato = Cursor.fetchone()

    return render_template('/Actualizar/FuncionarioSexo.html', Dato = Dato, ID = ID)

@app.route('/Funcionario/ActualizarSexoFuncionario1', methods=['POST'])
def ActualizarSexoFuncionario1():
    Sexo = request.form.get('SexoFuncionario')
    ID = int(request.form.get('ID'))
    sql_Actualizar = "UPDATE FUNCIONARIO SET SEXO = %s WHERE ID = %s"
    Datos = (Sexo, ID)

    Conexion = mysql.connection
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_Actualizar, Datos)
        Conexion.commit()
    
    return redirect('/Funcionario')

# Direccion de Funcionario
@app.route('/Funcionario/ActualizarDireccion/<int:ID>')
def ActualizarDireccion(ID):
    Conexion = mysql.connection
    sql_Direccion = "SELECT DIRECCION FROM FUNCIONARIO WHERE ID = %s"
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_Direccion, (ID,))
        Dato = Cursor.fetchone()
    
    return render_template('/Actualizar/Direccion.html', Dato = Dato, ID = ID)

@app.route('/Funcionario/ActualizarDireccion1', methods=['POST'])
def ActualizarDireccion1():
    Direccion = request.form.get('Direccion')
    ID = int(request.form.get('ID'))
    sql_Actualizar = "UPDATE FUNCIONARIO SET DIRECCION = %s WHERE ID = %s"
    Datos = (Direccion, ID)

    Conexion = mysql.connection
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_Actualizar, Datos)
        Conexion.commit()

    return redirect('/Funcionario')

# Telefono de Funcionario
@app.route('/Funcionario/ActualizarTelefonoFuncionario/<int:ID>')
def TelefonoFuncionario(ID):
    Conexion = mysql.connection
    sql_Telefono = "SELECT TELEFONO FROM FUNCIONARIO WHERE ID = %s"
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_Telefono, (ID,))
        Dato = Cursor.fetchone()
    
    return render_template('/Actualizar/TelefonoFuncionario.html', Dato = Dato, ID = ID)

@app.route('/Funcionario/ActualizarTelefonoFuncionario1', methods=['POST'])
def ActualizarTelefonoFuncionario1():
    Telefono = request.form.get('TelefonoFuncionario')
    ID = int(request.form.get('ID'))
    sql_Actualizar = "UPDATE FUNCIONARIO SET TELEFONO = %s WHERE ID = %s"
    Datos = (Telefono, ID)

    Conexion = mysql.connection
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_Actualizar, Datos)
        Conexion.commit()

    return redirect('/Funcionario')

# Nombre de Contacto
@app.route('/Funcionario/ActualizarNombreContacto/<int:ID>')
def ActualizarNombreContacto(ID):
    Conexion = mysql.connection
    sql_Contacto = "SELECT NOMBRE FROM CONTACTO_EMERGENCIA WHERE ID_FUNCIONARIO = %s"
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_Contacto, (ID,))
        Dato = Cursor.fetchone()

    return render_template('/Actualizar/NombreContacto.html', Dato = Dato, ID = ID)

@app.route('/Funcionario/ActualizarNombreContacto1', methods=['POST'])
def ActualizarNombreContacto1():
    Contacto = request.form.get('NombreContacto')
    ID = int(request.form.get('ID'))
    sql_Actualizar = "UPDATE CONTACTO_EMERGENCIA SET NOMBRE = %s WHERE ID_FUNCIONARIO = %s"
    Datos = (Contacto, ID)

    Conexion = mysql.connection
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_Actualizar, Datos)
        Conexion.commit()
    
    return redirect('/Funcionario')

# Relacion de Contacto
@app.route('/Funcionario/ActualizarRelacionContacto/<int:ID>')
def ActualizarRelacionContacto(ID):
    Conexion = mysql.connection
    sql_Relacion = "SELECT RELACION FROM CONTACTO_EMERGENCIA WHERE ID_FUNCIONARIO = %s"
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_Relacion, (ID,))
        Dato = Cursor.fetchone()

    return render_template('/Actualizar/RelacionContacto.html', Dato = Dato, ID = ID)

@app.route('/Funcionario/ActualizarRelacionContacto1', methods=['POST'])
def ActualizarRelacionContacto1():
    Relacion = request.form.get('Relacion')
    ID = int(request.form.get('ID'))
    sql_Actualizar = "UPDATE CONTACTO_EMERGENCIA SET RELACION = %s WHERE ID_FUNCIONARIO = %s"
    Datos = (Relacion, ID)

    Conexion = mysql.connection
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_Actualizar, Datos)
        Conexion.commit()
    
    return redirect('/Funcionario')

# Telefono de Contacto
@app.route('/Funcionario/ActualizarTelefonoContacto/<int:ID>')
def ActualizarTelefonoContacto(ID):
    Conexion = mysql.connection
    sql_TelefonoContacto = "SELECT TELEFONO FROM CONTACTO_EMERGENCIA WHERE ID_FUNCIONARIO = %s"  
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_TelefonoContacto, (ID,))
        Dato = Cursor.fetchone()

    return render_template('/Actualizar/TelefonoContacto.html', Dato=Dato, ID=ID)

@app.route('/Funcionario/ActualizarTelefonoContacto1', methods=['POST'])
def ActualizarTelefonoContacto1():
    TelefonoContacto = request.form.get('TelefonoContacto')
    ID = int(request.form.get('ID'))
    sql_Actualizar = "UPDATE CONTACTO_EMERGENCIA SET TELEFONO = %s WHERE ID_FUNCIONARIO = %s"  
    Datos = (TelefonoContacto, ID)

    Conexion = mysql.connection
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_Actualizar, Datos)
        Conexion.commit()
    
    return redirect('/Funcionario')

# Nombre de Carga Familiar
@app.route('/Funcionario/ActualizarNombreCarga/<int:ID>')
def ActualizarNombreCarga(ID):
    Conexion = mysql.connection
    sql_Carga = "SELECT NOMBRE FROM CARGA_FAMILIAR WHERE ID_FUNCIONARIO = %s"  
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_Carga, (ID,))
        Dato = Cursor.fetchone()

    return render_template('/Actualizar/NombreCarga.html', Dato=Dato, ID=ID)

@app.route('/Funcionario/ActualizarNombreCarga1', methods=['POST'])
def ActualizarNombreCarga1():
    Carga = request.form.get('NombreCarga')
    ID = int(request.form.get('ID'))
    sql_Actualizar = "UPDATE CARGA_FAMILIAR SET NOMBRE = %s WHERE ID_FUNCIONARIO = %s"  
    Datos = (Carga, ID)

    Conexion = mysql.connection
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_Actualizar, Datos)
        Conexion.commit()
    
    return redirect('/Funcionario')

# Parentesco de Carga Familiar
@app.route('/Funcionario/ActualizarParentesco/<int:ID>')
def ActualizarParentesco(ID):
    Conexion = mysql.connection
    sql_Parentesco = "SELECT PARENTESCO FROM CARGA_FAMILIAR WHERE ID_FUNCIONARIO = %s"  
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_Parentesco, (ID,))
        Dato = Cursor.fetchone()

    return render_template('/Actualizar/Parentesco.html', Dato=Dato, ID=ID)

@app.route('/Funcionario/ActualizarParentesco1', methods=['POST'])
def ActualizarParentesco1():
    Parentesco = request.form.get('Parentesco')
    ID = int(request.form.get('ID'))
    sql_Actualizar = "UPDATE CARGA_FAMILIAR SET PARENTESCO = %s WHERE ID_FUNCIONARIO = %s"  
    Datos = (Parentesco, ID)

    Conexion = mysql.connection
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_Actualizar, Datos)
        Conexion.commit()
    
    return redirect('/Funcionario')

# Sexo de Carga Familiar
@app.route('/Funcionario/ActualizarSexoCarga/<int:ID>')
def ActualizarSexoCarga(ID):
    Conexion = mysql.connection
    sql_SexoCarga = "SELECT SEXO FROM CARGA_FAMILIAR WHERE ID_FUNCIONARIO = %s"  
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_SexoCarga, (ID,))
        Dato = Cursor.fetchone()

    return render_template('/Actualizar/SexoCarga.html', Dato=Dato, ID=ID)

@app.route('/Funcionario/ActualizarSexoCarga1', methods=['POST'])
def ActualizarSexoCarga1():
    SexoCarga = request.form.get('SexoCarga')
    ID = int(request.form.get('ID'))
    sql_Actualizar = "UPDATE CARGA_FAMILIAR SET SEXO = %s WHERE ID_FUNCIONARIO = %s"  
    Datos = (SexoCarga, ID)

    Conexion = mysql.connection
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_Actualizar, Datos)
        Conexion.commit()
    
    return redirect('/Funcionario')

# RUT de Carga Familiar
@app.route('/Funcionario/ActualizarRUTCarga/<int:ID>')
def ActualizarRUTCarga(ID):
    Conexion = mysql.connection
    sql_RUTCarga = "SELECT RUT FROM CARGA_FAMILIAR WHERE ID_FUNCIONARIO = %s"  
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_RUTCarga, (ID,))
        Dato = Cursor.fetchone()

    return render_template('/Actualizar/RUTCarga.html', Dato=Dato, ID=ID)

@app.route('/Funcionario/ActualizarRUTCarga1', methods=['POST'])
def ActualizarRUTCarga1():
    RUTCarga = request.form.get('RUTCarga')
    ID = int(request.form.get('ID'))
    sql_Actualizar = "UPDATE CARGA_FAMILIAR SET RUT = %s WHERE ID_FUNCIONARIO = %s"  
    Datos = (RUTCarga, ID)

    Conexion = mysql.connection
    with Conexion.cursor() as Cursor:
        Cursor.execute(sql_Actualizar, Datos)
        Conexion.commit()
    
    return redirect('/Funcionario')

# FuncionarioRRHH
@app.route('/FuncionarioRRHH', methods=['GET', 'POST'])
def FuncionarioRRHH():
    if request.method == 'POST':
        # Recibir datos del formulario
        # USUARIOS
        Usuario = request.form.get('NombreUsuario')
        Contraseña = request.form.get('Contraseña')
        Rol = request.form.get('Rol')
        # FUNCIONARIO
        Funcionario = request.form.get('NombreFuncionario')
        RutFuncionario = request.form.get('RUTFuncionario')
        SexoFuncionario = request.form.get('SexoFuncionario')
        Direccion = request.form.get('Dirección')
        TelefonoFuncionario = request.form.get('TelefonoFuncionario')
        # DATOS_LABORALES
        Cargo = request.form.get('Cargo')
        FechaIngreso = request.form.get('FechaIngreso')
        Area = request.form.get('Area')
        Departamento = request.form.get('Departamento')
        # CONTACTO_EMERGENCIA
        Contacto = request.form.get('NombreContacto')
        Relacion = request.form.get('Relacion')
        TelefonoContacto = request.form.get('TelefonoContacto')
        # CARGA_FAMILIAR
        Carga = request.form.get('NombreCarga')
        Parentesco = request.form.get('Parentesco')
        SexoCarga = request.form.get('SexoCarga')
        RUTCarga = request.form.get('RUTCarga')

        # Validaciones
        if not all([Usuario, Contraseña, Rol, Funcionario, RutFuncionario, SexoFuncionario, Direccion, TelefonoFuncionario,
                    Cargo, FechaIngreso, Area, Departamento, Contacto, Relacion, TelefonoContacto, Carga, Parentesco, SexoCarga, RUTCarga]):
            return render_template('RRHHError.html')

        # Crear consultas para las respectivas inserciones
        sql_Usuario = "INSERT INTO USUARIOS(NOMBRE, CONTRASEÑA, ROL) VALUES (%s, %s, %s)"
        Tupla_Usuario = (Usuario, Contraseña, Rol)

        sql_Funcionario = "INSERT INTO FUNCIONARIO(RUT, NOMBRE, SEXO, DIRECCION, TELEFONO) VALUES (%s, %s, %s, %s, %s)"
        Tupla_Funcionario = (RutFuncionario, Funcionario, SexoFuncionario, Direccion, TelefonoFuncionario)

        sql_DatosLaborales = "INSERT INTO DATOS_LABORALES(CARGO, FECHA_INGRESO, AREA, DEPARTAMENTO) VALUES(%s, %s, %s, %s)"
        Tupla_DatosLaborales = (Cargo, FechaIngreso, Area, Departamento)

        sql_ContactoEmergencia = "INSERT INTO CONTACTO_EMERGENCIA(NOMBRE, RELACION, TELEFONO) VALUES(%s, %s, %s)"
        Tupla_ContactoEmergencia = (Contacto, Relacion, TelefonoContacto)

        sql_CargaFamiliar = "INSERT INTO CARGA_FAMILIAR(NOMBRE, PARENTESCO, SEXO, RUT) VALUES(%s, %s, %s, %s)"
        Tupla_CargaFamiliar = (Carga, Parentesco, SexoCarga, RUTCarga)

        

        Conexion = mysql.connection
        with Conexion.cursor() as Cursor:
            Cursor.execute(sql_Usuario, Tupla_Usuario)
            Cursor.execute(sql_Funcionario, Tupla_Funcionario)
            Cursor.execute(sql_DatosLaborales, Tupla_DatosLaborales)
            Cursor.execute(sql_ContactoEmergencia, Tupla_ContactoEmergencia)
            Cursor.execute(sql_CargaFamiliar, Tupla_CargaFamiliar)
            Conexion.commit()
        return render_template('FuncionarioRRHH.html')
    
    Conexion = mysql.connection
    sql_ListadoFuncionarios = """SELECT 
                FUNCIONARIO.RUT,
                FUNCIONARIO.NOMBRE,
                FUNCIONARIO.SEXO,
                DATOS_LABORALES.CARGO
            FROM 
                FUNCIONARIO
            INNER JOIN 
                DATOS_LABORALES ON FUNCIONARIO.ID = DATOS_LABORALES.ID_FUNCIONARIO;"""
    
    with Conexion.cursor() as Cursor:
            Cursor.execute(sql_ListadoFuncionarios)
            Listado = Cursor.fetchall()
    return render_template('FuncionarioRRHH.html', Listado = Listado)

# Funcion de login 
@app.route('/acceso-login', methods=['GET', 'POST'])
def Login():
    # Verificar si la petición (request) es de tipo POST y si el nombre y contraseña esté presentes en los datos enviados por el formulario
    if request.method == 'POST' and 'NombreUsuario' in request.form and 'ContraseñaUsuario':
        # Obtener el nombre y contraseña desde el formulario (Inicio.html)
        _Usuario = request.form['NombreUsuario'] 
        _Contraseña = request.form['ContraseñaUsuario']

        Conexion = mysql.connection
        Cursor = Conexion.cursor()

        Cursor.execute('SELECT * FROM USUARIOS WHERE NOMBRE = %s AND CONTRASEÑA = %s', (_Usuario, _Contraseña))
        # Obtiene la primera fila del resultado de la consulta
        Account = Cursor.fetchone()

        # Si encuentra un registro de la base de datos que coincida con el usuario y la contraseña ejecuta...
        if Account:
            # Establece la sesión como "Logueado" y guarda el id del usuario en la sesión
            session['Logueado'] = True
            session['ID'] = Account['ID']

            # Redirigir según el rol del usuario encontrado (Rol insertado en la base de datos)
            if Account['ROL'] == "JefeRRHH":
                return redirect("/JefeRRHH")
            elif Account['ROL'] == "Funcionario":
                return redirect("/Funcionario")
            elif Account['ROL'] == "FuncionarioRRHH":
                return redirect("/FuncionarioRRHH")
        # Si no encuentra un registro en la base de datos que coincida, renderiza Inicio.html nuevamente
        else:
            return render_template("Inicio.html")
        
    # Si la petición no es de tipo POST o falta alguno de los campos en el formulario, renderiza el template 'Inicio.html'
    return render_template('Inicio.html')


if __name__ == '__main__':
    app.secret_key = "IgnacioDB"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)