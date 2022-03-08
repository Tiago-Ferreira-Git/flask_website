
# -*- coding: utf-8 -*-
from flask import Flask, escape, request, render_template,url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, RoleMixin, login_required,UserMixin
from wtforms import StringField
from flask_security.forms import RegisterForm, Required
from flask_mail import Mail, Message
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formataddr
from email.utils import formatdate
from email.utils import COMMASPACE
from email.header import Header
from email import encoders
import smtplib, ssl
from email.mime.multipart import MIMEMultipart



 
 
app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "#######################"
app.config['SECURITY_PASSWORD_SALT'] = "##############"
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = '###############'
app.config['SECURITY_POST_LOGIN_VIEW'] = '/contact/'
app.config['SECURITY_POST_LOGOUT_VIEW'] ='/contact/'
db = SQLAlchemy(app)
mail = Mail(app)
 
# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
        db.Column('produtos_id', db.Integer(), db.ForeignKey('produtos.id')))


class ExtendedRegisterForm(RegisterForm):
    name = StringField('Nome', [Required()])
    morada = StringField('Morada', [Required()])



class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    morada = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
class Produtos(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name =  db.Column(db.String(80), unique=True)
    quantidade = db.Column(db.Integer)

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app,user_datastore,register_form=ExtendedRegisterForm)

def send_email(sender_name: str, sender_addr: str, smtp: str, port: str,
               recipient_addr: list, subject: str, text: str,
               fn: str='last.eml', save: bool=False):

    passwd = getpass.getpass('Password: ')

    sender_name = Header(sender_name, 'utf-8').encode()

    msg_root = MIMEMultipart('mixed')
    msg_root['Date'] = formatdate(localtime=1)
    msg_root['From'] = formataddr((sender_name, sender_addr))
    msg_root['To'] = COMMASPACE.join(recipient_addr)
    msg_root['Subject'] = Header(subject, 'utf-8')
    msg_root.preamble = 'This is a multi-part message in MIME format.'

    msg_related = MIMEMultipart('related')
    msg_root.attach(msg_related)

    msg_alternative = MIMEMultipart('alternative')
    msg_related.attach(msg_alternative)

    

    mail_server = smtplib.SMTP(smtp, port)
    mail_server.ehlo()
    mail_server.starttls()
    try:
        mail_server.starttls()
        mail_server.ehlo()
    except smtplib.SMTPException as e:
        print(e)

    mail_server.login(sender_addr, passwd)
    mail_server.send_message(msg_root)
    mail_server.quit()

    if save:
        with open(fn, 'w') as f:
            f.write(msg_root.as_string())

@app.route('/', methods=["POST","GET"])
def index():
    if request.method == "POST":
        number = request.form.get("number")
        return render_template('index.html',number = number)
    else :
        number = None
        lista_produtos = [
        {
            "Produt" : Produtos.query.get(1).name,
            "Quantity": Produtos.query.get(1).quantidade,
            "img_link" : "link"
        },
        {
            "Produt" : Produtos.query.get(2).name,
            "Quantity": Produtos.query.get(2).quantidade,
            "img_link" : "link"
        },
        {
            "Produt" : Produtos.query.get(3).name,
            "Quantity": Produtos.query.get(3).quantidade,
            "img_link" : "link"
        }
    ]
    return render_template('index.html',products = lista_produtos)
@app.route('/contact/', methods=["GET"])
def contact():
    lista_produtos = [
        {
            "Produt" : Produtos.query.get(1).name,
            "Quantity": Produtos.query.get(1).quantidade,
            "img_link" : "###"
        },
        {
            "Produt" : Produtos.query.get(2).name,
            "Quantity": Produtos.query.get(2).quantidade,
            "img_link" : "###"
        },
        {
            "Produt" : Produtos.query.get(3).name,
            "Quantity": Produtos.query.get(3).quantidade,
            "img_link" : "###"
        }
    ]
    return render_template('contact.html',products = lista_produtos)
    
