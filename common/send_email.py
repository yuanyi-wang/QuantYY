# -*-coding:utf-8 -*-

import os
import json
import smtplib
from email.mime.text import MIMEText

from loguru import logger

import common.supports as supports


@logger.catch
def send_message(subject, content):
    secrets_file = os.path.join(supports.get_project_root_folder(), "secrets.json")
    with open(secrets_file, 'r') as f:
         secrets = json.load(f)
    
    smtp_host   = secrets["notification"]["email"]["smtp_host"]
    smtp_port   = secrets["notification"]["email"]["smtp_port"]
    sender      = secrets["notification"]["email"]["from"]
    to          = secrets["notification"]["email"]["to"]
    # cc          = secrets["notification"]["email"]["cc"]
    password    = secrets["notification"]["email"]["password"]

    email_message = MIMEText(content)
    email_message['Subject'] = subject
    email_message['From'] = sender
    email_message['To'] = to
    # email_message['Cc'] = cc

    with smtplib.SMTP_SSL(host=smtp_host, port=smtp_port) as server:
        server.login(sender, password)
        server.sendmail(sender, to, email_message.as_string())
        logger.info("Successfully sent email")
