#!/usr/bin/env python

import os
import sys
import argparse
from filecmp import dircmp
from diff_py import *
from diff_py.diff_helper import *


class check_files_dirs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        for file_or_dir in values:
            if not os.path.exists(file_or_dir):
                raise ValueError('{0} is not a valid path'.format(file_or_dir))
        setattr(namespace, self.dest, values)


class DiffRunner(object):

    def __init__(self):
        # argument parser
        parser = argparse.ArgumentParser(prog='diff_py', description='The simple diff tool which is written by Python.')
        format_group = parser.add_mutually_exclusive_group()
        format_group.add_argument('-c', '--context', action='store_true', dest='context', help='output 3 lines of copied context')
        format_group.add_argument('-C', type=int, metavar='NUM', action='store', dest='context_num', help='output NUM lines of copied context')
        format_group.add_argument('-u', '--unified', action='store_true', dest='unified', help='output 3 lines of unified context')
        format_group.add_argument('-U', type=int, metavar='NUM', action='store', dest='unified_num', help='output NUM lines of unified context')
        format_group.add_argument('-n', '--ndiff', action='store_true', dest='ndiff', help='output Python Differ-style context')
        format_group.add_argument('-H', '--html', metavar='OUTPUT_FILE', type=argparse.FileType('w'), action='store', dest='html', help='output HTML format context')
        parser.add_argument('FILES', action=check_files_dirs, nargs=2, help='can be "FILE1 FILE2", "DIR1 DIR2", "FILE DIR", or "DIR FILE"')
        self.version = '0.0.1'
        with open('diff_py' + os.sep + 'VERSION') as f:
            self.version = f.readline()
        parser.add_argument('-v', '--version', action='version', version='%(prog)s {version}'.format(version=self.version))

        # parser the argv
        self.options = parser.parse_args(sys.argv[1:])

        # run diff
        if self.options.html is not None:
            self.diff_html()
            self.options.html.close()
        elif self.options.ndiff:
            self.diff_text(type='ndiff')
        elif self.options.context or self.options.context_num is not None:
            if self.options.context_num is not None:
                self.diff_text(type='context', n=self.options.context_num)
            else:
                self.diff_text(type='context')
        elif self.options.unified or self.options.unified_num is not None:
            if self.options.unified_num is not None:
                self.diff_text(type='unified', n=self.options.unified_num)
            else:
                self.diff_text(type='unified')
        else:
            # run unified diff by default
            self.diff_text(type='unified')

    def diff_html(self):
        dh = HTMLDiffHelper(html_file=self.options.html)
        dh.diff(*self.options.FILES)
        dh.make_report()

    def diff_text(self, type='unified', n=3):
        dh = ConsoleDiffHelper(diff_type=type, n=n)
        dh.diff(*self.options.FILES)
        dh.make_report()


def main():
    DiffRunner()


if __name__ == '__main__':
    main()
