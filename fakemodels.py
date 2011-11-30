from djangomock import FakeDjangoQuerySet

class Field(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class CharField(Field):
    pass

class AutoField(Field):
    pass

class ModelMetaclass(type):
    def __new__(klass, name, bases, dct):
        theclass = type.__new__(klass, name, bases, dct)
        fields = [getattr(theclass,field) for field in dir(theclass) if issubclass(type(getattr(theclass, field)), Field)]
        fields.insert(0, AutoField())
        setattr(theclass, 'fields', fields)
        setattr(theclass, 'objects', FakeDjangoQuerySet(model=name))
        return theclass

class Model(object):
    __metaclass__ = ModelMetaclass

