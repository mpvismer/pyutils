'''
@author Mark Vismer
'''
import ctypes

class LibraryWrapper(object):
    '''
    A proxy class for loading a DLL that forces DLL unloading and clean
    up when the proxy class is no longer used.
    '''
    def __init__(self, name):
        self._handle = ctypes.windll.kernel32.LoadLibraryA(name)
        self._lib = ctypes.WinDLL(None, handle=self._handle)
        if hasattr(self._lib, 'DLLStart'):
            self._lib.DLLStart()

    def __safecleanup(self):
        if hasattr(self, '_lib'):
            try:
                if hasattr(self._lib, 'DLLStop'):
                    self._lib.DLLStop()
            finally:
                del self._lib
                ctypes.windll.kernel32.FreeLibrary(self._handle)

    def __getattr__(self, key):
        return getattr(self._lib,key)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.__safecleanup()
        return False

    def __del__(self):
        self.__safecleanup()

