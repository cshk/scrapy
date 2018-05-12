import redis


def insert_start(str, type):
    try:
        r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    except:
        print('connect error')
    else:
        if 1 == type:
            r.lpush('start_urls', str)

def insert_req(str, type):
    try:
        r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    except:
        print('connect error')
    else:
        if 2 == type:
            r.lpush('58_zufang:requests', str)