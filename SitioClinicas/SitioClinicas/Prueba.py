from flask import render_template, url_for, flash, redirect, request, abort, current_app, session
from SitioClinicas import app, mail
from SitioClinicas.Forms import registrarAdmin, registrarProfesor, registrarAlumno, registrarPaciente, consulta, consultaPacientes, LoginForm, RecuperarForm, CambiarForm, optometria, odontologia, fisioterapia
from flask_login import LoginManager, login_user, current_user, logout_user,login_required
from flask_principal import Principal, Identity, AnonymousIdentity, identity_changed, identity_loaded, RoleNeed, UserNeed, Permission
import mysql.connector
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import os
from datetime import date, datetime
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from models.ModelUser import ModelUser
from models.entities.User import User


# Configura los detalles de la conexión a la base de datos
#En caso de que cambien los datos, se deberan modificar
db_config = {
    'user': 'root',
    'password': '6patapollo',
    'host': 'localhost',
    'database': 'serviciosocial',
}

Principal(app)
login_manager_app = LoginManager(app)

#Función para manejar la sesión con el usuario 
@login_manager_app.user_loader
def load_user(id):
    conn = mysql.connector.connect(**db_config)
    return ModelUser.get_by_id(conn, id)

#Función niega la entrada a persona sin iniciar sesión
@login_manager_app.unauthorized_handler
def unauthorized():
    return redirect(url_for('hello_world'))

#Función para manejar la identidad del usario
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Asigna el objeto user a la identidad
    identity.user = current_user

    # Agrega el UserNeed a la identidad
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Se agrega el rol a la identidad
    if hasattr(current_user, 'rol'):
        identity.provides.add(RoleNeed(current_user.rol))

#Crea los permisos de acceso, la función Permission utiliza or
#por lo que si el rol es al menos uno de los indicados, se permitira el acceso
superAdmin_permission = Permission(RoleNeed('SuperAdmin'))
admin_permission = Permission(RoleNeed('SuperAdmin'), RoleNeed('Admin'))
profesor_permission = Permission(RoleNeed('SuperAdmin'), RoleNeed('Admin'), RoleNeed('Profesor'))

#Se crea la función que checa que haya información en el dato de "Proxima visita" en las tablas de optometría, fisioterapia y odontología
#En caso que falten 14 días, se mandará un correo con el id y nombre del paciente así como la fecha de la visita
def recordatorio():
    with app.app_context():

        #Recordatorio para optometria, hace un join con las tablas de optometría y usuario para obtener la información
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute("""SELECT opt.idPaciente, opt.proximaVisita, pac.nombrePaciente, pac.apellidoPaternoPaciente, pac.apellidoMaternoPaciente 
                 from optometria as opt left join paciente as pac on opt.idPaciente=pac.idPaciente WHERE opt.proximaVisita IS NOT NULL""")
        data = cur.fetchall()
        cur.close()
        conn.close()
        lista=[]
        newline="\n"

        #Se lee la información recabada y verifica que falten 14 días, en caso de que asi sea, el paciente se agrega a una lista
        for visita in data:
            today = date.today()
            new=datetime.strptime(visita[1],'%Y-%m-%d')
            difference=new.date()-today
            if difference.days==14:
                lista.append(visita)

        #Si la lista no esta vacia, se le da formato y se manda al correo pertinente
        #El "recipient" debera ser cambiado por el correo deseado, en el caso de optometría: programa.nomasdiabetes@enes.unam.mx 
        if lista:
            msg=Message('Recordatorio próximas citas Optometría', recipients=['adrimarvi10@hotmail.com'],sender='noreply@hotmail.com')
            msg.body=f'''Los siguientes pacientes tienen una visita el {lista[0][1]}:\n{newline.join(f'Id: {value[0]} Nombre: {value[2]} {value[3]} {value[4]}' for value in lista)}'''
                        
            mail.send(msg)
            print('Mensaje enviado')
        
        #Recordatorio para fisiterapia, hace un join con las tablas de fisioterapia y usuario para obtener la información
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute("""SELECT fis.idPaciente, fis.proximaVisita, pac.nombrePaciente, pac.apellidoPaternoPaciente, pac.apellidoMaternoPaciente 
                 from fisioterapia as fis left join paciente as pac on fis.idPaciente=pac.idPaciente WHERE fis.proximaVisita IS NOT NULL""")
        data = cur.fetchall()
        cur.close()
        conn.close()
        lista=[]
        newline="\n"

        #Se lee la información recabada y verifica que falten 14 días, en caso de que asi sea, el paciente se agrega a una lista
        for visita in data:
            today = date.today()
            new=datetime.strptime(visita[1],'%Y-%m-%d')
            difference=new.date()-today
            if difference.days==14:
                lista.append(visita)

        #Si la lista no esta vacia, se le da formato y se manda al correo pertinente
        #El "recipient" debera ser cambiado por el correo deseado 
        if lista:
            msg=Message('Recordatorio próximas citas Fisioterapia', recipients=['adrimarvi10@hotmail.com'],sender='noreply@hotmail.com')
            msg.body=f'''Los siguientes pacientes tienen una visita el {lista[0][1]}:\n{newline.join(f'Id: {value[0]} Nombre: {value[2]} {value[3]} {value[4]}' for value in lista)}'''
                        
            mail.send(msg)
            print('Mensaje enviado')

        #Recordatorio para odontologia, hace un join con las tablas de odontología y usuario para obtener la información
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute("""SELECT odo.idPaciente, odo.proximaVisita, pac.nombrePaciente, pac.apellidoPaternoPaciente, pac.apellidoMaternoPaciente 
                 from odontologia as odo left join paciente as pac on odo.idPaciente=pac.idPaciente WHERE odo.proximaVisita IS NOT NULL""")
        data = cur.fetchall()
        cur.close()
        conn.close()
        lista=[]
        newline="\n"

        #Se lee la información recabada y verifica que falten 14 días, en caso de que asi sea, el paciente se agrega a una lista
        for visita in data:
            today = date.today()
            new=datetime.strptime(visita[1],'%Y-%m-%d')
            difference=new.date()-today
            if difference.days==14:
                lista.append(visita)

        #Si la lista no esta vacia, se le da formato y se manda al correo pertinente
        #El "recipient" debera ser cambiado por el correo deseado 
        if lista:
            msg=Message('Recordatorio próximas citas Odontología', recipients=['adrimarvi10@hotmail.com'],sender='noreply@adrian.com')
            msg.body=f'''Los siguientes pacientes tienen una visita el {lista[0][1]}:\n{newline.join(f'Id: {value[0]} Nombre: {value[2]} {value[3]} {value[4]}' for value in lista)}'''
                        
            mail.send(msg)
            print('Mensaje enviado')



with app.app_context():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=recordatorio, trigger="cron", hour=12)
    scheduler.start()

