import unittest
from Object import ConcreteObject

class TestObject(unittest.TestCase):

    def test_relation_category_is_initialized_correctly(self):
        concrete_object = ConcreteObject("city", "Berlin")
        self.assertEqual("city", concrete_object.category_name)
        self.assertEqual("Berlin", concrete_object.name)
