'''
@author Mark Vismer
Functions related to path stuff
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import fnmatch
import os
import errno

import logging

log = logging.getLogger(__name__)


def mkdir_p(path):
    '''
    Creates a path if it does not exists.
    '''
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def fix_sep(path):
    '''
    Fixes the path to use the correct directory separator for the current OS.
    '''
    path = path.replace('/',os.sep)
    path = path.replace('\\',os.sep)
    return path


def fix_filename(filename):
    """
    Removes invalid symbols etc from a filename string so it can actually
    be used as a filename.
    """
    chars = string.ascii_letters+string.digits+"()[]-_.~"
    return ''.join(c for c in name if c in chars)


def rglob(pattern, path=os.curdir):
    '''
    Like glob but recursive, only returns files.
    '''
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            matches.append(os.path.relpath(os.path.join(root, filename), path))
    return matches


def rglob_iter(pattern, path=os.curdir):
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, pattern):
            yield os.path.relpath(os.path.join(root, filename), path)


def read_file(filename, permissions = 'rb'):
    '''
    Reads the contents of a file as a blob.
    '''
    with open(filename, permissions) as f:
        data = f.read()
    return data


def get_filepath_change_image(path = os.curdir, exclude=None):
    files = rglob('*', path)
    files.sort()
    ret = []
    for filepath in files:
        if not fnmatch.fnmatch(filepath, exclude):
            ret.append( (filepath, os.path.getmtime(filename)) )
    return ret