# Apagar el scheduler cuando se sale de la app
atexit.register(lambda: scheduler.shutdown())

#Función que se realiza al acceder a la pagina principal http://127.0.0.1:5000/, es la página de inicio de sesión
@app.route("/",methods=['GET','POST'])
def hello_world():
    #Si el usuario ya tiene una sesión activa, se redirecciona a la página principal
    if current_user.is_authenticated:
        return redirect(url_for('inicio'))

    #Al ser la página de inicio de sesión, el form sera el de login
    form=LoginForm()

    #Si se hace un request, se crea un user con el username y contraseña ingresado y se utiliza la función ModelUser.Login 
    #Para buscar el username y si existe, comparar la contraseña ingresada con la guardada en la base de datos
    if form.validate_on_submit():
        user=User(0, username=form.username.data, password=form.password.data)
        conn = mysql.connector.connect(**db_config)
        logged_user = ModelUser.login(conn, user)

        #Si el usuario existe y las contraseñas coinciden, se inicia sesión y se crea la identidad
        if logged_user!=None:
            if logged_user.password:
                flash("Sesión iniciada",'success')        
                login_user(logged_user)
                identity_changed.send(current_app._get_current_object(), identity=Identity(logged_user.id))
                    
            else:
                #Si la contraseña es incorrecta, redirecciona a la misma página de inicio de sesión y se le indica al usuario
                flash("Contraseña inválida... ", 'danger')
                return render_template('login.html',form=form)
        else:
            #Si la usuario no se encuentra, redirecciona a la misma página de inicio de sesión y se le indica al usuario
            flash("No se encuentra el usuario... ", 'danger')
            return render_template('login.html', form=form)
        return redirect(url_for('inicio'))
    
    #Si no se envió ningún form, simplemente muestra la página de inicio de sesión
    return render_template('login.html', form=form)

#En la página de inicio, unicamente se muestra el template de Inicio.html
@app.route("/inicio")
@login_required
def inicio():
    return render_template('Inicio.html')

#En esta función registraremos admins, se requiere tener una sesión activa y tener el rol de SuperAdmin
@app.route("/registrarAdmin", methods=['GET','POST']) 
@login_required
@superAdmin_permission.require(http_exception=403)
def registerAdmin():
    #Se usará el form registrarAdmin
    form=registrarAdmin()

    #Si se hace un request, la contraseña se convierte en un hash por seguridad y se checa en la tabla usuario si el 
    #usuario o contraseña que se esta registrando, ya han estan guardados en la base de datos
    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.password.data)

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario where username='{}' or correo='{}' ".format(form.username.data, form.correo.data))
        data = cursor.fetchall()

        #Si no se encuentra información en la tabla usuario, se procede a guardar la información, luego, se busca
        #si el id o usuario estan en la tabla admin de la clinica correspondiente
        if not data:
            cursor.execute('INSERT INTO usuario (correo, username, contraseña, rol, clinica) VALUES (%s, %s, %s, %s, %s)', (form.correo.data, form.username.data, hashed_password, "Admin", form.clinica.data))
            
            cursor.execute("SELECT * FROM admin{} where idAdmin{}='{}' or usuarioAdmin{}='{}'".format(form.clinica.data, form.clinica.data, form.id.data, form.clinica.data, form.username.data))
            data = cursor.fetchall()

            #Si no se encuentra la información en la tabla admin de la clínica correspondiente, se procede a guardar la información
            #y se hace commit para confirmar el guardado de información en la base de datos
            if not data:
                cursor.execute('INSERT INTO admin{} VALUES (%s, %s, %s, %s, %s, %s)'.format(form.clinica.data), 
                              (form.id.data, form.nombre.data, form.username.data, hashed_password, None, None))
                conn.commit()
                flash('El admin fue creado con éxito!','success')

            #Si en algunos de los casos anteriores, el id, correo o username se encuentran ya 
            #registrados en la base de datos Se le pide al usuario que cambie el dato correspondiente, 
            #asi mismo se hace un rollback para que no se quede información guardada a medias
            else:
                if data[0][0]==form.id.data:
                    flash("Ingrese otro id","danger")
                else:
                    flash("Ingrese otro usuario","danger")
                conn.rollback()
                return render_template('registrarAdmin.html', form=form)
        
        else:
            if data[0][2]==form.username.data:
                flash("Ingrese otro usuario","danger")
            else:
                flash("Ingrese otro correo","danger")
            conn.rollback()
            return render_template('registrarAdmin.html', form=form)
            
        #Cerramos la conexión a la base de datos
        cursor.close()
        conn.close()

        #En caso de que el registro sea exitoso, se redirecciona a la página de inicio 
        return redirect(url_for('inicio'))

    #Si no se envió ningún form, simplemente muestra la página de registrarAdmin
    return render_template('registrarAdmin.html', form=form)

#En esta función registraremos profesores, se requiere tener una sesión activa y tener el rol de SuperAdmin o de Admin
@app.route("/registrarProfesor", methods=['GET','POST']) 
@login_required
@admin_permission.require(http_exception=403)
def registerProfesor():

    #Se usará el form registrarProfesor
    form=registrarProfesor()

    #Si se hace un request, la contraseña se convierte en un hash por seguridad y se checa en la tabla usuario si el 
    #usuario o contraseña que se esta registrando, ya han estan guardados en la base de datos
    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.password.data)

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario where username='{}' or correo='{}' ".format(form.username.data, form.correo.data))
        data = cursor.fetchall()

        #Si no se encuentra información en la tabla usuario, se procede a guardar la información, luego, se busca
        #si el rfc o usuario estan en la tabla profesor de la clinica correspondiente
        if not data:
            cursor.execute('INSERT INTO usuario (correo, username, contraseña, rol, clinica) VALUES (%s, %s, %s, %s, %s)', (form.correo.data, form.username.data, hashed_password, "Profesor", form.clinica.data))
            
            cursor.execute("SELECT * FROM profesor{} where rfcProfesor{}='{}' or usuarioProfesor{}='{}'".format(form.clinica.data, form.clinica.data, form.rfc.data, form.clinica.data, form.username.data))
            data = cursor.fetchall()

            #Si no se encuentra la información en la tabla profesor de la clínica correspondiente, se procede a guardar la información
            #y se hace commit para confirmar el guardado de información en la base de datos
            if not data:
                # Inserta el nuevo profesor en la base de datos (rfcProfesorOdontologia, nombreProfesorOdontologia, apellidosProfesorOdontologia, usuarioProfesorOdontologia, contraseñaProfesorOdontologia, idAdminOdontologia_FK)
                cursor.execute('INSERT INTO profesor{} VALUES (%s, %s, %s, %s, %s, %s, %s)'.format(form.clinica.data), 
                              (form.rfc.data, form.nombre.data, form.apellidos.data, form.username.data, hashed_password, None, None))
                conn.commit()
                flash('El profesor fue creado con éxito!','success')

            #Si en algunos de los casos anteriores, el rfc, correo o username se encuentran ya 
            #registrados en la base de datos, se le pide al usuario que cambie el dato correspondiente, 
            #asi mismo se hace un rollback para que no se quede información guardada a medias
            else:
                if data[0][0]==form.rfc.data:
                    flash("Ingrese otro RFC","danger")
                else:
                    flash("Ingrese otro usuario","danger")
                conn.rollback()
                return render_template('RegistrarProfesor.html', form=form)
        
        else:
            if data[0][2]==form.username.data:
                flash("Ingrese otro usuario","danger")
            else:
                flash("Ingrese otro correo","danger")
            conn.rollback()
            return render_template('RegistrarProfesor.html', form=form)

        #Se cierra la conexión a la base de datos
        cursor.close()
        conn.close()

        #En caso de que el registro sea exitoso, se redirecciona a la página de inicio 
        return redirect(url_for('inicio'))

    #Si no se envió ningún form, simplemente muestra la página de registrarProfesor
    return render_template('RegistrarProfesor.html', form=form)

