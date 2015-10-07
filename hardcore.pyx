"""
@author Mark Vismer
Some extra hardcore low-level functionality
"""


from cpython.buffer cimport PyBUF_SIMPLE
from cpython.buffer cimport Py_buffer
from cpython.buffer cimport PyObject_GetBuffer
from cpython.buffer cimport PyBuffer_Release
from cpython cimport PyLong_FromVoidPtr
from libc.string cimport memcpy as cmemcpy


def buffer_address(obj):
    '''
    This is just a generally awesome function which gets the memory address
    of the underlying data - it works for any object whcih supports the new
    buffer interface.
    '''
    cdef Py_buffer gotdata
    try:
        PyObject_GetBuffer(obj, &gotdata, PyBUF_SIMPLE)
        return PyLong_FromVoidPtr(gotdata.buf)
    finally:
        PyBuffer_Release(&gotdata)


def buffer_size(obj):
    '''
    This is just a generally awesome function which returns the size of the
    underlying data buffer - it works for any object which supports the new
    buffer interface.
    '''
    cdef Py_buffer gotdata
    try:
        PyObject_GetBuffer(obj, &gotdata, PyBUF_SIMPLE)
        return gotdata.len
    finally:
        PyBuffer_Release(&gotdata)


def buffercpy(dest, src, num_bytes=None, dest_offset=0, src_offset=0, ignore_readonly=False):
    '''
    This does a super fast copy between to objects supporting the buffer
    interface.
    '''
    cdef Py_buffer destbuf
    cdef Py_buffer srcbuf
    cdef void * destptr = NULL
    cdef void * srcptr = NULL
    copy_guess = None

    if type(dest)==int :
        destprt = <void*>dest
    else:
        try:
            PyObject_GetBuffer(dest, &destbuf, PyBUF_SIMPLE)
            if destbuf.readonly and not ignore_readonly :
                raise RuntimeError('"dest" is not writable.')
            if dest_offset > destbuf.len :
                raise RuntimeError('"dest_offset" greater than destination buffer.')
            if num_bytes is None :
                copy_guess = destbuf.len-dest_offset
            else:
                if destbuf.len-dest_offset < num_bytes :
                    raise RuntimeError('"dest" buffer too small.')
            destptr = destbuf.buf
        finally:
            PyBuffer_Release(&destbuf)

    if type(src)==int :
        srcptr = <void*>src
    else:
        try:
            PyObject_GetBuffer(src, &srcbuf, PyBUF_SIMPLE)
            if src_offset > srcbuf.len :
                raise RuntimeError('"src_offset" greater than source buffer.')
            if num_bytes is None:
                if copy_guess is None :
                    num_bytes = srcbuf.len-src_offset
                else:
                    num_bytes = min(srcbuf.len-src_offset, copy_guess)
            else:
                if srcbuf.len-src_offset < num_bytes :
                    raise RuntimeError('"src" buffer too small.')
            srcptr = srcbuf.buf
        finally:
            PyBuffer_Release(&srcbuf)

    cmemcpy(destptr, srcptr, num_bytes)
    return num_bytes




