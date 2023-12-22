# -*-coding:utf-8 -*-

import smtplib
from email.mime.text import MIMEText

from loguru import logger

import common.supports as supports
config = supports.configuration

@logger.catch
def send_message(subject, content):
    supports.configuration
    
    smtp_host   = config["notification"]["email"]["smtp_host"]
    smtp_port   = config["notification"]["email"]["smtp_port"]
    sender      = config["notification"]["email"]["from"]
    to          = config["notification"]["email"]["to"]
    # cc          = secrets["notification"]["email"]["cc"]
    password    = config["notification"]["email"]["password"]

    email_message = MIMEText(content)
    email_message['Subject'] = subject
    email_message['From'] = sender
    email_message['To'] = to
    # email_message['Cc'] = cc

    with smtplib.SMTP_SSL(host=smtp_host, port=smtp_port) as server:
        server.login(sender, password)
        server.sendmail(sender, to, email_message.as_string())
        logger.info("Successfully sent email")