#En esta función registraremos alumnos, se requiere tener una sesión activa y tener el rol de SuperAdmin, de Admin o de Profesor
@app.route("/registrarAlumno",  methods=['GET','POST']) 
@login_required
@profesor_permission.require(http_exception=403)
def registerAlumno():

    #Se usará el form registrarAlumno
    form=registrarAlumno()

    #Si se hace un request, la contraseña se convierte en un hash por seguridad y se checa en la tabla usuario si el 
    #usuario o contraseña que se esta registrando, ya han estan guardados en la base de datos
    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.password.data)

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuario where username='{}' or correo='{}' ".format(form.username.data, form.correo.data))
        data = cursor.fetchall()

        #Si no se encuentra información en la tabla usuario, se procede a guardar la información, luego, se busca
        #si el numero de cuenta o usuario estan en la tabla alumno de la clinica correspondiente
        if not data:
            cursor.execute('INSERT INTO usuario (correo, username, contraseña, rol, clinica) VALUES (%s, %s, %s, %s, %s)', (form.correo.data, form.username.data, hashed_password, "Alumno", form.clinica.data))
            
            cursor.execute("SELECT * FROM alumno{} where numeroCuentaAlumno{}='{}' or usuarioAlumno{}='{}'".format(form.clinica.data, form.clinica.data, form.numeroCuenta.data, form.clinica.data, form.username.data))
            data = cursor.fetchall()

            #Si no se encuentra la información en la tabla alumno de la clínica correspondiente, se procede a guardar la información
            #y se hace commit para confirmar el guardado de información en la base de datos
            if not data:
                # Inserta el nuevo alumno en la base de datos (numeroCuentaAlumnoOdontologia, nombreAlumnoOdontologia, apellidosAlumnoOdontologia, año, asignaturaAlumnoOdontologia, usuarioAlumnoOdontologia, contraseñaAlumnoOdontologia, rfcProfesorOdontologia_FK)
                cursor.execute('INSERT INTO alumno{} VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'.format(form.clinica.data), 
                              (form.numeroCuenta.data, form.nombre.data, form.apellidos.data, form.año.data, form.asignatura.data, form.username.data, hashed_password, None, None))
                conn.commit()
                flash('El alumno fue registrado con éxito!','success')

            #Si en algunos de los casos anteriores, el numero de cuenta, correo o username se encuentran ya 
            #registrados en la base de datos, se le pide al usuario que cambie el dato correspondiente, 
            #asi mismo se hace un rollback para que no se quede información guardada a medias
            else:
                if data[0][0]==form.numeroCuenta.data:
                    flash("Ingrese otro número de cuenta","danger")
                else:
                    flash("Ingrese otro usuario","danger")
                conn.rollback()
                return render_template('registrarAlumno.html', form=form)
        
        else:
            if data[0][2]==form.username.data:
                flash("Ingrese otro usuario","danger")
            else:
                flash("Ingrese otro correo","danger")
            conn.rollback()
            return render_template('registrarAlumno.html', form=form)

        # Cierra la conexión a la base de datos
        cursor.close()
        conn.close()

        #En caso de que el registro sea exitoso, se redirecciona a la página de inicio
        return redirect(url_for('inicio'))

    #Si no se envió ningún form, simplemente muestra la página de registrarAlumno
    return render_template('registrarAlumno.html', form=form)

