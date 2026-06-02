import os, sys
_lib_path = os.path.join(os.path.dirname(__file__), 'lib')
if os.path.isdir(_lib_path):
    sys.path.insert(0, _lib_path)

from . import models
