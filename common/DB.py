import redis

import common.supports as supports

REDIS_CLIENT = redis.Redis(host=supports.APP_CONFIG["redis"]["host"], \
                        port=supports.APP_CONFIG["redis"]["port"], \
                            db=0, password=supports.APP_CONFIG["redis"]["password"], \
                                decode_responses=True)