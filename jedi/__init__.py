"""
Jedi is an autocompletion tool for Python that can be used in IDEs/editors.
Jedi works. Jedi is fast. It understands all of the basic Python syntax
elements including many builtin functions.

Additionaly, Jedi suports two different goto functions and has support for
renaming as well as Pydoc support and some other IDE features.

Jedi uses a very simple API to connect with IDE's. There's a reference
implementation as a `VIM-Plugin <http://github.com/davidhalter/jedi-vim>`_,
which uses Jedi's autocompletion.  I encourage you to use Jedi in your IDEs.
It's really easy. If there are any problems (also with licensing), just contact
me.

To give you a simple example how you can use the Jedi library, here is an
example for the autocompletion feature:

>>> import jedi
>>> source = '''
... import datetime
... datetime.da'''
>>> script = jedi.Script(source, 3, len('datetime.da'), 'example.py')
>>> script
<Script: 'example.py'>
>>> completions = script.completions()
>>> completions                                         #doctest: +ELLIPSIS
[<Completion: date>, <Completion: datetime>, ...]
>>> print(completions[0].complete)
te
>>> print(completions[0].name)
date

As you see Jedi is pretty simple and allows you to concentrate on writing a
good text editor, while still having very good IDE features for Python.
"""
import logging
import traceback
import sys
logging.basicConfig(filename='log')
logging.warn(__name__ + '\n' + ''.join(traceback.format_stack()))
if False:
    sys.stdin.close(); sys.stdin = open('/dev/pts/8', 'r');
    sys.stdout.close(); sys.stdout = open('/dev/pts/8', 'a');
    sys.stderr.close(); sys.stderr = open('/dev/pts/8', 'a');
    import pdb; pdb.set_trace()

__version__ = 0, 6, 0

import sys

# python imports are hell sometimes. Especially the combination of relative
# imports and circular imports... Just avoid it:
sys.path.insert(0, __path__[0])

#from .api import Script, NotFoundError, set_debug_function, _quick_complete
from . import settings

sys.path.pop(0)

def lazy_import_api():
    import api
    import jedi
    for name in ('Script', 'NotFoundError', 'set_debug_function', '_quick_complete'):
        setattr(sys.modules['jedi'], name, getattr(api, name))

logging.warn('end jedi/__init__')
logging.warn([k for k, v in sorted(sys.modules.items()) if v and 'jedi' in k])
