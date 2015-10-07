"""
@author: mark
Functions related to string stuff
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import time



def str_localtime(secs=None):
    '''
    Returns a string of the local time.
    '''
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(secs))


def str_gmtime(secs=None):
    '''
    Like str_localtime(), except UTC time.
    '''
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(secs))


def first_line(astring):
    '''
    Extracts the first line OF TEXT from a string.
    '''
    if (astring):
        astring = astring.lstrip('\r\n\t ')
        if astring:
            lines = astring.splitlines()
            return lines[0]
    return ''


def quote_it(path):
    '''
    Puts quotes around a path/string - useful when passing to the command line.
    '''
    return '"'+path+'"'


def split_lines(s):
    '''
    A slightly different version of str.
    '''
    char = '\n'
    split_list = s.split(char);
    ret = [ split + char for split in split_list[:-1]]
    if s.endswith(char):
        ret.append(split_list[-1]+char)
    else:
        ret.append(split_list[-1])
    return ret


def hex_it(arr):
    '''
    Convert a string, or byte array to a hex string.
    '''
    return ' '.join('%2X' % ord(x) for x in arr)


def unhex_it(hex_str, separator=' '):
    '''
    Reverse action of hex_it()
    '''
    l = [ chr(int(b, 16)) for b in hex_str.split(separator) ]
    return ''.join(l)


def isstr(x):
    '''
    Safely detects if <x> is a string type handling all possible unicode and
    string mix ups.
    '''
    return type(x) in [type(b''), type(u'')]



