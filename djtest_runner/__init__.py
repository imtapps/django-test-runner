from unittest.loader import defaultTestLoader
from django.core.exceptions import ImproperlyConfigured
from django.test.simple import DjangoTestSuiteRunner
import re
import os
import fnmatch
from django.db.models.loading import get_app
from django.utils import unittest as ut2
from django.conf import settings

import xmlrunner

class DjangoPyCharmRunner(DjangoTestSuiteRunner):

    def run_suite(self, suite, **kwargs):
        verbose = getattr(settings, 'TEST_OUTPUT_VERBOSE', True)
        descriptions = getattr(settings, 'TEST_OUTPUT_DESCRIPTIONS', True)
        output = getattr(settings, 'TEST_OUTPUT_DIR', '.')
        return xmlrunner.XMLTestRunner(verbose=verbose, descriptions=descriptions, output=output).run(suite)

    def get_py_files(self, discovery_root):
        for root, _, files in os.walk(discovery_root):
            for filename in fnmatch.filter(files, "*.py"):
                yield os.path.join(root, filename)

    def build_test_case_path(self, class_and_method_names, file_path):
        project_path = re.sub(settings.ROOT_DIR, "", file_path)
        module_path = re.sub(".py", "", project_path[1:])
        test_case_path = re.sub(os.sep, '.', module_path)
        test_case_path += "." + '.'.join(class_and_method_names)
        return test_case_path

    def get_tests_one(self, app_label_parts, discovery_root):
        tests = []
        for file_path in self.get_py_files(discovery_root):
            with open(file_path) as python_file:
                data = python_file.read()

                class_and_method_names = app_label_parts[1:]
                if all([True if item in data else False for item in class_and_method_names]):
                    test_case_path = self.build_test_case_path(class_and_method_names, file_path)
                    try:
                        tests.append(defaultTestLoader.loadTestsFromName(test_case_path))
                    except AttributeError:
                        pass #This means a class name was found but wasn't a class
        return tests

    def get_tests_two(self, discovery_root, pattern):
        tests = defaultTestLoader.discover(
            discovery_root,
            pattern=pattern,
            top_level_dir=settings.ROOT_DIR,
        )

        return [tests]

    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        print test_labels
        print settings.ROOT_DIR
        suite = ut2.TestSuite()

        pattern = "*.py"

        tests = []
        for label in test_labels:
            if '.' in label:
                app_label_parts = label.split(".")
                discovery_root = self.get_discovery_root(app_label_parts[0])
                tests += self.get_tests_one(app_label_parts, discovery_root)
            else:
                discovery_root = self.get_discovery_root(label)
                tests += self.get_tests_two(discovery_root, pattern)

        suite.addTests(tests)
        return suite

    def get_discovery_root(self, label):
        try:
            models_module = get_app(label)
            discovery_root = os.path.dirname(models_module.__file__)
        except ImproperlyConfigured:
            discovery_root = os.path.join(settings.ROOT_DIR, label)

        return discovery_root

