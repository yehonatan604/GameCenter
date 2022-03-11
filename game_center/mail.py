import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def forgot_password():
    mail_content = 'Dear mister. this is tryout,\nthanks for trying.\n\n\n'
    subject = "hello, world!"
    receiver_address = "peyoteking@gmail.com"
    return [receiver_address, subject, mail_content]


to_send = forgot_password()


def send_it(receiver_address, subject, mail_content):
    sender_address = "gameroom604@gmail.com"
    sender_pass = "123456abc1234"

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = subject

    message.attach(MIMEText(mail_content, 'plain'))
    text = message.as_string()

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_address, sender_pass)
    server.sendmail(sender_address, receiver_address, text)
    server.quit()


send_it(to_send[0], to_send[1], to_send[2])
