"""
@author Mark Vismer
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals



class Observable(object):
    '''
    Implements the Observer Pattern
    Ref: http://code.
    '''
    def __init__(self):
        '''
        Constructor
        '''
        super(Observable, self).__init__()
        self._observers = []

    def attach(self, observer):
        if not observer in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self):
        '''
        Calls each observer passing this observable as the first parameter.
        '''
        for observer in self._observers:
            try:
                observer(self)
            except:
                traceback.printexc()

