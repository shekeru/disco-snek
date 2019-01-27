#-- Message Structure
class _Map(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for arg in args:
            self.update(Map(arg))
    def __getattr__(self, attr):
        return self.get(attr)
    def __setattr__(self, key, value):
        self.__setitem__(key, value)
    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.__dict__.update({key: value})
    def __delattr__(self, item):
        self.__delitem__(item)
    def __delitem__(self, key):
        super().__delitem__(key)
        del self.__dict__[key]
    def update(self, alt):
        super().update(alt)
        self.__dict__.update(alt)
def Map(data):
    if isinstance(data, dict):
        safely = _Map(); safely.update(
            {k: Map(v) for k,v in data.items()}
        ); return safely
    if isinstance(data, (tuple, list, set, frozenset)):
        return type(data)(Map(v) for v in data)
    return data
