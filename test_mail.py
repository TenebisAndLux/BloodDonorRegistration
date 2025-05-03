import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

smtp_server = 'smtp.yandex.ru'
smtp_port = 465
login = 'matvej.averkin@yandex.ru'
password = 'oupkonmsitjlnqwy'

sender_email = login
receiver_email = 'egorogenia7m@yandex.ru'

subject = 'Тестовое письмо'
body = 'Привет! Это тестовое письмо, отправленное с помощью Python.'

message = MIMEMultipart()
message['From'] = sender_email
message['To'] = receiver_email
message['Subject'] = subject

message.attach(MIMEText(body, 'plain'))

try:
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    print('Письмо успешно отправлено!')
except Exception as e:
    print(f'Ошибка при отправке письма: {e}')
