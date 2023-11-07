import redis
from redis import ConnectionPool

chronic_disease_pool = ConnectionPool(host='39.96.138.111', port=6379, db=6, password='Sigsit123', max_connections=30)
#新数据库
chronic_disease2_pool = ConnectionPool(host='182.92.154.119', port=6379, db=1, password='Sigsit123', max_connections=30)
# 从连接池中获取 Redis 连接
#这个需要对应前端的数据库吗  redis_com = redis.Redis(connectin_pool=redis_pool)
chronic_disease_redis = redis.Redis(connection_pool=chronic_disease_pool)
#连接新的数据库
chronic_disease2_redis = redis.Redis(connection_pool=chronic_disease2_pool)

