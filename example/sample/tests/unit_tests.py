from django.utils import unittest

class RunnerTests(unittest.TestCase):

    def setUp(self):
        from djtest_runner import DjangoPyCharmRunner
        self.runner = DjangoPyCharmRunner()

    def test_returns_test_suite(self):
        result = self.runner.build_suite('')
        self.assertIsInstance(result, unittest.TestSuite)

    def test_returns_x_tests_when_no_label(self):
        result = self.runner.build_suite('')
        self.assertEqual(result.countTestCases(), 100)

    def test_check_return_value_for_applabel(self):
        result = self.runner.build_suite(('sample',))
        self.assertGreater(result.countTestCases(), 0)

    def test_check_return_value_for_test_class(self):
        result = self.runner.build_suite(('sample.FormOneTests',))
        self.assertGreater(result.countTestCases(), 0)

    def test_return_value_for_applabel_greater_than_test_class(self):
        result_applabel = self.runner.build_suite(('sample',))
        result_test_class = self.runner.build_suite(('sample.FormOneTests',))
        self.assertGreater(result_applabel.countTestCases(),result_test_class.countTestCases())

    def test_return_value_for_specific_test_case(self):
        result = self.runner.build_suite(('sample.FormOneTests.test_fail',))
        self.assertEqual(result.countTestCases(), 1)

    def test_return_value_for_non_django_app(self):
        result = self.runner.build_suite(('sample',))
        self.assertGreater(result.countTestCases(), 0)

    def test_return_value_for_non_django_test(self):
        result = self.runner.build_suite(('sample.FormOneTests',))
        self.assertGreater(result.countTestCases(), 0)
