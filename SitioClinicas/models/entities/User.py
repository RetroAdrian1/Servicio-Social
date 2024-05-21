from werkzeug.security import check_password_hash
from flask_login import UserMixin

#Se crea una clase User que contiene id, username, password, rol y clinica
class User(UserMixin):

    def __init__(self, id, username, password, rol="", clinica="") -> None:
        self.id = id
        self.username = username
        self.password = password
        self.rol = rol
        self.clinica = clinica

    #Se crea una función regresa True o False dependiendo de si la contraseña
    #introducida coincide con la guardada en la base de datos
    @classmethod
    def check_password(self, hashed_password, password):
        return check_password_hash(hashed_password, password)