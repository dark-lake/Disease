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

def remove_cover():
    keys = get_all_keys()
    for key in keys:
        print(key)
        if key.endswith("_length"):
            continue
        data_length = chronic_redis2_conn.llen(key)
        for i in range(0, data_length):
            article = chronic_redis2_conn.lindex(key, i)
            try:
                article = json.loads(article)
            except Exception as e:
                print(i)
                chronic_redis2_conn.lrem(key, i, json.dumps(article))
                continue
            article['cover'] = ""
            chronic_redis2_conn.lset(key, i, json.dumps(article))
            print(article)

if __name__ == '__main__':
    remove_cover()