#En esta función registraremos pacientes, se requiere tener una sesión activa
@app.route("/registrarPaciente", methods=['GET','POST'])
@login_required
def registerPaciente():

    #Se usará el form registrarPaciente
    form=registrarPaciente()

    #Si se hace un request, se checa si el id o el rfc del paciente ya han estan guardados en la base de datos
    if form.validate_on_submit():

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM paciente where idPaciente='{}' or rfcPaciente='{}' ".format(form.id.data, form.rfc.data))
        data = cursor.fetchall()

        #Si no se encuentra información en la tabla paciente, se procede a guardar la información
        if not data:
            # Inserta el nuevo paciente en la base de datos
            cursor.execute("""INSERT INTO paciente (idPaciente, rfcPaciente, fechaRemision, fechaAtención, sexo, edad, nombrePaciente, apellidoPaternoPaciente, apellidoMaternoPaciente, fechaNacimiento, edadAños, edadMeses, telefonoCasa, 
                           extensionTelefono, telefonoOficina, celular, email, calle, numeroExterior, numeroInterior, colonia, ciudad, codigoPostal, estado, pais, origen, estadoCivil, ocupacion, nacionalidad, tipoSangre, clasificacion, 
                           alertaAdministrativa, numeroSeguro, nombreContactoEmergencia, telefonoContactoEmergencia, coberturaMedica, relacionContactoPaciente, idAdminOdontologia_FK, idAdminFisioterapia_FK, idAdminOptometria_FK, numeroCuentaAlumnoOdontologia_FK, 
                           numeroCuentaAlumnoFisioterapia_FK, numeroCuentaAlumnoOptometria_FK) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                           (form.id.data, form.rfc.data, form.fechaRemision.data, form.fechaAtención.data, form.sexo.data, form.edad.data, form.nombre.data, form.apellidoPaterno.data, form.apellidoMaterno.data, form.fechaNacimiento.data,
                           form.edadAños.data, form.edadMeses.data, form.telefonoCasa.data, form.extensionTelefono.data, form.telefonoOficina.data, form.celular.data, form.email.data, form.calle.data, form.numeroExterior.data, form.numeroInterior.data, 
                           form.colonia.data, form.ciudad.data, form.codigoPostal.data, form.estado.data, form.pais.data, form.origen.data, form.estadoCivil.data, form.ocupacion.data, form.nacionalidad.data, form.tipoSangre.data, form.clasificacion.data,
                           form.alertaAdministrativa.data, form.numeroSeguro.data, form.nombreContactoEmergencia.data, form.telefonoContactoEmergencia.data, form.coberturaMedica.data, form.relacionContactoPaciente.data, None, None, None, None, None, None,))
            
            #En el caso de pacientes, tambien debemos crear su espacio corrrespondiente en las clinicas
            #por lo que guardamos la información en las clinicas con su id y el resto de valores None
            #Una vez que se obtenga la información de las clinicas de odontología y fisioterapia, 
            #se deberam actualizar estos datos
            cursor.execute("""INSERT INTO optometria(idPaciente,octDiscoOptico,octMacular,octMacularCube,octA,anguloIridocorneal,retinografiaPosiciones,retinografiaCentral,ergBasal,ergPhNR,ergRD,ergFlickerThenFlash,
                            contrastSensitivity,tonometria,campimetriaFast,topografia,estudiosClinicos,OSDI,BUT,schirmer,pesoCorporal,estatura,circunferenciaCintura,IMC,genero,edad,paquimetria,glucosa,presiónArterial,diagnosticoOcular,tratamientos,seguimiento,proximaVisita, idPaciente_FK) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                           (form.id.data, None, None, None, None, None, None,None, None, None, None, None, None,None, None, None, None, None, None,None, None, None, None, None, None,None, None, None, None, None, None, None, None, form.id.data))
            cursor.execute("""INSERT INTO odontologia(idPaciente,octDiscoOptico,octMacular,octMacularCube,octA,anguloIridocorneal,proximaVisita,idPaciente_FK) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
                           (form.id.data, None, None, None, None, None, None, form.id.data))
            cursor.execute("""INSERT INTO fisioterapia(idPaciente,octDiscoOptico,octMacular,octMacularCube,octA,anguloIridocorneal,proximaVisita,idPaciente_FK) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
                           (form.id.data, None, None, None, None, None, None, form.id.data))

            #Se hace commit para guardar la información
            conn.commit()

            #Para el siguiente paso se crearan las carpetas que contendrán los archivos de cada paciente en esl servidor, primero se guarda como variable
            #el id del paciente, se selecciona el form de la clínica correspondiente y se hace una iteración de los campos del form
            #buscando aquellos que sean de tipo "FileField". Cuando se encuentra uno, se crea la carpeta con el formato
            #SitioClinicas/static/Archivos/idPaciente/Clínica/Nombre del campo, el proceso se repite para las 3 clínicas
            idPac=form.id.data
            form=optometria()
            for field in form:
                if field.type == 'FileField':
                    if not os.path.exists(os.path.join("SitioClinicas/static/Archivos", idPac, "Optometria", field.name)): 
                        os.makedirs(os.path.join("SitioClinicas/static/Archivos", idPac, "Optometria", field.name))

            form=odontologia()
            for field in form:     
                if field.type == 'FileField': 
                    if not os.path.exists(os.path.join("SitioClinicas/static/Archivos", idPac, "Odontologia", field.name)): 
                        os.makedirs(os.path.join("SitioClinicas/static/Archivos", idPac, "Odontologia", field.name))

            form=fisioterapia()
            for field in form:
                if field.type == 'FileField':
                    if not os.path.exists(os.path.join("SitioClinicas/static/Archivos", idPac, "Fisioterapia", field.name)): 
                        os.makedirs(os.path.join("SitioClinicas/static/Archivos", idPac, "Fisioterapia", field.name))
            flash('El paciente fue registrado con éxito!','success')
    
        #Si el id o rfc del paciente se encuentran ya registrados en la base de datos, 
        #se le pide al usuario que cambie el dato correspondiente, 
        #asi mismo se hace un rollback para que no se quede información guardada a medias 
        else:
            if data[0][0]==form.id.data:
                flash("Ingrese otro id","danger")
            else:
                flash("Ingrese otro RFC","danger")
            conn.rollback()
            return render_template('registrarPaciente.html', form=form)

        # Cierra la conexión a la base de datos
        cursor.close()
        conn.close()

        #En caso de que el registro sea exitoso, se redirecciona a la página de inicio   
        return redirect(url_for('inicio'))

    #Si no se envió ningún form, simplemente muestra la página de resgistrarPaciente
    return render_template('registrarPaciente.html', form=form)

#En esta función consultaremos al personal, se requiere tener una sesión activa
@app.route("/consultas", methods=['GET','POST'])
@login_required
def consultas():
    #Se utiliza el form consulta
    form=consulta()

    #Al hacer un request, nos conectamos a la base de datos y dependiendo del tipo de personal que busquemos, haremos una busqueda en
    #la tabla correspondiente con un join
    if form.validate_on_submit():

        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        if form.personal.data=="admin":
            cur.execute("""SELECT per.id{}{}, per.nombre{}{}, per.usuario{}{}, us.correo from {}{} as per left join usuario as us on per.usuario{}{}=us.username""".format(form.personal.data, form.clinica.data,form.personal.data, form.clinica.data,form.personal.data, form.clinica.data,form.personal.data, form.clinica.data,form.personal.data, form.clinica.data))

        elif form.personal.data=="profesor":
            cur.execute("""SELECT per.rfc{}{}, per.nombre{}{}, per.usuario{}{}, us.correo from {}{} as per left join usuario as us on per.usuario{}{}=us.username""".format(form.personal.data, form.clinica.data,form.personal.data, form.clinica.data,form.personal.data, form.clinica.data,form.personal.data, form.clinica.data,form.personal.data, form.clinica.data))

        elif form.personal.data=="alumno":
            cur.execute("""SELECT per.numeroCuenta{}{}, per.nombre{}{}, per.usuario{}{}, us.correo from {}{} as per left join usuario as us on per.usuario{}{}=us.username""".format(form.personal.data, form.clinica.data,form.personal.data, form.clinica.data,form.personal.data, form.clinica.data,form.personal.data, form.clinica.data,form.personal.data, form.clinica.data))

        data = cur.fetchall()
        cur.close()
        conn.close()

        #Obtenemos los nombres de las columnas de la tabla y combinamos los nombres de las columnas con los datos
        column_names = [i[0] for i in cur.description]
        data_with_columns = [dict(zip(column_names, row)) for row in data]

        #Se mostrarán los resultados usando los parametros de data_with_columns, personal, clinica y rol
        return render_template('Consultas.html', data_with_columns=data_with_columns, form=form, personal=form.personal.data, clinica=form.clinica.data, rol=current_user.rol)
    return render_template('Consultas.html', form=form)

