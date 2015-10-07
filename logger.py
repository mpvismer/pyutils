'''
@author Mark Vismer

Some functions to simplify modularised system wide logging.

The python logging system is hierarchical with the parent.child.subchild notation

The root/parent logger is logging.getLogger() or logging.getLogger('')
Get children with logging.getLogger('child') or logging.getLogger('child.subchild')

Hence, logging.getLogger(__name__) works well.

This library simply provides an alternative get_logger() which helps to isolate
logging form third party libraries which also use logging.

'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import logging
import logging.handlers
from .string import *
import msvcrt
import _subprocess

_LOGGER_ROOT = None

#
#  see here: http://compgroups.net/comp.lang.python/rotatingfilehandler-fails/1694422
def duplicate(handle, inheritable=False):
    target_process = _subprocess.GetCurrentProcess()
    return _subprocess.DuplicateHandle(
        _subprocess.GetCurrentProcess(), handle, target_process,
        0, inheritable, _subprocess.DUPLICATE_SAME_ACCESS).Detach()

class NoInheritRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def _open(self):
        """
        Open the current base file with the (original) mode and encoding.
        """
        if self.encoding is None:
            stream = open(self.baseFilename, self.mode)
            newosf = duplicate(msvcrt.get_osfhandle(stream.fileno()), inheritable=False)
            newFD  = msvcrt.open_osfhandle(newosf,os.O_APPEND)
            newstream = os.fdopen(newFD,self.mode)
            stream.close()
            return newstream
        else:
            stream = codecs.open(self.baseFilename, self.mode, self.encoding)
        return stream


def configure_rotating_logging(filename, level=logging.DEBUG, maxBytes = 1024*100):
    '''
    Configures a rotating file logger to <filename>.
    '''
    logger = get_root_logger()

    if configure_rotating_logging.handler is None:
        configure_rotating_logging.handler = NoInheritRotatingFileHandler(filename, mode='w', maxBytes = maxBytes, backupCount=5, delay=True)
        handler = configure_rotating_logging.handler
        handler.doRollover()
        logger.warning('=============Logger created at %s' % str_localtime() )

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)-8s - %(message)s')

        handler.setFormatter(formatter)

        logger.addHandler(handler)

        logger.setLevel(level)

        def _exception_handler(exc_type, exc_value, exc_traceback):
            #logger.error("Unhandled exception:\n" + "".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
            logger.exception("Unhandled exception!")
            return _exception_handler.old_exception_handler(exc_type, exc_value, exc_traceback)
        _exception_handler.old_exception_handler = sys.excepthook
        sys.excepthook = _exception_handler
    else:
        logger.warning('Logger already configured!')

configure_rotating_logging.handler = None

def get_logger(name):
    '''
    A function to get the logger for the current module.
    '''
    rootLogger = get_root_logger()
    return rootLogger.getChild(name)


def get_root_logger(name=''):
    '''
    A function to get the top most logger.
    '''
    global _LOGGER_ROOT
    if _LOGGER_ROOT == None:
        _LOGGER_ROOT = logging.getLogger(name)
    return _LOGGER_ROOT