#@app.route('/add_user', methods=["POST"])
#def add_user():
#    teste = User(email = request.form.get("email"), password = request.form.get("password"))
#    db.session.add(teste)
#    db.session.commit()
#    return redirect(url_for('contact',username = request.form['email'])) 


@app.route('/login_teste', methods=["POST"])
def login_teste():
    if request.method == "POST":
        try:
            name = request.form.get("email")
        except ValueError:
            return render_template("error.html", message="Invalid username.")
        
        try:
            password = request.form.get("password")
        except ValueError:
            return render_template("error.html", message="Invalid username.")

        myUser = User.query.filter_by(email=name).first()
        if myUser != None:
            if myUser.email == name and myUser.password == password:
                #return redirect(url_for('contact',username = name))
                return render_template("contact.html", username=name,products = lista_produtos)
            else:
                return redirect(url_for('login', error = "password"))       
        else:
            return redirect(url_for('login', error = "email"))
@app.route('/login', methods=["GET"])
def login():
    return render_template("login.html")


@app.route('/compra', methods = ["POST"]) 
def compra():
    if request.method == "POST":
        try:
            numeros = request.form.getlist('number')
            lista_produtos = [
            {
                "Produt" : Produtos.query.get(1).name,
                "Quantity": Produtos.query.get(1).quantidade,
                "Proposta" : int(numeros[0])
            },
            {
                "Produt" : Produtos.query.get(2).name,
                "Quantity": Produtos.query.get(2).quantidade,
                "Proposta" : int(numeros[1])
            },
            {
                "Produt" : Produtos.query.get(3).name,
                "Quantity": Produtos.query.get(3).quantidade,
                "Proposta" : int(numeros[2])
            }
            ]
        
            for i in range(3):
                if int(numeros[i]) == 0:
                    if len(lista_produtos) <= 2:
                        if i == 2:
                            lista_produtos.remove(lista_produtos[1])
                        elif i == 1:
                            lista_produtos.remove(lista_produtos[0])
                    else:
                        lista_produtos.remove(lista_produtos[i])
            return render_template("compra.html",products = lista_produtos)
        except ValueError:
            return render_template("error.html", message="Não deu.")
        
@app.route('/finalizar', methods = ["POST"])
def finalizar():
    data = list()
    initializer = 0
    password = "###"
    # Create a secure SSL context
    context = ssl.create_default_context()

    try:
        numeros = request.form.get('content')
        email = request.form.get('email')
        adress = request.form.get('adress')
        name = request.form.get('name')
        euros = request.form.get('euros')
        for i in range(3):
            find = numeros.find('=',initializer)
            if find > 0:
                try:
                    to_append = int(numeros[find+1:find+3])
                except:
                    to_append= int(numeros[find+1:find+2])
                data.append(to_append)
                initializer = find+1
            
        if len(data) != 0:
            for i in range(len(data)):
                Produtos.query.get(i+1).quantidade = Produtos.query.get(i+1).quantidade - int(data[i])
                
                db.session.commit()
            
        else:
            return jsonify({"success":False})

        # Try to log in to server and send email
        try:
            message =  """\
                Olá senhor/a {},
                Agradecemos a sua encomenda de {} euros de medronho para a morada {}
                Atenciosamente,
                 """.format(name, euros, adress)
            sender_name = '#######'
            sender_addr = '##########'
            smtp = 'smtp.gmail.com'
            port = '587'
            recipient_addr = ['#####']
            subject = 'Confirmação da encomenda'
            send_email(sender_name, sender_addr, smtp, port, recipient_addr, subject, message, fn='my.eml', save=True)
            return jsonify({"success":True})
        except Exception as e:
            # Print any error messages to stdout
            print(e)
            return jsonify({"success":False})
        finally:
            server.quit()
    except:
        return jsonify({"success":False})

if __name__ == "__main__":
    app.run(host = '127.0.0.1', port = 5000, threaded=True)