#En esta función consultaremos a los pacientes, se requiere tener una sesión activa
@app.route("/consultasPacientes", methods=['GET','POST'])
@login_required
def Pacientes():
    form=consultaPacientes()

    #En este caso tenemos 2 botones, uno para buscar por id y otro para buscar por nombre
    #Busqueda a traves de id
    if 'submitIdPaciente' in request.form:
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute("SELECT idPaciente, nombrePaciente FROM serviciosocial.paciente where idPaciente='{}'".format(form.idPaciente.data))
        data = cur.fetchall()
        cur.close()
        conn.close()

        column_names = [i[0] for i in cur.description]
        data_with_columns = [dict(zip(column_names, row)) for row in data]

        return render_template('ConsultasPacientes.html', data_with_columns=data_with_columns, form=form, )

    #Busqueda a traves del nombre
    elif 'submitNombrePaciente' in request.form:
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute("SELECT idPaciente, nombrePaciente FROM serviciosocial.paciente where nombrePaciente='{}'".format(form.nombrePaciente.data))
        data = cur.fetchall()
        cur.close()
        conn.close()

        column_names = [i[0] for i in cur.description]
        data_with_columns = [dict(zip(column_names, row)) for row in data]

        return render_template('ConsultasPacientes.html', data_with_columns=data_with_columns, form=form)
        
    return render_template('ConsultasPacientes.html', form=form)

#Esta función permite realizar modificaciones a mi perfil
@app.route("/perfil", methods=['GET','POST'])
@login_required
def perfiles():

    #Dependiendo del rol que tengamos, se asignará el form
    if current_user.rol=="Admin":
        form=registrarAdmin()
        
    elif current_user.rol=="Profesor":
        form=registrarProfesor()   

    elif current_user.rol=="Alumno":
        form=registrarAlumno()

    #Se eliminan del form el campo de password y confirm_password para evitar la validacipon obligatoria de estos
    #Se podrán cambiar en otro lugar
    del form.password
    del form.confirm_password

    #Al realizar un request, se guardan los cambios en las tablas correspondientes dependiendo del rol que tengamos
    if form.validate_on_submit():
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        if current_user.rol=="Admin":
            cur.execute("UPDATE admin{} set idAdmin{}='{}', nombreAdmin{}='{}', usuarioAdmin{}='{}'  where usuarioAdmin{}='{}' "
                .format(current_user.clinica, current_user.clinica, form.id.data, current_user.clinica, form.nombre.data, current_user.clinica, form.username.data, current_user.clinica, current_user.username))
            cur.execute("UPDATE usuario set username='{}', correo='{}'  where username='{}' "
                .format(form.username.data, form.correo.data, current_user.username))

        elif current_user.rol=="Profesor":
            cur.execute("""UPDATE profesor{} SET rfcProfesor{}='{}', nombreProfesor{}='{}', apellidosProfesor{}='{}', usuarioProfesor{}='{}' where usuarioProfesor{}='{}'"""
                .format(current_user.clinica, current_user.clinica, form.rfc.data, current_user.clinica, form.nombre.data, current_user.clinica, form.apellidos.data, current_user.clinica, form.username.data, current_user.clinica, current_user.username))
            cur.execute("UPDATE usuario set username='{}', correo='{}'  where username='{}' "
                .format(form.username.data, form.correo.data, current_user.username))

        elif current_user.rol=="Alumno":
            cur.execute("""UPDATE alumno{} SET numeroCuentaAlumno{}='{}', nombreAlumno{}='{}', apellidosAlumno{}='{}', año='{}', asignaturaAlumno{}='{}', usuarioAlumno{}='{}' where usuarioAlumno{}='{}'"""
                .format(current_user.clinica, current_user.clinica, form.numeroCuenta.data, current_user.clinica, form.nombre.data, current_user.clinica, form.apellidos.data, form.año.data, current_user.clinica, form.asignatura.data, current_user.clinica, form.username.data, current_user.clinica, current_user.username))
            cur.execute("UPDATE usuario set username='{}', correo='{}'  where username='{}' "
                .format(form.username.data, form.correo.data, current_user.username))

        conn.commit()  
        cur.close()
        conn.close()
        flash("Información guardada", "success")
        #Se hace el commit, se cierra la conexión y se redirecciona a la página de inicio
        return redirect(url_for('inicio'))

    #Al ser una página donde se muestra información, esta debe de ser buscada al momento de cargar la página
    #Igual que antes, la busqueda se realiza dependiendo del rol que tengamos 
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    if current_user.rol=="Admin":
        form=registrarAdmin(clinica=current_user.clinica)
        cur.execute("""SELECT adm.idAdmin{}, adm.nombreAdmin{}, adm.usuarioAdmin{}, us.correo from admin{} as adm left join usuario as us on adm.usuarioAdmin{}=us.username where adm.usuarioAdmin{}='{}'"""
            .format(current_user.clinica, current_user.clinica, current_user.clinica, current_user.clinica, current_user.clinica, current_user.clinica, current_user.username))
        
    elif current_user.rol=="Profesor":
        form=registrarProfesor(clinica=current_user.clinica)
        cur.execute("""SELECT prof.rfcProfesor{}, prof.nombreProfesor{}, prof.apellidosProfesor{}, prof.usuarioProfesor{}, us.correo from profesor{} as prof left join usuario as us on prof.usuarioProfesor{}=us.username where prof.usuarioProfesor{}='{}'"""
            .format(current_user.clinica, current_user.clinica, current_user.clinica, current_user.clinica, current_user.clinica, current_user.clinica, current_user.clinica, current_user.username))
        

    elif current_user.rol=="Alumno":
        form=registrarAlumno(clinica=current_user.clinica)
        cur.execute("""SELECT alum.numeroCuentaAlumno{}, alum.nombreAlumno{}, alum.apellidosAlumno{}, alum.año, alum.asignaturaAlumno{}, alum.usuarioAlumno{}, us.correo from alumno{} as alum left join usuario as us on alum.usuarioAlumno{}=us.username where alum.usuarioAlumno{}='{}'"""
            .format(current_user.clinica, current_user.clinica, current_user.clinica, current_user.clinica, current_user.clinica, current_user.clinica, current_user.clinica, current_user.clinica, current_user.username))

    data = cur.fetchall()
    cur.close()
    conn.close()
    
    #Se muestran los resultados con datos y rol como parametros
    return render_template('infoPerfil.html', data=data, form=form, rol=current_user.rol)

#En esta función podemos cambir la contraseña, se requiere una sesión activa
@app.route("/perfil/cambiarContraseña", methods=['GET','POST'])
@login_required
def cambiarContraseña():
    form=CambiarForm()

    #Al recibir un request, la contraseña se convierte en un hash y se guarda en l base de datos
    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.password.data)

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("UPDATE usuario set contraseña='{}' where id='{}' ".format(hashed_password, current_user.id))
        conn.commit()

        # Cierra la conexión a la base de datos
        cursor.close()
        conn.close()
        flash('La contraseña ha sido cambiada', 'success')
        return redirect(url_for('inicio'))
    return render_template('cambiarContraseña.html', form=form)


