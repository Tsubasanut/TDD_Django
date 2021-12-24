from django.test import TestCase

# Create your tests here.
class MyTest(TestCase):

    def bad_math(self):
        self.assertEqual(1 + 1, 3)
