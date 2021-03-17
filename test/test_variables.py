from variables import VariableSet
import sys
sys.path.append("..")


def test_qwe():
    a = VariableSet()
    a.addVariable("id", "1")
    a.addVariable("name", "admin")
    a.addVariable("password", "123456")
    assert a.urlEncoded() == "id=1&name=admin&password=123456"
    print(a.urlEncoded())


test_qwe()
