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
#--Fucking Threading
from threading import Lock
class ODST():
    def __init__(self, *args, **kwargs):
        self.dict = dict(*args, **kwargs)
        self.lock = Lock()
    def __iter__(self):
        with self.lock:
            return (key for key in self.dict)
    def __repr__(self):
        with self.lock:
            return repr(self.dict)
    def __str__(self):
        with self.lock:
            return str(self.dict)
    def __len__(self):
        with self.lock:
            return len(self.dict)
    def __getitem__(self,key):
        with self.lock:
            return self.dict[key]
    def __setitem__(self,key,value):
        value = rec_dict(value)
        with self.lock:
            self.dict[key]=value
    def __delitem__(self,key):
        with self.lock:
            del self.dict[key]
    def get(self,key,default=None):
        with self.lock:
            if key in self.dict:
                return self.dict[key]
            return default;
    def update(self,alt):
        with self.lock:
            return self.dict.update(alt)
    def keys(self):
        with self.lock:
            return self.dict.keys()
    def items(self):
        with self.lock:
            return self.dict.items()
    def values(self):
        with self.lock:
            return self.dict.values()
#--Fuck Everying
def rec_dict(data):
    if isinstance(data, dict):
        safely = ODST(); safely.update(
            {k: rec_dict(v) for k,v in data.items()}
        ); return safely
    if isinstance(data, (tuple, list, set, frozenset)):
        return type(data)(rec_dict(v) for v in data)
    return data
