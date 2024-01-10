# -*-coding:utf-8 -*-

from loguru import logger
import requests

import common.supports as supports

@logger.catch
def send_message(subject, content, url = None):

    uids    = supports.APP_CONFIG["notification"]["wxpusher"]["uids"]
    token   = supports.APP_CONFIG["notification"]["wxpusher"]["token"]

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
    try:
        return requests.post("http://wxpusher.zjiecode.com/api/send/message", json=payload)
    except BaseException as e:
        logger.exception("Get exception when send wechat message", e)
        return None
