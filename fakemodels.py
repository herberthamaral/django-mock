from djangomock import FakeDjangoQuerySet

class Field(object):
    default = None
    name = ''
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

        if self.default is not None:
            self.value = self.default
    
    def __eq__(self, value):
        self.value = value

class CharField(Field):
    default = ''

class IntegerField(Field):
    default = 0

class AutoField(IntegerField):
    default = None

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
        fields = []
        for field in dir(theclass):
            if issubclass(type(getattr(theclass,field)), Field): 
                f = getattr(theclass, field)
                f.name = field
                fields.append(f)
            
        auto = AutoField()
        auto.name = 'id'
        fields.insert(0, auto)
        options = Options(name)
        options.fields = fields
        setattr(theclass, '_meta', options)
        setattr(theclass, 'objects', FakeDjangoQuerySet(model=name))
        return theclass

class Model(object):
    __metaclass__ = ModelMetaclass

    def __init__(self, **kwargs):
        for field in self._meta.fields:
            setattr(self, field.name, field.default)

    def save(self, **kwargs):
        self.objects.add_from_model_object(self)

