from flask_pymongo import PyMongo


def mongo_decorator(cls, mongo_repo):
    class MongoWrapped(object):
        def __init__(self, *args, **kwargs):
            self.mongo_wrapped = cls(*args, **kwargs)
            self.mongo_wrapped.repository = mongo_repo

        def __getattr__(self, item):
            return getattr(self.mongo_wrapped, item)

    return MongoWrapped


_injected = {}


class Component:
    def __init__(self, a_class):
        self.inner_class = a_class
        self.instance = None
        self.component_type = self.__class__.__name__

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.inner_class(*args, **kwargs)
        return self.instance


class Repository(Component):
    pass


class Service(Component):
    pass


@Component
class Context:
    def __init__(self, app):
        self.app = app
        self._mongo = None

    @property
    def mongo(self):
        if self._mongo is None:
            self._mongo = PyMongo(self.app)
        return self._mongo

    def __call__(self, a_class):
        injection_key = a_class.inner_class.__module__ + '.' + a_class.inner_class.__name__
        if injection_key not in _injected.keys():
            if a_class.component_type == Repository.__name__:
                _injected[injection_key] = mongo_decorator(a_class, self.mongo)()
            else:
                _injected[injection_key] = a_class()
        return _injected[injection_key]
