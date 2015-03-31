import os
import shutil
import tempfile
import unittest

from py.xml import html
from diff_py import *


class DiffHelperTest(unittest.TestCase):
    def setUp(self):
        self.file_a1 = tempfile.NamedTemporaryFile()
        self.file_a1.write('A')
        self.file_a1.flush()

        self.file_a2 = tempfile.NamedTemporaryFile()
        self.file_a2.write('A')
        self.file_a2.flush()

        self.file_b = tempfile.NamedTemporaryFile()
        self.file_b.write('B')
        self.file_b.flush()

        self.file_name_a = 'FILE_A'
        self.file_name_b = 'FILE_B'
        self.dir_a1 = tempfile.mkdtemp()
        open(os.path.join(self.dir_a1, self.file_name_a), 'w').close()
        
        self.dir_a2 = tempfile.mkdtemp()
        open(os.path.join(self.dir_a2, self.file_name_a), 'w').close()

        self.dir_b = tempfile.mkdtemp()
        open(os.path.join(self.dir_b, self.file_name_a), 'w').close()
        open(os.path.join(self.dir_b, self.file_name_b), 'w').close()

    def tearDown(self):
        self.file_a1.close()
        self.file_a2.close()
        self.file_b.close()
        try:
            shutil.rmtree(self.dir_a1)
            shutil.rmtree(self.dir_a2)
            shutil.rmtree(self.dir_b)
        except OSError as exc:
            if exc.errno != errno.ENOENT:
                raise

    def test_console_diff_file_equal(self):
        dh = ConsoleDiffHelper()
        result = dh.diff(self.file_a1.name, self.file_a2.name)
        expected = 'diff {0} {1}\n'.format(self.file_a1.name, self.file_a2.name)
        self.assertEqual(expected, result)

    def test_console_diff_file_not_equal(self):
        dh = ConsoleDiffHelper()
        result = dh.diff(self.file_a1.name, self.file_b.name)
        expected = 'diff {0} {1}\n--- {0}\n+++ {1}\n@@ -1 +1 @@\n-A+B'.format(self.file_a1.name, self.file_b.name)
        self.assertEqual(expected, result)

    def test_console_diff_dir_equal(self):
        dh = ConsoleDiffHelper()
        result = dh.diff(self.dir_a1, self.dir_a2)
        expected = ''
        self.assertEqual(expected, result)

    def test_console_diff_dir_not_equal(self):
        dh = ConsoleDiffHelper()
        result = dh.diff(self.dir_a1, self.dir_b)
        expected = 'Only in {0}: {1}'.format(self.dir_b, self.file_name_b)
        self.assertEqual(expected, result)

    def test_html_diff_file_equal(self):
        dh = HTMLDiffHelper()
        result = dh.diff(self.file_a1.name, self.file_a2.name)
        expected_substring = 'No Differences Found'
        self.assertIsInstance(result, html.html, 'The result is not html object.')
        self.assertTrue(expected_substring in result.unicode(), 'The result does not have "{}" string.'.format(expected_substring))

    def test_html_diff_file_not_equal(self):
        dh = HTMLDiffHelper()
        result = dh.diff(self.file_a1.name, self.file_b.name)
        expected_substring = 'No Differences Found'
        self.assertIsInstance(result, html.html, 'The result is not html object.')
        self.assertFalse(expected_substring in result.unicode(), 'The result have "{}" string.'.format(expected_substring))

    def test_html_diff_dir_not_equal(self):
        dh = HTMLDiffHelper()
        result = dh.diff(self.dir_a1, self.dir_b)
        expected_re = r'<h2>Only in {0}</h2>\s*<ul>\s*<li>{1}</li>\s*</ul>'.format(self.dir_b, self.file_name_b)
        self.assertIsInstance(result, html.html, 'The result is not html object.')
        self.assertRegexpMatches(result.unicode(), expected_re)


if __name__ == '__main__':
    unittest.main()
