from typing import Callable


def add_function_name(func: Callable):
    """
    装饰器 
    返回2元组，1.插件函数名 2.插件函数自身生成发包的信息
    """
    def wrapper(*args, **kwargs):
        return (func(*args), func.__name__)
    return wrapper
