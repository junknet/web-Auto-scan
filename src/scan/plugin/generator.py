from sys import meta_path, path
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

base_path = ""


def encode_data(headers: Dict[str, str], data: VariableSet) -> str:
    if "application/json" in headers["Content-Type"]:
        post_data = data.jsonEncoded()
    elif "x-www-form-urlencoded" in headers["Content-Type"]:
        post_data = data.urlEncoded()
    else:
        post_data = data.multipartEncoded()
    return post_data


def attack_request_start(parsed_request: RequestParse, que: Queue, debug: bool):
    # 利用payload和本文件的相对路劲取得绝对路劲
    global base_path
    path = __file__.split('/')
    base_path = '/'.join(path[:-4])+"/payload/"
    # 请求包 元信息
    http_meta = parsed_request.http_meta()
    print(http_meta)
    # 开始生成成攻击报文
    # no_change(http_meta, que)
    sql_attack_param(http_meta, que)
    brute_attack_login(http_meta, que)


def no_change(meta: HttpMeta, que: Queue):
    que.put(meta.post_meta('no_change'))


def brute_attack_login(meta: HttpMeta, que: Queue):
    data_names = meta.data.names()
    #  攻击条件检测
    if "username" in data_names and "password" in data_names:
        print('ok')
        (usernames, passwords) = brute_attack_load()
        for param in meta.data.variables:
            if param.name == "username":
                username_param = param
            if param.name == "password":
                password_param = param
        for username in usernames:
            username_param.updateValue(username)
            for password in passwords:
                password_param.updateValue(password)
                que.put(meta.post_meta('brute_attack_login'))


def brute_attack_load():
    global base_path
    try:
        username = open(
            base_path+"Brute_force/Top20_Admin_Username.txt").read().split('\n')
        password = open(
            base_path+"Brute_force/Top_Dev_Password.txt").read().split('\n')
        return (username, password)
    except Exception as e:
        print("sql_payload load failed!")
        raise e


def sql_attack_param(meta: HttpMeta, que: Queue):
    sql_payload = sql_payload_load()
    for param in meta.data.variables:
        for payload in sql_payload:
            param.updateValue(payload)
            # print(meta.post_meta('sql_attack_param'))
            que.put(meta.post_meta('sql_attack_param'))
        param.restore()


def sql_payload_load():
    global base_path
    try:
        return open(base_path+"Sql_Injection/Sql.txt").read().split('\n')
    except Exception as e:
        print("sql_payload load failed!")
        raise e