#En esta función podemos ver la información de los pacientes, se requiere una sesión activa
#Al presionar el botón de "consulta" en la página de consulta de pacientes, nos redirecciona a esta página
#Toamando el id del paciente como parametro 
@app.route("/paciente/<id>", methods=['GET','POST'])
@login_required
def infoPaciente(id):
    #Utilizamos el id del paciente como variable
    idPac=id
    form=registrarPaciente()

    #Al hacer un request, podemos actualizar la información del paciente 
    if form.validate_on_submit():
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute("""UPDATE paciente SET fechaRemision='{}', fechaAtención='{}', sexo='{}', edad='{}', nombrePaciente='{}', apellidoPaternoPaciente='{}', apellidoMaternoPaciente='{}', fechaNacimiento='{}', edadAños='{}', edadMeses='{}', telefonoCasa='{}', 
                       extensionTelefono='{}', telefonoOficina='{}', celular='{}', email='{}', calle='{}', numeroExterior='{}', numeroInterior='{}', colonia='{}', ciudad='{}', codigoPostal='{}', estado='{}', pais='{}', origen='{}', estadoCivil='{}', ocupacion='{}', 
                       nacionalidad='{}', tipoSangre='{}', clasificacion='{}', alertaAdministrativa='{}', numeroSeguro='{}', nombreContactoEmergencia='{}', telefonoContactoEmergencia='{}', coberturaMedica='{}', relacionContactoPaciente='{}' WHERE idPaciente='{}'""".format 
                       (form.fechaRemision.data, form.fechaAtención.data, form.sexo.data, form.edad.data, form.nombre.data, form.apellidoPaterno.data, form.apellidoMaterno.data, form.fechaNacimiento.data,form.edadAños.data, form.edadMeses.data, 
                       form.telefonoCasa.data, form.extensionTelefono.data, form.telefonoOficina.data, form.celular.data, form.email.data, form.calle.data, form.numeroExterior.data, form.numeroInterior.data, form.colonia.data, form.ciudad.data, 
                       form.codigoPostal.data, form.estado.data, form.pais.data, form.origen.data, form.estadoCivil.data, form.ocupacion.data, form.nacionalidad.data, form.tipoSangre.data, form.clasificacion.data,
                       form.alertaAdministrativa.data, form.numeroSeguro.data, form.nombreContactoEmergencia.data, form.telefonoContactoEmergencia.data, form.coberturaMedica.data, form.relacionContactoPaciente.data, form.id.data))
        conn.commit()
        flash('Las modificaciones fueron realizadas con éxito!','success')

        # Cierra la conexión a la base de datos
        cur.close()
        conn.close()

    #Al cargar la página queremos mostrar la información del paciente,
    #por lo que hacemos una busqueda de la información del paciente mediante su id
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("SELECT * FROM serviciosocial.paciente where idPaciente='{}'".format(idPac))
    data = cur.fetchall()
    cur.close()
    conn.close()

    #Debido a que estamos usando Flask Form, los campos de tipo "SelectField" deben definirse al seleccionar el form
    form=registrarPaciente(sexo=data[0][4], estado=data[0][23], pais=data[0][24], estadoCivil=data[0][26], ocupacion=data[0][27], tipoSangre=data[0][29], coberturaMedica=data[0][35], relacionContactoPaciente=data[0][36])
    return render_template('infoPaciente.html', data=data, idPac=idPac, form=form)

#En esta función podemos ver la información del paciente de la clinica de odontología
@app.route("/paciente/<id>/odontologia", methods=['GET','POST'])
@login_required
def infoOdontologia(id):
    idPac=id
    form=odontologia()

    #Al recibir un request, debemos guardar los archivos en las carpetas previamente creadas
    #Iteramos los campos del form buscando los que sean de tipo "FileField" y si el campo tiene un archivo,
    #se procede a guardarlo en su carpeta correspedondiente con el formato:
    #SitioClinicas/static/Archivos/idPaciente/Clínica/Nombre del campo/Nombre del archivo
    if form.validate_on_submit():
        for field in form:
            if field.type == 'FileField':
                f = field.data
                if f != None: 
                    filename = secure_filename(f.filename) 
                    f.save(os.path.join("SitioClinicas/static/Archivos", idPac, "Odontologia", field.name, filename))

        #Posteriormente se guarda la información en la base datos, en el caso de la clínica de odontología, se deberan actualizar estos
        #datos al recibir la información de parte de la clínica
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("""UPDATE odontologia Set octDiscoOptico=CONCAT("SitioClinicas/static/Archivos/",'{}','/Odontologia/octDiscoOptico'), octMacular=CONCAT("SitioClinicas/static/Archivos/",'{}','/Odontologia/octMacular'), octMacularCube=CONCAT("SitioClinicas/static/Archivos/",'{}','/Odontologia/octMacularCube'), octA=CONCAT("SitioClinicas/static/Archivos/",'{}','/Odontologia/octA'), 
                        anguloIridocorneal=CONCAT("SitioClinicas/static/Archivos/",'{}','/Odontologia/anguloIridocorneal'), proximaVisita='{}' Where idPaciente='{}' """
                        .format(idPac, idPac, idPac, idPac, idPac, form.proximaVisita.data, idPac))     
        conn.commit()
        cursor.close()
        conn.close()
        flash('Información guardada','success')

    #Al cargar la página queremos mostrar la información del paciente,
    #por lo que hacemos una busqueda de la información del paciente mediante su id
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("SELECT * FROM serviciosocial.odontologia where idPaciente='{}'".format(idPac))
    data = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('odontologia.html', form=form, idPac=idPac, data=data)

#En esta función podemos visualizar los archivos guardados del paciente de la clínica de odontología
@app.route("/paciente/<id>/odontologia/archivos", methods=['GET','POST'])
@login_required
def archivosOdontologia(id):
    form=odontologia()
    idPac=id

    #Tomamos como variable la primera parte fija de la ruta donde se encuentran los archivos
    #Primero iteramos los campos del form, después iteramos las carpetas del paciente en la clínica
    #Si el nombre de la carpeta y el nombre el campo coinciden, se agregan a una lista 
    #el nombre de la carpeta, el label del campo y los archivos dentro de las carpetas
    dir_path = "SitioClinicas/static/Archivos"
    res = []

    for field in form:
        for path in os.listdir(os.path.join(dir_path, idPac, "Odontologia")):#Viendo el nombre de las carpetas 
            if field.name==path:
                res2=[path, field.label, os.listdir(os.path.join(dir_path, idPac, "Odontologia", path))]
                res.append(res2)

    #Se muestra el template correspondiente tomando como parametros el id del paciente y la lista antes mencionada
    return render_template('archivosOdontologia.html', idPac=idPac, res=res)

