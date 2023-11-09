from flask import Flask, request
import RedisConnectionPool as rcp
import json
from utils import get_all_keys
from flask_cors import cross_origin

# 获取redis连接
# key为数据库的表名
chronic_redis_conn = rcp.chronic_disease_redis
chronic_redis2_conn = rcp.chronic_disease2_redis
app = Flask(__name__)


@app.route('/init_info', methods=["GET", "POST"])
@cross_origin()
def get_data():
    # 获取慢性病的数据源列表
    disease_category_json = chronic_redis_conn.lrange("ChronicDisease_new", 0, -1)
    # 获取所有数据源的长度值 总数据量
    # disease_all_length = chronic_redis_conn.get("ChronicDisease_all_length").decode('utf-8')
    resource_length = len(disease_category_json)
    # all_length = int(disease_all_length)
    source_category_data = [json.loads(i) for i in disease_category_json]
    all_length = 0
    for i in source_category_data:
        # todo json.loads会自动将对data.decode("utf8")
        data = json.loads(get_lenght(i['length']).data)
        i['length'] = data['length']
        all_length += int(data['length'])
    result = {"resource": source_category_data, "resource_length": resource_length,
              "all_length": str(all_length)}

    return result


@app.route("/get_cate_data", methods=['post'])
@cross_origin()
def get_cate_data():
    key = request.form.get("key")

    start = request.form.get("start")
    end = request.form.get("end")
    print(key, start, end)
    """
    {
    "key":"wechat_data",
    "start":1,
    "end":50
    }
    """
    temp_redis_conn = chronic_redis_conn
    temp_redis2_conn = chronic_redis2_conn
    # 获取数据库2里面的值
    redis2_keys = get_all_keys()
    try:
        if key:
            print(key)
            if key in redis2_keys:
                key_cate_data = temp_redis2_conn.lrange(key, start, end)
            else:
                key_cate_data = temp_redis_conn.lrange(key, start, end)
            result_data_list = [str(json.loads(i)) for i in key_cate_data]
            for i in range(len(result_data_list)):
                result_data_list[i] = result_data_list[i].replace("'", '"')
            # todo 获取数据长度
            length_key = key + "_length"
            length_data = json.loads(get_lenght(length_key).data)
            print(result_data_list)
            result_data = {
                "data": result_data_list,
                "length": length_data['length']
            }
            print(result_data)
            return result_data
        else:
            return {"data": [], "length": 0}
    except Exception as e:
        print(e)
        return {"data": [], "length": 0}


@app.route("/del", methods=['post'])
@cross_origin()
def delete_in_redis():
    key = request.form.get("key")
    category_name = request.form.get("category_name")
    count = request.form.get("count")
    value = request.form.get("del_value")
    print(key)
    print(count)
    print(value)
    temp_redis = chronic_redis_conn

    # 后面这里改成redis事务写
    # 删除对应数据
    del_pipline = temp_redis.pipeline()
    del_pipline.lrem(key, count, value)
    # 总长度自减
    del_pipline.decr("ChronicDisease_all_length")
    del_result = del_pipline.execute()

    # 删除完毕
    response_data = {}
    if del_result[0]:
        response_data['state'] = 200
        response_data['message'] = "删除成功"
    else:
        response_data['state'] = 100
        response_data['message'] = "删除失败"

    return response_data


@app.route("/length", methods=['get', 'post'])
@cross_origin()
def get_lenght(key="no_key"):
    if key == "no_key":
        key = request.form.get("key")
    print(key)
    redis2_keys = get_all_keys()
    if key in redis2_keys:
        temp_redis_conn = chronic_redis2_conn
    else:
        temp_redis_conn = chronic_redis2_conn
    length = temp_redis_conn.get(key)
    print("这里是length")
    print(length)
    if length is not None:
        length = length.decode('utf-8')
    else:
        length = "0"
    print({"length": length})
    return {"length": length}


@app.route("/get_article", methods=['post'])
@cross_origin()
def get_wx_article(key="no_key"):
    article_data = []
    try:
        all_keys = get_all_keys()
        for key in all_keys:
            if key.endswith("_length"):
                continue
            # 获取每个表中的所有文章
            articles = chronic_redis2_conn.lrange(key, 0, -1)
            articles = [json.loads(i) for i in articles]
            for article in articles:
                try:
                    if article['content'] is None:
                        continue
                    # cid 默认为0
                    article['cid'] = 0
                    # 封面图片先为空
                    article['image'] = article.pop('cover')
                    # 将link的名字修改为original_url
                    article['original_url'] = article.pop('link')
                    print(article)
                except Exception as e:
                    continue
                article_data.append(article)
        data = {
            "code": 1,
            "show": 1,
            "msg": "请求成功",
            "data": article_data
        }
        print(len(article_data))
        return data
    except Exception as e:
        print(e)
        data = {
            "code": 0,
            "show": 1,
            "msg": "请求失败",
            "data": []
        }
        return data


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=7777, debug=False)
    app.run(host="0.0.0.0", port=5000, debug=True)
