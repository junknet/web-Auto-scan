from sys import meta_path
from typing import Dict
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


def encode_data(headers: Dict[str, str], data: VariableSet) -> str:
    if "application/json" in headers["Content-Type"]:
        post_data = data.jsonEncoded()
    elif "x-www-form-urlencoded" in headers["Content-Type"]:
        post_data = data.urlEncoded()
    else:
        post_data = data.multipartEncoded()
    return post_data

# 
def attack_no_change(parsed_request: RequestParse, que: Queue):
    (method, url, headers, data) = parsed_request.http_meta().post_meta()
    for _ in range(1000):
        post_data = encode_data(headers, data)
        que.put((method, url, headers, post_data))