#En esta función podemos ver la información del paciente de la clinica de odontología
@app.route("/paciente/<id>/fisioterapia", methods=['GET','POST'])
@login_required
def infoFisioterapia(id):
    idPac=id
    form=fisioterapia()

    #Al recibir un request, debemos guardar los archivos en las carpetas previamente creadas
    #Iteramos los campos del form buscando los que sean de tipo "FileField" y si el campo tiene un archivo,
    #se procede a guardarlo en su carpeta correspedondiente con el formato:
    #SitioClinicas/static/Archivos/idPaciente/Clínica/Nombre del campo/Nombre del archivo
    if form.validate_on_submit():
        for field in form:
            if field.type == 'FileField':
                f = field.data
                if f != None: 
                    filename = secure_filename(f.filename) 
                    f.save(os.path.join("SitioClinicas/static/Archivos", idPac, "Fisioterapia", field.name, filename))

        #Posteriormente se guarda la información en la base datos, en el caso de la clínica de fisioterapia, se deberan actualizar estos
        #datos al recibir la información de parte de la clínica         
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        
        cursor.execute("""UPDATE fisioterapia Set octDiscoOptico=CONCAT("SitioClinicas/static/Archivos/",'{}','/Fisiotreapia/octDiscoOptico'), octMacular=CONCAT("SitioClinicas/static/Archivos/",'{}','/Fisiotreapia/octMacular'), octMacularCube=CONCAT("SitioClinicas/static/Archivos/",'{}','/Fisiotreapia/octMacularCube'), octA=CONCAT("SitioClinicas/static/Archivos/",'{}','/Fisiotreapia/octA'), 
                        anguloIridocorneal=CONCAT("SitioClinicas/static/Archivos/",'{}','/Fisiotreapia/anguloIridocorneal'), proximaVisita='{}' Where idPaciente='{}' """
                        .format(idPac, idPac, idPac, idPac, idPac, form.proximaVisita.data, idPac))     
        conn.commit()
        cursor.close()
        conn.close()
        flash('Información guardada','success')

   
    #Al cargar la página queremos mostrar la información del paciente,
    #por lo que hacemos una busqueda de la información del paciente mediante su id
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("SELECT * FROM serviciosocial.fisioterapia where idPaciente='{}'".format(idPac))
    data = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('fisioterapia.html', form=form, idPac=idPac, data=data)

#En esta función podemos visualizar los archivos guardados del paciente de la clínica de fisioterapia
@app.route("/paciente/<id>/fisioterapia/archivos", methods=['GET','POST'])
@login_required
def archivosFisioterapia(id):
    form=fisioterapia()
    idPac=id

    #Tomamos como variable la primera parte fija de la ruta donde se encuentran los archivos
    #Primero iteramos los campos del form, después iteramos las carpetas del paciente en la clínica
    #Si el nombre de la carpeta y el nombre el campo coinciden, se agregan a una lista 
    #el nombre de la carpeta, el label del campo y los archivos dentro de las carpetas
    dir_path = "SitioClinicas/static/Archivos"
    res = []

    for field in form:
        for path in os.listdir(os.path.join(dir_path, idPac, "Fisioterapia")):#Viendo el nombre de las carpetas 
            if field.name==path:
                res2=[path, field.label, os.listdir(os.path.join(dir_path, idPac, "Fisioterapia", path))]
                res.append(res2)


    #Se muestra el template correspondiente tomando como parametros el id del paciente y la lista antes mencionada
    return render_template('archivosFisioterapia.html', idPac=idPac, res=res)

#En esta función podemos ver la información del paciente de la clinica de optometría
@app.route("/paciente/<id>/optometria", methods=['GET','POST'])
@login_required
def infoOptometria(id):
    form=optometria()
    idPac=id

    #Al recibir un request, debemos guardar los archivos en las carpetas previamente creadas
    #Iteramos los campos del form buscando los que sean de tipo "FileField" y si el campo tiene un archivo,
    #se procede a guardarlo en su carpeta correspedondiente con el formato:
    #SitioClinicas/static/Archivos/idPaciente/Clínica/Nombre del campo/Nombre del archivo
    if form.validate_on_submit():
        for field in form:
            if field.type == 'FileField':
                f = field.data
                if f != None: 
                    filename = secure_filename(f.filename) 
                    f.save(os.path.join("SitioClinicas/static/Archivos", idPac, "Optometria", field.name, filename))
            
        #Posteriormente se guarda la información en la base datos, en el caso de la clínica de optometría
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("""UPDATE optometria Set octDiscoOptico=CONCAT("SitioClinicas/static/Archivos/",'{}','/Optometria/octDiscoOptico'), octMacular=CONCAT("SitioClinicas/static/Archivos/",'{}','/Optometria/octMacular'), octMacularCube=CONCAT("SitioClinicas/static/Archivos/",'{}','/Optometria/octMacularCube'), octA=CONCAT("SitioClinicas/static/Archivos/",'{}','/Optometria/octA'), 
                        anguloIridocorneal=CONCAT("SitioClinicas/static/Archivos/",'{}','/Optometria/anguloIridocorneal'), retinografiaPosiciones=CONCAT("SitioClinicas/static/Archivos/",'{}','/Optometria/retinografiaPosiciones'), retinografiaCentral=CONCAT("SitioClinicas/static/Archivos/",'{}','/Optometria/retinografiaCentral'), ergBasal=CONCAT("SitioClinicas/static/Archivos/",'{}','/Optometria/ergBasal'), 
                        ergPhNR=CONCAT("SitioClinicas/static/Archivos/",'{}','/Optometria/ergPhNR'), ergRD=CONCAT("SitioClinicas/static/Archivos/",'{}','/Optometria/ergRD'), ergFlickerThenFlash=CONCAT("SitioClinicas/static/Archivos/",'{}','/Optometria/ergFlickerThenFlash'), contrastSensitivity='{}', tonometria='{}', campimetriaFast=CONCAT("SitioClinicas/static/Archivos/",'{}',+'/Optometria/campimetriaFast'),
                        topografia=CONCAT("SitioClinicas/static/Archivos/",'{}','/Optometria/topografia'), estudiosClinicos=CONCAT("SitioClinicas/static/Archivos/",'{}','/Optometria/estudiosClinicos'), OSDI='{}', BUT='{}', schirmer='{}', pesoCorporal='{}', estatura='{}', circunferenciaCintura='{}', IMC='{}', genero='{}', edad='{}', paquimetria='{}', glucosa='{}', 
                        presiónArterial='{}', diagnosticoOcular='{}', tratamientos='{}', seguimiento='{}', proximaVisita='{}' Where idPaciente='{}' """
                        .format(idPac, idPac, idPac, idPac, idPac, idPac, idPac, idPac, idPac, idPac, idPac, form.contrastSensitivity.data, form.tonometria.data, idPac, idPac, idPac, form.OSDI.data, form.BUT.data, form.schirmer.data, form.pesoCorporal.data, form.estatura.data, form.circunferenciaCintura.data, form.IMC.data,
                        form.genero.data, form.edad.data, form.paquimetria.data, form.glucosa.data, form.presiónArterial.data, form.diagnosticoOcular.data, form.tratamientos.data, form.seguimiento.data, form.proximaVisita.data, idPac))     
        conn.commit()
        cursor.close()
        conn.close()
        flash('Información guardada','success')

    #Al cargar la página queremos mostrar la información del paciente,
    #por lo que hacemos una busqueda de la información del paciente mediante su id
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("SELECT * FROM serviciosocial.optometria where idPaciente='{}'".format(idPac))
    data = cur.fetchall()
    cur.close()
    conn.close()

    return render_template('optometria.html', form=form, idPac=idPac, data=data)

