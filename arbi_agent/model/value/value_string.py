from arbi_agent.model.value.value import Value
from arbi_agent.configuration import GLValueType


class StringValue(Value):
    def __init__(self, value):
        self.value = self.unescape(value)

    def unescape(self, content):
        if type(content) == bytes:
            content = content.replace(b"&lt;", b"<")
            content = content.replace(b"&gt;", b">")
            content = content.replace(b"&amp;", b"&")
            content = content.replace(b"&quot;", b"\"")
            content = content.replace(b"&apos;", b"\'")
        elif type(content) == str:
            content = content.replace("&lt;", "<")
            content = content.replace("&gt;", ">")
            content = content.replace("&amp;", "&")
            content = content.replace("&quot;", "\"")
            content = content.replace("&apos;", "\'")
        return content

    def escape(self, content):
        str_list = []
        for i in content:
            if i == "<":
                str_list.append("&lt;")
            elif i == ">":
                str_list.append("&gt;")
            elif i == "&":
                str_list.append("&amp;")
            elif i == "\"":
                str_list.append("&quot;")
            elif i == "\'":
                str_list.append("&apos;")
            else:
                str_list.append(i)

        return ''.join(map(str, str_list))

    def get_type(self):
        return GLValueType.TYPE_STRING

    def int_value(self) -> int:
        return self.value.__len__()

    def float_value(self) -> float:
        return self.value.__len__()

    def string_value(self) -> str:
        return self.value

    def boolean_value(self) -> bool:
        if self.value is not None:
            if self.value.__len__() > 0:
                return True
        return False

    def add(self, value: Value) -> Value:
        raise Exception()

    def sub(self, value: Value) -> Value:
        raise Exception()

    def mul(self, value: Value) -> Value:
        raise Exception()

    def div(self, value: Value) -> Value:
        raise Exception()

    def mod(self, value: Value) -> Value:
        raise Exception()

    def lt(self, value: Value) -> bool:
        if value.get_type() == GLValueType.TYPE_STRING:
            return self.value < value.string_value()
        
        if self.value == "":
            return False

        raise Exception()

    def gt(self, value: Value) -> bool:
        if value.get_type() == GLValueType.TYPE_STRING:
            return self.value > value.string_value()
        
        if self.value == "":
            return False

        raise Exception()

    def eq(self, value: Value) -> bool:
        if value.get_type() == GLValueType.TYPE_STRING:
            return self.value == value.string_value()
        
        if self.value == "":
            return False

        raise Exception()

    def equals(self, obj) -> bool:
        if obj == self:
            return True
        
        if self.value == "":
            return False

        if isinstance(obj, Value):
            return self.eq(obj)
        else:
            return False

    def __str__(self):
        return '"' + self.escape(self.value) + '"'

    def hashcode(self) -> int:
        return hash(self.value)
