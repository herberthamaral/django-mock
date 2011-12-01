from djangomock import FakeDjangoQuerySet

class Field(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def __eq__(self, value):
        self.value = value

class CharField(Field):
    pass

class AutoField(Field):
    pass

class Options(object):
    fields = []
    name = ''
    def __init__(self, name):
        self.name = name
    
    def __unicode__(self):
        return '<Options for '+self.name+'>'

    def __str__(self):
        return '<Options for '+self.name+'>'
        
class ModelMetaclass(type):
    def __new__(klass, name, bases, dct):
        theclass = type.__new__(klass, name, bases, dct)
        fields = [getattr(theclass,field) for field in dir(theclass) if issubclass(type(getattr(theclass, field)), Field)]
        fields.insert(0, AutoField())
        options = Options(name)
        options.fields = fields
        setattr(theclass, '_meta', options)
        setattr(theclass, 'objects', FakeDjangoQuerySet(model=name))
        return theclass

class Model(object):
    __metaclass__ = ModelMetaclass

