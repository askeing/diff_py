import os
import difflib
import logging
from filecmp import dircmp
from py.xml import html, raw


class BaseDiffHelper(object):
    def __init__(self):
        self.report = None
        # init logger
        logging.basicConfig()
        self.logger = logging.getLogger(__name__)

    def is_binary_file(self, file, chunk_size=1024):
        """
        Reference:
        http://git.savannah.gnu.org/cgit/diffutils.git/tree/src/io.c#n88
        http://git.kernel.org/cgit/git/git.git/tree/xdiff-interface.c?id=HEAD#n198
        """
        if not os.path.isfile(file):
            self.logger.error('%s:no such file or directory' % file)
            return False
        with open(file, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if '\0' in chunk:
                    return True
                if len(chunk) < chunk_size:
                    break
        return False

    @property
    def diff_file(self):
        raise NotImplementedError()

    @property
    def diff_dir(self):
        raise NotImplementedError()

    def diff(self, a, b):
        # a is file, b is file
        if os.path.isfile(a) and os.path.isfile(b):
            self.diff_file(a, b)
        # a is dir, b is dir
        elif os.path.isdir(a) and os.path.isdir(b):
            self.diff_dir(a, b)
        # a/b is file, b/a is dir
        elif (os.path.isfile(a) and os.path.isdir(b)) or (os.path.isdir(a) and os.path.isfile(b)):
            # a is file, b is dir.
            if os.path.isfile(a) and os.path.isdir(b):
                b_file = os.path.join(b, os.path.basename(a))
                if not os.path.exists(b_file):
                    self.logger.error('%s:no such file or directory' % b_file)
                else:
                    self.diff_file(a, b_file)
            # a is dir, b is file.
            elif os.path.isdir(a) and os.path.isfile(b):
                a_file = os.path.join(a, os.path.basename(b))
                if not os.path.exists(a_file):
                    self.logger.error('%s:no such file or directory' % a_file)
                else:
                    self.diff_file(a_file, b)
        else:
            if not os.path.exists(a):
                self.logger.error('%s:no such file or directory' % a)
            if not os.path.exists(b):
                self.logger.error('%s:no such file or directory' % b)
        return self.generate_diff_result()

    @property
    def generate_diff_result(self):
        raise NotImplementedError()


class HTMLDiffHelper(BaseDiffHelper):
    html_wrapcolumn = 80

    def __init__(self, html_file=None, contextual_differences=True):
        super(HTMLDiffHelper, self).__init__()
        # init logger
        self.logger = logging.getLogger(__name__)
        # setup the html_file
        if html_file is None:
            self.html_file = 'diff.html'
        else:
            self.html_file = html_file
        # loading the html settings
        self.div_container = html.div(class_='container')
        self.contextual_differences = contextual_differences

    def diff_file(self, file1, file2):
        html_diff = difflib.HtmlDiff(wrapcolumn=HTMLDiffHelper.html_wrapcolumn)
        with open(file1, 'r') as f1:
            with open(file2, 'r') as f2:
                table = html_diff.make_table(f1.readlines(), f2.readlines(), fromdesc=file1, todesc=file2, context=self.contextual_differences)
        self.div_container.append(raw(table))

    def diff_dir(self, dir1, dir2):
        dcmp = dircmp(dir1, dir2)
        # handle left dir1
        self.div_container.append(html.h2('Only in %s' % (dcmp.left,)))
        if len(dcmp.left_only) == 0:
            self.div_container.append(html.p('There is no file only in %s' % (dcmp.left,)))
        else:
            ul_left = html.ul()
            for name in dcmp.left_only:
                ul_left.append(html.li(name))
            self.div_container.append(ul_left)
        # handle right dir2
        self.div_container.append(html.h2('Only in %s' % (dcmp.right,)))
        if len(dcmp.right_only) == 0:
            self.div_container.append(html.p('There is no file only in %s' % (dcmp.right,)))
        else:
            ul_right = html.ul()
            for name in dcmp.right_only:
                ul_right.append(html.li(name))
            self.div_container.append(ul_right)
        # handle diff between dir1 and dir2
        self.div_container.append(html.h2('Diff between %s and %s' % (dcmp.left, dcmp.right)))
        if len(dcmp.diff_files) == 0:
            self.div_container.append(html.p('No Differences Found'))
        else:
            for name in dcmp.diff_files:
                if self.is_binary_file(os.path.join(dcmp.left, name), 1024):
                    self.div_container.append(
                        html.table(
                            html.thead(
                                html.tr(
                                    html.th(os.path.join(dcmp.left, name)),
                                    html.th(os.path.join(dcmp.right, name))
                                )
                            ),
                            html.tbody(
                                html.tr(
                                    html.td('Binary files differ')
                                )
                            ),
                            class_='table'
                        )
                    )
                else:
                    self.diff_file(os.path.join(dcmp.left, name), os.path.join(dcmp.right, name))
        # handle sub-dirs
        for sub_dcmp in dcmp.subdirs.values():
            diff_dir(sub_dcmp)

    def generate_diff_result(self):
        html_report_css = """
        h1 {
            text-align: center;
        }
        .container {
            width: 1170px;
            margin-left: auto;
            margin-right: auto;
        }
        table {
            font-family:Courier;
            border-collapse: collapse;
            border: 1px solid gray;
            width: 100%;
            margin-left: auto;
            margin-right: auto;
            margin-bottom: 20px;
        }
        table th {
            background-color: #e0e0e0;
            border: 1px solid gray;
        }
        table td {
            font-size: 12px;
        }
        /* For diff table */
        table.diff {
            font-family:Courier;
            border-collapse: collapse;
            border: 1px solid gray;
            width: 100%;
            margin-left: auto;
            margin-right: auto;
            margin-bottom: 20px;
        }
        .diff_header {
            background-color:#e0e0e0;
        }
        td.diff_header {
            text-align:right;
        }
        .diff_next {
            background-color:#c0c0c0;
        }
        .diff_add {
            background-color:#aaffaa;
        }
        .diff_chg {
            background-color:#ffff77;
        }
        .diff_sub {
            background-color:#ffaaaa;
        }
        """
        html_report = html.html(
            html.head(
                html.meta(name='Content-Type', value='text/html; charset=utf-8'),
                html.title('Diff Report'),
                html.style(
                    raw(html_report_css),
                    type='text/css'
                )
            ),
            html.body(
                html.h1('Diff Report'),
                self.div_container
            )
        )
        self.report = html_report
        return self.report

    def make_report(self):
        with open(self.html_file, 'w') as f:
            f.write(self.report.unicode(indent=2).encode('utf8'))


class ConsoleDiffHelper(BaseDiffHelper):
    diff_type_unified = 'unified'
    diff_type_context = 'context'
    diff_type_ndiff = 'ndiff'

    html_wrapcolumn = 80

    def __init__(self, diff_type='unified'):
        """
        The diff_type should be one of 'unified', 'context', and 'ndiff'.
        """
        super(ConsoleDiffHelper, self).__init__()
        # init logger
        self.logger = logging.getLogger(__name__)
        # init the result_list
        self.result_list = []
        # loading the diff_type
        if diff_type in [ConsoleDiffHelper.diff_type_unified, ConsoleDiffHelper.diff_type_context, ConsoleDiffHelper.diff_type_ndiff]:
            self.diff_type = diff_type
        else:
            self.diff_type = diff_type_unified

    def diff_file(self, file1, file2):
        with open(file1, 'r') as f1:
            with open(file2, 'r') as f2:
                if self.diff_type == ConsoleDiffHelper.diff_type_unified:
                    diff = difflib.unified_diff(f1.readlines(), f2.readlines(), fromfile=file1, tofile=file2)
                elif self.diff_type == ConsoleDiffHelper.diff_type_context:
                    diff = difflib.context_diff(f1.readlines(), f2.readlines(), fromfile=file1, tofile=file2)
                elif self.diff_type == ConsoleDiffHelper.diff_type_ndiff:
                    diff = difflib.ndiff(f1.readlines(), f2.readlines())
        diff_string = ''.join(diff)
        self.result_list.append('diff ' + file1 + ' ' + file2 + '\n' + diff_string)

    def diff_dir(self, dir1, dir2):
        dcmp = dircmp(dir1, dir2)
        # handle left dir1
        for name in dcmp.left_only:
            self.result_list.append('Only in %s: %s' % (dcmp.left, name))
        # handle right dir2
        for name in dcmp.right_only:
            self.result_list.append('Only in %s: %s' % (dcmp.right, name))
        # handle diff between dir1 and dir2
        for name in dcmp.diff_files:
            if self.is_binary_file(os.path.join(dcmp.left, name), 1024):
                self.result_list.append('Binary files %s and %s differ' % (os.path.join(dcmp.left, name), os.path.join(dcmp.right, name)))
            else:
                self.diff_file(os.path.join(dcmp.left, name), os.path.join(dcmp.right, name))
        # handle sub-dirs
        for sub_dcmp in dcmp.subdirs.values():
            diff_dir(sub_dcmp)

    def generate_diff_result(self):
        self.report = '\n'.join(self.result_list)
        return self.report

    def make_report(self):
        print(self.report)
