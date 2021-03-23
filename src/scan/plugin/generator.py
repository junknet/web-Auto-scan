from sys import meta_path
from types import MethodWrapperType
from typing import Dict

from scan.http_meta import HttpMeta
from .func_decorator import add_function_name
from scan.parse_request import RequestParse
from queue import Queue
from scan.variables import VariableSet

"""
 if "application/json" in self.headers["Content-Type"]:
            data = self.data.jsonEncoded()
        elif "x-www-form-urlencoded" in self.headers["Content-Type"]:
            data = self.data.urlEncoded()
        else:
            data = self.data.multipartEncoded()
"""

# 编码 body包成str 发射

sql_payload = []


def encode_data(headers: Dict[str, str], data: VariableSet) -> str:
    if "application/json" in headers["Content-Type"]:
        post_data = data.jsonEncoded()
    elif "x-www-form-urlencoded" in headers["Content-Type"]:
        post_data = data.urlEncoded()
    else:
        post_data = data.multipartEncoded()
    return post_data


def attack_request_start(parsed_request: RequestParse, que: Queue, debug: bool):
    payloads_loading()
    http_meta = parsed_request.http_meta()
    print(http_meta)
    # 开始生成成攻击报文
    # no_change(http_meta, que)
    sql_attack_param(http_meta, que)


def no_change(meta: HttpMeta, que: Queue):
    que.put(meta.post_meta('no_change'))


def sql_attack_param(meta: HttpMeta, que: Queue):
    global sql_payload
    for param in meta.data.variables:
        for payload in sql_payload:
            param.updateValue(payload)
            # print(meta.post_meta('sql_attack_param'))
            que.put(meta.post_meta('sql_attack_param'))
        param.restore()


def payloads_loading():
    global sql_payload
    path = __file__.split('/')
    base_path = '/'.join(path[:-4])
    try:
        sql_payload = open(
            base_path+"/payload/Sql_Injection/Sql.txt").read().split('\n')
    except Exception as e:
        print("sql_payload load failed!")
        raise e
