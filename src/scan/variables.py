from typing import Dict, List
import json
import re
""""
参数基类
处理json www-encode  multipartEncoded 解码编码
"""


class Variable:
    def __init__(self, name, value=""):
        self.name = name
        self.value = value
        self.initValue = value

    def restore(self):
        self.value = self.initValue

    def updateValue(self, value):
        self.value = value

    def append(self, value):
        self.value += value

    def __str__(self) -> str:
        return "[ %s : %s ]" % (self.name, self.value)


class VariableSet:
    def __init__(self):
        self.variables: List[Variable] = []
        self.boundary = ""

    def __str__(self) -> str:
        return " ".join([item.__str__() for item in self.variables])

    def names(self) -> List[str]:
        dic = []
        for item in self.variables:
            dic.append(item.name)
        return dic

    def isExist(self, name) -> bool:
        return name in self.names()

    def addVariable(self, name, value):
        if not self.isExist(name):
            self.variables.append(Variable(name, value))

    def getVariables(self, name) -> str:
        for item in self.variables:
            if item.name == name:
                return item.value
        raise Exception("Variable %s not found" % name)

    def parseJsonEncoded(self, content):
        content: Dict[str, str] = json.loads(content)
        for key, val in content.items():
            self.addVariable(key, val)

    def parseUrlEncoded(self, content: str):
        for item in content.split("&"):
            key, value = item.split("=")
            self.addVariable(key, value)

    def parseMultipart(self, content, boundary=None):
        self.boundary = boundary
        r = re.compile(r'name="([^"]+)"\s+(\S+)\s')
        result = r.findall(content)
        for item in result:
            self.addVariable(item[0], item[1])

    def jsonEncoded(self):
        dic = {item.name: item.value for item in self.variables}
        return json.dumps(dic)

    def urlEncoded(self):
        return "&".join(["=".join([item.name, item.value])for item in self.variables])

    def multipartEncoded(self):
        content = ""
        for item in self.variables:
            content += "--"+self.boundary+"\r\n"
            content += 'Content-Disposition: form-data; name="%s"\r\n\r\n' % item.name
        content += "--"+self.boundary+"--"+"\r\n"
        return content
