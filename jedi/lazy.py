"""Collects failed imports, hopefully due to mutual imports
in order to try import them later.
http://docs.python.org/2/faq/programming.html#how-can-i-have-modules-that-mutually-import-each-other

>>> from jedi.lazy import collect_import
>>> try:
...     from jedi import evaluate
... except ImportError:
...     collect_import(__file__, 'evaluate')
>>> try:
...     from jedi import evaluate_representation as er
... except ImportError:
...     collect_import(__file__, 'evaluate_representation', 'er')

# in other module later
>>> retry_import()
"""

import sys

def collect_import(destination, name, alias=None, mfrom='jedi'):
    assert not '.' in name
    if enabled:
        #import traceback
        #traceback.print_stack()
        #print
        imp_list.append((destination, name, alias, mfrom))
    else:
        raise ImportError("Module {0}.{1} import can not be imp_list because too late.".format(mfrom, name))

def retry_import():
    global enabled
    retries = 1
    for retry in range(retries):
        i = 0
        while i < len(imp_list):
            (destination, name, alias, mfrom) = imp_list[i]
            full_name = '.'.join((mfrom, name))
            try:
                module = sys.modules.get(full_name, __import__(full_name))
                setattr(sys.modules[destination], alias or name, module)
                imp_list.pop(i)
            except ImportError:
                if retry == retries - 1:  # last round
                    raise
                else:
                    i += 1
    enabled = False

enabled = True
imp_list = []