#En esta función podemos visualizar los archivos guardados del paciente de la clínica de optometría
@app.route("/paciente/<id>/optometria/archivos", methods=['GET','POST'])
@login_required
def archivosOptometria(id):
    form=optometria()
    idPac=id

    #Tomamos como variable la primera parte fija de la ruta donde se encuentran los archivos
    #Primero iteramos los campos del form, después iteramos las carpetas del paciente en la clínica
    #Si el nombre de la carpeta y el nombre el campo coinciden, se agregan a una lista 
    #el nombre de la carpeta, el label del campo y los archivos dentro de las carpetas
    dir_path = "SitioClinicas/static/Archivos"
    res = []

    for field in form:
        for path in os.listdir(os.path.join(dir_path, idPac, "Optometria")):#Viendo el nombre de las carpetas 
            if field.name==path:
                res2=[path, field.label, os.listdir(os.path.join(dir_path, idPac, "Optometria", path))]
                res.append(res2)

    #Se muestra el template correspondiente tomando como parametros el id del paciente y la lista antes mencionada
    return render_template('archivosOptometria.html',idPac=idPac, res=res)

#Esta función es llamada traves de un JQuery en el html que permite la visualización de los archivos
#La función permite la eliminación de los archivos
@app.route('/background_process_test')
def background_process_test():
    #Se recibe como variable la parte de la ruta que incluye el id del paciente, clínica y el nombre del archivo
    #En caso de que el archivo sea eliminado se informa al usuario
    try:
        prueba = request.args.get('prueba', 0)
        dir_path = "SitioClinicas/static/Archivos/"+prueba
        os.remove(dir_path)
        flash ("Archivo eliminado", 'success')
    except:
        flash("El archivo ya fue eliminado", "succes")
    return ("nothing")

#Esta función es llamada traves de un JQuery en el html que permite la consulta del personal
#La función permite la eliminación del personal
@app.route('/background_process_test2')
def background_process_test2():

    #Se recibe como variable el id, clinica y rol del usuario
    #Se busca y se elimina al usuario de la base de datos
    #En caso de que el archivo sea eliminado se informa al usuario
    try:
        idUsuario = request.args.get('id', 0)
        clinica = request.args.get('clinica', 0)
        personal = request.args.get('personal', 0)
        
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute("SELECT usuario{}{} from {}{} where id{}{}='{}'".format(personal,clinica,personal,clinica,personal,clinica,idUsuario))
        data = cur.fetchone()
        cur.execute("DELETE from usuario where username='{}'".format(data[0]))
        cur.execute("DELETE from {}{}  where usuario{}{}='{}'".format(personal,clinica,personal,clinica,data[0]))
        conn.commit()
        cur.close()
        conn.close()
        flash ("Usuario eliminado", 'success')
        
    except:
        flash("El usuario ya fue eliminado", "succes")
    return ("nothing")

#La función de logout nos permite cerrar sesión
@app.route('/logout')
def logout():

    #Usamos la función logout_user para cerrar sesión, removemos la identidad y redireccionamos a la página de inicio de sesión
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):session.pop(key, None)
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())

    return redirect(url_for('hello_world'))

#Esta función nos permite obtener un link para cambiar nuestra contraseña en caso de olvidarla
@app.route('/recuperarContrasena', methods=['GET','POST'])
def recuperar():
    form=RecuperarForm()

    #Al recibir un request se busca en la base datos si el correo introducido existe
    if form.validate_on_submit():
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()
        cur.execute("SELECT id,correo FROM serviciosocial.usuario where correo='{}'".format(form.correo.data))
        data = cur.fetchall()
        cur.close()
        conn.close()
        column_names = [i[0] for i in cur.description]
        data_with_columns = [dict(zip(column_names, row)) for row in data]
        
        #En caso de que si exista, se crea un token que contiendrá el id del usuario asociado al correo
        #Y se mandará un correo con el link que incluye el token
        if data!=[]:
            serial=Serializer(app.config['SECRET_KEY'],expires_in=300)
            token=serial.dumps({'user_id':(data_with_columns[0])['id']}).decode('utf-8')
            msg=Message('Cambio de contraseña', recipients=[(data_with_columns[0])['correo']],sender='noreply@correo.com')
            msg.body=f'''Para cambiar tu contraseña presiona el link:

            {url_for('recuperar_token',token=token,_external=True)}

             '''

            mail.send(msg)
            flash('Correo enviado', 'success')
            return redirect(url_for('hello_world'))
        else:
            flash('Correo no encontrado', 'danger')
    return render_template('recuperarContraseña.html', form=form)

#Esta función es una continuación de la función anterior ya que es la 
#correspondiente al token creado, permite cambiar la contraseña
@app.route('/recuperarContrasena/<token>', methods=['GET','POST'])
def recuperar_token(token):

    #Se inicializa el Serializer para poder leer el token
    serial2=Serializer(app.config['SECRET_KEY'])
    form=CambiarForm()

    #Se lee el token y se obtiene el id del usuario, en caso contrario se le informa al usuario 
    try:
        user_id=serial2.loads(token)['user_id']
    except:
        flash('No se encuentra el usuario o el link expiró', 'danger')
        return redirect(url_for('recuperar'))
    
    #Al recibir un request, nos conectamos a la base de datos y se cambia la contraseña del usuario
    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.password.data)

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("UPDATE usuario set contraseña='{}' where id='{}' ".format(hashed_password,user_id))

        conn.commit()
        cursor.close()
        conn.close()
        flash('La contraseña se ha cambiado, por favor inicia sesion', 'success')
        return redirect(url_for('hello_world'))
    return render_template('cambiarContraseña.html', form=form)

#Esta función maneja el error 403 que aparece cuando alquien 
#intenta acceder a alguna página sin los permisos necesarios
@app.errorhandler(403)
def page_not_found(e):
    flash("No tienes permiso para acceder a este recurso","danger")
    return redirect(url_for('inicio'))