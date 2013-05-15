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

__version__ = 0, 6, 0

import sys
from functools import partial

from . import settings
from .errors import NotFoundError

_api = None

def lazy_import_api_call(name, *args, **kwargs):
    global _api
    if not _api:
        sys.path.insert(0, __path__[0])
        import api
        sys.path.pop(0)
        _api = api
    return getattr(_api, name)(*args, **kwargs)

# These names are imported lazy and replaced later by jedi.api objects.
# If the __doc__ string is important, any of these objects should be used
# first or jedi.api should be imported.
Script = partial(lazy_import_api_call, 'Script')
set_debug_function = partial(lazy_import_api_call, 'set_debug_function')
_quick_complete = partial(lazy_import_api_call, '_quick_complete')
