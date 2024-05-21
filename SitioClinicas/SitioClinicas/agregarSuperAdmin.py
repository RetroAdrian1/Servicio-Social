from werkzeug.security import generate_password_hash
import mysql.connector

# Configura los detalles de la conexión a la base de datos
db_config = {
    'user': 'root',
    'password': '6patapollo',
    'host': 'localhost',
    'database': 'serviciosocial',
}

def agregar_usuario(id ,usuariosuperAdmin, password, rol):
    # Genera el hash de la contraseña utilizando werkzeug
    password_hashsuperAdmin = generate_password_hash(password)

    # Conecta a la base de datos
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Inserta el nuevo usuario en la base de datos
    cursor.execute('INSERT INTO usuario (username, contraseña, rol) VALUES (%s, %s, %s)', (usuariosuperAdmin, password_hashsuperAdmin, rol))
    conn.commit()
    cursor.execute('INSERT INTO superAdmin  VALUES (%s, %s, %s, %s)', (id, usuariosuperAdmin, password_hashsuperAdmin, None))
    conn.commit()
    # Cierra la conexión a la base de datos
    cursor.close()
    conn.close()

    print('El usuario se ha agregado exitosamente.')

# Ejemplo de uso
#nuevo_id = input('Ingrese el id del usuario: ')
#nuevo_username = input('Ingrese el nombre de usuario: ')
#nuevo_password = input('Ingrese la contraseña: ')
#nuevo_rol = input('Ingrese el rol: ')

nuevo_id = "1"
nuevo_username = "SuperAdmin1"
nuevo_password = "123"
nuevo_rol = "SuperAdmin"

agregar_usuario(nuevo_id, nuevo_username, nuevo_password, nuevo_rol)