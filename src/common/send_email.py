
import os
import json
import smtplib
from email.mime.text import MIMEText

from loguru import logger

import common.supports as supports


@logger.catch
def send_message(subject, content):
    config_file = os.path.join(supports.get_project_root_folder(), "config.json")
    with open(config_file, 'r') as f:
         config = json.load(f)
    
    smtp_host   = config["notification"]["email"]["smtp_host"]
    smtp_port   = config["notification"]["email"]["smtp_port"]
    sender      = config["notification"]["email"]["from"]
    to          = config["notification"]["email"]["to"]
    # cc          = config["notification"]["email"]["cc"]
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
