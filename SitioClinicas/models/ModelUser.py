from .entities.User import User

#Se crea una clase ModelUser
class ModelUser():

    #Contiene una función que obtiene la información de dicho usuario en la base de datos para poder iniciar sesión
    @classmethod
    def login(self, db, user):
        try:
            print("voy a conectarme a la db")
            cursor = db.cursor()
            print("me conecte a la db")
            sql = """SELECT id, username, contraseña, rol, clinica FROM usuario
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            print("ejecute la SQL")
            row = cursor.fetchone()
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password), row[3], row[4])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    #Contiene una función que obtiene la información a traves del id del usuario en la base de datos
    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.cursor()
            sql = "SELECT id, username, rol, clinica FROM usuario WHERE id = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return User(row[0], row[1], None, row[2], row[3])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)