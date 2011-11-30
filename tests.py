import unittest
import fudge
from djangomock import FakeDjangoQuerySet, stub


class TestFakeDjangoQueryset(unittest.TestCase):
    def setUp(self):
        self.objects = FakeDjangoQuerySet()

    def test_all(self):
        self.objects = FakeDjangoQuerySet([1,2,3])
        self.assertEquals(3, self.objects.all().count())
    
    def test_filter_equals(self):
        person1 = stub('person1').has_attr(age = 12)
        person2 = stub('person2').has_attr(age = 13)
        person3 = stub('person3').has_attr(age = 12)
        self.objects = FakeDjangoQuerySet([person1, person2, person3,])
        self.assertEquals(1, self.objects.filter(age = 13).count())
        self.assertEquals(2, self.objects.filter(age = 12).count())

    def test_multiple_filter(self):
        person1 = stub('person1').has_attr(age = 12, sex='male')
        person2 = stub('person2').has_attr(age = 13, sex='male')
        person3 = stub('person2').has_attr(age = 13, sex='female')
        person4 = stub('person3').has_attr(age = 12, sex='female')
        self.objects = FakeDjangoQuerySet([person1, person2, person3, person4])
        self.assertEquals(1, self.objects.filter(age = 13, sex='male').count())

    def test_filter_gt(self):
        person1 = stub('person1').has_attr(age = 12)
        person2 = stub('person2').has_attr(age = 13)
        person3 = stub('person3').has_attr(age = 13)
        self.objects = FakeDjangoQuerySet([person1, person2, person3,])
        self.assertEquals(2, self.objects.filter(age__gt =  12).count())

    def test_filter_lt(self):
        person1 = stub('person1').has_attr(age = 12)
        person2 = stub('person2').has_attr(age = 13)
        person3 = stub('person3').has_attr(age = 13)
        self.objects = FakeDjangoQuerySet([person1, person2, person3,])
        self.assertEquals(1, self.objects.filter(age__lt =  13).count())

    def test_order_by(self):
        person1 = stub('person1').has_attr(age = 14)
        person2 = stub('person2').has_attr(age = 13)
        person3 = stub('person3').has_attr(age = 12)
        self.objects = FakeDjangoQuerySet([person1, person2, person3,])
        self.assertEquals(12, self.objects.order_by('age')[0].age)
        self.assertEquals(13, self.objects.order_by('age')[1].age)

    def test_order_by_desc(self):
        person1 = stub('person1').has_attr(age = 14)
        person2 = stub('person2').has_attr(age = 18)
        person3 = stub('person3').has_attr(age = 10)
        self.objects = FakeDjangoQuerySet([person1, person2, person3,])
        self.assertEquals(18, self.objects.order_by('-age')[0].age)
        self.assertEquals(14, self.objects.order_by('-age')[1].age)

    def test_it_can_load_fixtures(self):
        queryset = FakeDjangoQuerySet(fixtures='fixtures.json', model='auth.permission')
        self.assertEquals(3, queryset.count())

if __name__=='__main__':
    unittest.main()
