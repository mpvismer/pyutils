"""
@author: mark
Custom test result printer.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import os.path
from StringIO import StringIO
import unittest.result as result



class TextTestResultPlus(result.TestResult):
    """
    A test result class that can print formatted text results to a stream.
    """
    separator1 = '=' * 70
    separator2 = '-' * 70
    separator2short = separator2[:int(len(separator2)/2)]

    startTestSeparator = separator1

    def __init__(self, stream, descriptions, verbosity):
        super(TextTestResultPlus, self).__init__(stream, descriptions, verbosity)
        self.stream = stream
        self.verbosity = verbosity
        self.descriptions = descriptions

    def write(self, *args):
        sys.stdout.flush()
        sys.stderr.flush()
        self.stream.write(*args)
        self.stream.flush()

    def writeln(self, *args):
        sys.stdout.flush()
        sys.stderr.flush()
        self.stream.writeln(*args)
        self.stream.flush()

    def getDescription(self, test):
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return '\n'.join((str(test), doc_first_line))
        else:
            return str(test)

    def startTest(self, test):
        self.buffer = True
        if self.verbosity > 2:
            self.writeln(self.startTestSeparator)
            self.writeln(self.getDescription(test))
            self.writeln(self.separator2short)
            self.buffer = False
        elif self.verbosity > 1:
            self.write(self.getDescription(test))
            self.write(" ... ")
            self._setupStdout()
        super(TextTestResultPlus, self).startTest(test)

    def stopTest(self, test):
        super(TextTestResultPlus, self).stopTest(test)
        if self.verbosity > 2:
            self.writeln()
            #self.writeln()

    def addSuccess(self, test):
        super(TextTestResultPlus, self).addSuccess(test)
        if self.verbosity > 1:
            self.writeln("PASS")
        elif self.verbosity > 0:
            self.write('.')

    def addError(self, test, err):
        super(TextTestResultPlus, self).addError(test, err)
        #self._mirrorOutput = False
        if self.verbosity > 1:
            self.writeln("ERROR")
            if self.verbosity > 2:
                self.writeln(self.separator2short)
                self.writeln("%s" % self.errors[-1][1])
        elif self.verbosity > 0:
            self.write('E')

    def addFailure(self, test, err):
        super(TextTestResultPlus, self).addFailure(test, err)
        #self._mirrorOutput = False
        if self.verbosity > 2:
            self.writeln("FAIL")
            self.writeln(self.separator2short)
            self.writeln("%s" % self.failures[-1][1])
        else:
            if self.verbosity > 1:
                self.writeln("FAIL")
            elif self.verbosity > 0:
                self.write('F')

    def addSkip(self, test, reason):
        super(TextTestResultPlus, self).addSkip(test, reason)
        if self.verbosity > 1:
            self.writeln("SKIPPED: {0}".format(reason))
        elif self.verbosity > 0:
            self.write("s")

    def addExpectedFailure(self, test, err):
        super(TextTestResultPlus, self).addExpectedFailure(test, err)
        if self.verbosity > 1:
            self.writeln("expected failure")
        elif self.verbosity > 0:
            self.write("x")

    def addUnexpectedSuccess(self, test):
        super(TextTestResultPlus, self).addUnexpectedSuccess(test)
        if self.verbosity > 1:
            self.writeln("unexpected success")
        elif self.verbosity > 0:
            self.write("u")

    def printErrors(self):
        if (self.verbosity > 0) and (self.verbosity <= 2):
            self.writeln()
            self.printErrorList('ERROR', self.errors)
            self.printErrorList('FAIL', self.failures)
        else:
            pass

    def printErrorList(self, flavour, errors):
        for test, err in errors:
            self.writeln(self.separator1)
            self.writeln("%s: %s" % (flavour,self.getDescription(test)))
            self.writeln(self.separator2)
            self.writeln("%s" % err)



