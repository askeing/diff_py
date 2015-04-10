diff_py
=====
.. image:: https://travis-ci.org/askeing/diff_py.svg?branch=master
    :target: https://travis-ci.org/askeing/diff_py

The simple diff tool which is written by Python. The diff result can be printed in console or to html file.

Usage
-----
.. code-block:: bash

    usage: diff_py [-h] [-c | -C NUM | -u | -U NUM | -n | -H OUTPUT_FILE] [-v]
                   FILES FILES
    
    The simple diff tool which is written by Python.
    
    positional arguments:
      FILES                 can be "FILE1 FILE2", "DIR1 DIR2", "FILE DIR", or "DIR
                            FILE"
    
    optional arguments:
      -h, --help            show this help message and exit
      -c, --context         output 3 lines of copied context
      -C NUM                output NUM lines of copied context
      -u, --unified         output 3 lines of unified context
      -U NUM                output NUM lines of unified context
      -n, --ndiff           output Python Differ-style context
      -H OUTPUT_FILE, --html OUTPUT_FILE
                            output HTML format context
      -v, --version         show program's version number and exit
