'''
@author Mark Vismer
Collection of utilities.
'''

import warnings as _w
import traceback as _tb

import pyximport as _pyximport
_pyximport.install()
#  http://stackoverflow.com/questions/2817869/error-unable-to-find-vcvarsall-bat


#
#mingw_setup_args={'options': {'build_ext': {'compiler': 'mingw32'}}}
#import pyximport;
#pyximport.install(setup_args=mingw_setup_args)

from path import *
from string import *
from process import *
from other import *
from logger import *
from testhelper import *
from librarywrapper import *
try:
    from hardcore import *
except:
    _w.warn("Failed to import the cythonised hardcore utilities:\n" + _tb.format_exc())



