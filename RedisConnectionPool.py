import redis
from redis import ConnectionPool

chronic_disease_pool = ConnectionPool(host='39.96.138.111', port=6379, db=6, password='Sigsit123', max_connections=30)
# 从连接池中获取 Redis 连接
chronic_disease_redis = redis.Redis(connection_pool=chronic_disease_pool)

