from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

login_manager=LoginManager(app)
app.config['SECRET_KEY']='0896709031ff17d407ba27a6ad0dd96e'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']='adrimarvi16@gmail.com'
app.config['MAIL_PASSWORD']='rbda fcdb ydvb luza'

mail=Mail(app)

from SitioClinicas import Prueba