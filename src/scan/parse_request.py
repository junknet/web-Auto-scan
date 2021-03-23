from asyncio.tasks import sleep
import re
from typing import Dict
from .variables import Variable, VariableSet
from .http_meta import HttpMeta


class RequestParse:
    def __init__(self, filename) -> None:
        self.__parsedFile = filename
        self.__host = None
        self.__path = None
        self.__method = None
        self.__params = None
        self.__headers = {}
        self.__url = None
        self.__content = None
        self.parseRequest()

    def parseRequest(self):
        file = open(self.__parsedFile, 'r')
        r = re.compile(r"^(\S+) (.*) HTTP\S*$")
        self.__method, self.__path = r.findall(file.readline())[0]
        # 解析http头
        r = re.compile("^([^:]+): (.*)$")
        while True:
            tp = r.findall(file.readline())
            if tp:
                self.addHeader(tp[0][0], tp[0][1])
            else:
                break
        self.__host = self.tryGetfromHeaders("Host")
        self.__url = "http://"+self.__host+self.__path
        self.__content = file.read()
        boundray = None
        # 解析 ContentType
        if "Content-Type" in self.__headers:
            values: str = self.__headers["Content-Type"].split(";")
            self.ContentType = values[0].strip().lower()
            if self.ContentType == "multipart/form-data":
                boundray = values[1].split("=")[1].strip()
        self.setPostData(boundray)

    def tryGetfromHeaders(self, key):
        try:
            tmp = self.__headers[key]
            return tmp
        except Exception as e:
            raise e

    def setPostData(self, boundray=None):
        self.variables = VariableSet()
        if "application/json" in self.ContentType:
            self.variables.parseJsonEncoded(self.__content)
        elif "x-www-form-urlencoded" in self.ContentType:
            self.variables.parseUrlEncoded(self.__content)
        else:
            self.variables.parseMultipart(self.__content, boundray)

    def addHeader(self, key, value):
        """
        去除"Content-Length"字段，让发包库自动添加，
        否则扩展报文的时候，按照原先"Content-Length"字段值
        导致远程服务器接收时提前截断，
        阿里的fastjson库直接报解析错误，可用来做探针,DDOS
        """
        if key != "Content-Length":
            self.__headers[key] = value

    def url(self):
        return self.__url

    def heads(self):
        return self.__headers

    def method(self):
        return self.__method

    def http_meta(self) -> HttpMeta:
        return HttpMeta(self.method(), self.url(),
                        self.heads(), self.variables)
