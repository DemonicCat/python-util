import redis

def create_redis_cli(server, db):
    host, port = server
    args = {
        "host": host,
        "port": int(port),
        "socket_timeout": 2,
        "db": db
    }
    pool = redis.BlockingConnectionPool(**args)
    return redis.StrictRedis(connection_pool=pool)

def_redis_cli = create_redis_cli(('192.168.1.198', 5959), 0)

if __name__ == '__main__':
    print def_redis_cli.get(12)
    print def_redis_cli.get(2111)
