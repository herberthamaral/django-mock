import fudge
import json

def stub(name='stub'):
    return fudge.Fake(name).is_a_stub()

class FakeDjangoQuerySet(list):
    def __init__(self, iterable=None, fixtures='', model=''):
        if iterable is not None:
            super(FakeDjangoQuerySet, self).__init__(iterable)
        if fixtures != '':
            self.load_fixtures(fixtures, model)
    
    def load_fixtures(self, fixtures, model):
        content = open(fixtures).read()
        objects = json.loads(content)
        objects = [o for o in objects if o['model'] == model]
        modelname = model.split('.')[1]
        for o in objects:
            fakeobj = stub(modelname)
            self.add_from_dict(modelname, o['fields'], o['pk'])

    def add_from_model_object(self, obj):
        if obj.id is not None:
            return
        if self.__len__() == 0:
            obj.id = 1
        else:
            obj.id = self.order_by('-id')[0].id+1
        self.append(obj)

    def add_from_dict(self, name, thedict, pk=0):
        fakeobj = stub(name)
        for key, value in thedict.items():
            setattr(fakeobj, key, value)

        if pk != 0:
            fakeobj.id = pk
        elif self.__len__() == 0:
            fakeobj.id = 1
        else:
            fakeobj.id = self.order_by('-id')[0].id+1
          
        self.append(fakeobj)

    def count(self):
        return self.__len__()

    def all(self):
        return self

    def filter(self, **kwargs):
        filtered = FakeDjangoQuerySet([])
        items = kwargs.items()
        first = items[0]
        filtered = self._filter(first[0], first[1], self)
        items = items[1:]
        for key, value in items:
            filtered = self._filter(key, value, filtered)
        return filtered

    def _filter(self, key, value, filtered):
        returns = FakeDjangoQuerySet([])
        for item in filtered:
            if key.endswith('__gt'):
                if getattr(item, key[0:-4]) > value:
                    returns.append(item)
            if key.endswith('__lt'):
                if getattr(item, key[0:-4]) < value:
                    returns.append(item)
            elif getattr(item, key) == value:
                returns.append(item)
        return returns


    def order_by(self, field):
        reverse = False
        if field.startswith('-'):
            reverse = True
            field = field[1:]
        return sorted(self, key=lambda sortfield: getattr(sortfield, field), reverse=reverse)

