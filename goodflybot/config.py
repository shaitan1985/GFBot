from .DataWorker import FSWorker

def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance

@singleton
class Config(object):
    __slots__ = ('__params',)

    def __init__(self):
        self.__params = {}
        self.load_static()

    def __iter__(self):
        return iter(self.__params.items())

    def __getattribute__(self, key):
        try:
            return super().__getattribute__(key)
        except AttributeError:
            return self.__params.get(key)

    def __setattr__(self, key, value):
        try:
            super().__setattr__(key, value)
        except AttributeError:
            self.__params[key] = value

    def __delattr__(self, key):
        try:
            super().__delattr__(key)
        except AttributeError:
            del self.__params[key]

    def load_static(self):
        tree = FSWorker.get_static()
        for key, value in tree.items():
            self.__setattr__(key, value)