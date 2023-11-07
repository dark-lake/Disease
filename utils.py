from flask import Flask, request
import RedisConnectionPool as rcp
import json
from flask_cors import cross_origin
# 获取redis连接
# key为数据库的表名
chronic_redis2_conn = rcp.chronic_disease2_redis

def get_all_keys():
    # 获取所有键值
    keys = chronic_redis2_conn.keys("*")
    # 关闭Redis连接
    chronic_redis2_conn.close()

    keys = [i.decode() for i in keys]
    print(keys)
    return keys

if __name__ == '__main__':
    get_all_keys()
