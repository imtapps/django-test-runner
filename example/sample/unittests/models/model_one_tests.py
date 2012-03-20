from django.utils import unittest

class ModelOneTests(unittest.TestCase):

    def test_fail(self):
        self.fail("model one tests")
