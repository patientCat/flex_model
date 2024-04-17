def readable(cls):
    def __str__(self):
        readable_str_list = []
        for attr_name in dir(self):
            if not callable(getattr(self, attr_name)) and not attr_name.startswith("__"):
                attr_value = getattr(self, attr_name)
                readable_str_list.append(f"{attr_name}: {attr_value.__str__()}")
        return f'{cls.__name__}({",".join(readable_str_list)})'

    def __repr__(self):
        return self.__str__()

    cls.__str__ = __str__
    cls.__repr__ = __repr__
    return cls

