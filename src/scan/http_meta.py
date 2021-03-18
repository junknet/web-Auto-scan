import re
from typing import Dict
from .variables import VariableSet


# 返回格式 (self.method, self.url, self.headers, self.data)

class HttpMeta():
    def __init__(self, method: str, url: str, headers: Dict[str, str], data: VariableSet) -> None:
        self.method = method
        self.url = url
        self.headers = headers
        self.data = data
        # 初始化参数
        self.__method = self.method
        self.__url = self.url
        self.__headers = self.headers
        self.__data = self.data

    def restore_meta(self) -> None:
        self.method = self.__method
        self.data = self.__data
        self.url = self.__url
        self.data = self.__data

    def post_meta(self):

        return(self.method, self.url, self.headers, self.encode_data())

    def encode_data(self) -> str:
        if "application/json" in self.headers["Content-Type"]:
            post_data = self.data.jsonEncoded()
        elif "x-www-form-urlencoded" in self.headers["Content-Type"]:
            post_data = self.data.urlEncoded()
        else:
            post_data = self.data.multipartEncoded()
        return post_data

    def __str__(self) -> str:
        """
        保护视力(开始花里胡哨)
        """
        colors = {
            "purple": '\033[95m',
            "blue": '\033[94m',
            "green": '\033[92m',
            "yellow": '\033[33m',
            "red": '\033[31m',
            "magenta": '\033[35m',
            "cyan": '\033[36m',
        }
        default = '\033[0m'
        backgrounds = {
            'grey': '\033[40m', 'red': '\033[41m',
            'green': '\033[42m', 'yellow': '\033[43m',
            'blue': '\033[44m', 'magenta': '\033[45m',
            'cyan': '\033[46m', 'white': '\033[47m',
        }

        formats = {
            "bold": "\033[1m", "underline": "\033[4m", "blink": "\033[5m"
        }

        def colorful(raw_string: str, color=None):
            if color:
                return colors[color]+raw_string+default

        method = colorful("method: ", "yellow")+self.method+"\n"
        url = colorful("url: ", "blue")+self.url+"\n"
        headers = colorful("headers: ", "red")+self.headers.__str__()+"\n"
        data = colorful("data: ", "cyan")+self.data.__str__()
        return method+url+headers+data
