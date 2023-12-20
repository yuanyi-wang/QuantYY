# -*-coding:utf-8 -*-

import os
import json

from loguru import logger
import requests

import common.supports as supports

@logger.catch
def send_message(subject, content, url = None):
    secrets_file = os.path.join(supports.get_project_root_folder(), "secrets.json")
    with open(secrets_file, 'r') as f:
         secrets = json.load(f)

    uids    = secrets["notification"]["wxpusher"]["uids"]
    token   = secrets["notification"]["wxpusher"]["token"]

    logger.debug(f"uids is\n {uids}")
    logger.debug(f"contentis\n {content}")

    payload = {
            'appToken': token,
            "summary":subject,
            'content': content,
            'contentType': 1, # 1: text message; 2: html message without <body>; 3: markdown
            # 'topicIds': kwargs.get('topic_ids', []),
            'uids': uids,
            'url': url
        }

    return requests.post("http://wxpusher.zjiecode.com/api/send/message", json=payload)

    