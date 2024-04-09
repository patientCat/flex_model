def to_string(cls):
    def __str__(self):
        attr_list = []
        for attr in vars(self):
            attr_value = getattr(self, attr)
            if hasattr(attr_value, '__str__'):
                attr_list.append(attr_value.__str__())
            else:
                attr_list.append(attr_value)
        return f'{cls.__name__}({",".join(attr_list)})'

    cls.__str__ = __str__
    return cls

