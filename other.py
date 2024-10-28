'''
@author Mark Vismer
Functions related to string stuff
'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import threading
import math
import inspect
import types
import ctypes
import warnings

import timeit
import time
from time import strftime


def func_name():
    ''' Return the name of the current function (that called func_name().'''
    return inspect.stack()[1][3]


def parent_func_name():
    ''' Name of the parent function (parent of function that called parent_func_name()) '''
    return inspect.stack()[2][3]


def is_variable(x):
    '''
    Returns True if <x> is a variable of some kind - not a function etc.
    '''
    if not isinstance(x, types.BuiltinFunctionType) and\
        not isinstance(x, types.BuiltinMethodType) and\
        not isinstance(x, types.MemberDescriptorType) and\
        not isinstance(x, types.LambdaType) and\
        not isinstance(x, types.CodeType):
        return True
    else:
        return False


def prompt_yn(prompt):
    '''
    Asks the user a yes no question and does not return until either
    yes or no is responded.
    '''
    res = raw_input(promptStr)

    while len(res)!=1 or res[0].upper() not in ['Y','N']:
        res = raw_input("Enter 'y' or 'n': ")
    return res[0].upper()=='Y'


def arange(start, stop=None, step=1.0):
    '''
    Like range, but supports floats.
    '''

    if stop == None:
        stop = float(start)
        start = 0.0
    else:
        start = float(start)
    count = int(math.ceil((stop - start) / step))

    return [start + i * step for i in xrange(count)]


def enum_fields(cls, show_private=False):
    '''
    Returns the non-hidden attributes of a class.
    '''
    #for member in dir(cls):
    if hasattr(cls,'_fields_'):
        for member, _type in cls._fields_:
            if show_private or not member.startswith('_'):
                yield (member, getattr(cls ,member))
    elif issubclass(type(cls), dict):
        for member, val in cls.iteritems():
            if show_private or not member.startswith('_'):
                yield (member, val)
    else:
        for member, val in inspect.getmembers(cls):
            if not callable(val):
                if show_private or not member.startswith('_'):
                    yield (member, val)

def cls_fields(*args, **kwargs):
    warnings.warn('Obsolete use of cls_fields()')
    return enum_fields(*args, **kwargs)


def lookup_key(val, d, testfn=lambda x,y:bool(x==y)):
    '''
    Finds the keys in dictionay <d> which have value <val>.
    '''
    key = [key for key, value in d if testfn(value, stream)]


def array_flattern(data):
    '''
    Flatterns a multidemensional list of items into a single list.
    '''
    if hasattr(data[0], '__getitem__'):
        l = []
        for item in data:
            l.extend(array_flattern(item))
        return l
    else:
        return data


def array_unflattern(data, dimensions):
    '''
    Unflatterns a multidemensional list of items into a single list.
    '''
    offset = 0;
    if len(dimensions) > 1:
        l = []
        dimlen = 1
        for dim in dimensions[1:]:
            dimlen *= dim
        for idx in range(0, dimensions[0]):
            l.append(array_unflattern(data[offset:offset+dimlen], dimensions[1:]))
            offset += dimlen
        return l
    else:
        return data[:dimensions[0]]


def showstuff(data):
    '''
    Prints out all the members and their values
    '''
    for name in dir(data):
        if (name[0]!='_'):
            try:
                val = getattr(data,name)
                if len(val) > 1000:
                    print('  ' + name)
                else:
                    print('  ' + name + ' = ' + str(val))
            except:
                try:
                    print('  ' + name + ' = ' + str(val))
                except:
                    print('  ' + name + ' = <ERROR>')


def make_threadsafe(func):
    def decorator(*args, **kargs):
        decorator._lockobj.acquire()
        try:
            return func(*args, **kargs)
        finally:
            decorator._lockobj.release()
    decorator.lock = threading.Lock()
    return proxy


def dynamic_create(name, *args, **kargs):
    '''
    Dynamically imports the <name> module and then creates an instance of a class
    with the same name in that module.
    '''
    module = __import__(name)
    cls = module.__dict__[name]
    instance = cls(*args, **kargs)
    return instance


def shell_exec(command, duration_limit_seconds=0, directory=None):
    """
    Uses the subprocess module to run an external process piping stdout and stderr.
    """
    cwd = None

    if directory:
        cwd = os.getcwd()
        os.chdir(directory)

    process = subprocess.Popen(command, stdout=subprocess.PIPE,stderr=subprocess.PIPE)

    if duration_limit_seconds > 0:
        ticks = 0
        while (ticks < duration_limit_seconds) and (process.poll() == None):
            log.info('Waiting for end of process, tick %d....'%(ticks,))
            time.sleep(1)
            ticks += 1
        if process.poll() == None:
            log.error("Process execution time limit exceeded. Killing it....")
            try:
                process.kill()
            except:
                if (err.errno!=3) and (err.errno!=13):
                    raise

    if cwd:
        os.chdir(cwd)

    (output, error) = process.communicate()

    return (output, error)

def local_time_str():
    '''
    Returns a formatted string of the lcoal time.
    '''
    return strftime("%Y-%m-%d %H:%M:%S", time.localtime().getTime())


def svn_version(path = None):
    (out, err) =  shell_exec('svnversion', duration_limit_seconds = 15, directory = path)
    res = res.strip()
    if res:
        return res
    else:
        return out


def set_sigterm_handler(func):
    """
    Adds a handler for cleanup - usually for ctrl+c.
    """
    if os.name == "nt":
        import win32api
        win32api.SetConsoleCtrlHandler(func, True)
        log.info("Set windows handler to SIGTERM.")
    else:
        import signal
        signal.signal(signal.SIGTERM, func)


def execpyfile(filepath, **kwargs):
    '''
    This is a substitue for execfile().
    '''
    with open(filepath) as f:
        code = compile(f.read(), filepath, 'exec')
        #exec(code, **kwargs)


def buffer_info(obj):
    '''
    A routine to get the memory address and size of the underlying buffer of
    for the type supporting the buffer interface.
    '''
    cobj = ctypes.py_object(obj)
    address = ctypes.c_void_p()
    length = ctypes.c_ssize_t()
    ctypes.pythonapi.PyObject_AsReadBuffer(cobj, ctypes.byref(address), ctypes.byref(length))
    return address.value, length.value


def benchmark_it(func, repeat=3, number=1000):
    """
    Benchmark <func> by taking the shortest time of <repeat==3> test runs.
    """
    #print(s.ljust(20), end=" ")
    res = func()
    print(str(func) + ' took {:>5.0f} ms'.format(min(timeit.repeat(func,
                                          repeat=repeat,
                                          number=number)) * 1000))
    return res


class RedirectStdStreams(object):
    """
    Context manager to redirect stdout and stderr.
    """
    def __init__(self, stdout=None, stderr=None):
        self._stdout = stdout or sys.stdout
        self._stderr = stderr or sys.stderr

    def __enter__(self):
        self.old_stdout = sys.stdout
        self.old_stderr = sys.stderr
        self.old_stdout.flush()
        self.old_stderr.flush()
        sys.stdout = self._stdout
        sys.stderr = self._stderr

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush()
        self._stderr.flush()
        sys.stdout = self.old_stdout
        sys.stderr = self.old_stderr


class Mergem(object):
    '''
    A proxy class to manage operations and a list of the same object
    '''
    def __init__(self, *streams):
        super(ShadowedStream, self).__init__()
        self.streams = streams

    def __getattr__(self, name):
        for stream in self.streams:
            stream.__getattr__(name)

    def writeln(self, out=""):
        self.write(out)
        self.write("\n")

    def write(self, out):
        super(ShadowedStream, self).write(out)
        self.stream.write(out)



