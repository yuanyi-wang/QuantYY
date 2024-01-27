# -*-coding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText

from loguru import logger

from common import supports


@logger.catch
def send_message(subject, content):
    smtp_host = supports.get_app_config("notification.email.smtp_host")
    smtp_port = supports.get_app_config("notification.email.smtp_port")
    sender = supports.get_app_config("notification.email.from")
    to = supports.get_app_config("notification.email.to")
    # cc        = supports.get_app_config("notification.email.cc")
    password = supports.get_app_config("notification.email.password")

    email_message = MIMEText(content)
    email_message["Subject"] = subject
    email_message["From"] = sender
    email_message["To"] = to
    # email_message['Cc'] = cc

    with smtplib.SMTP_SSL(host=smtp_host, port=smtp_port) as server:
        server.login(sender, password)
        server.sendmail(sender, to, email_message.as_string())
        logger.info("Successfully sent email")
