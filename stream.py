'''
@author Mark Vismer
Holds the streaming classes
'''

from StringIO import StringIO


class ShadowedStream(StringIO):
    '''
    A StringIO class the also echoes it's output to a provided output
    stream class.
    '''
    def __init__(self, stream):
        super(ShadowedStream, self).__init__()
        self.stream = stream

    def flush(self):
        super(ShadowedStream, self).flush()
        self.stream.flush()

    def writeln(self, out=""):
        self.write(out)
        self.write("\n")

    def write(self, out):
        super(ShadowedStream, self).write(out)
        self.stream.write(out)


class StreamMerger(object):
    '''
    Merges two output streams.
    '''
    def __init__(self, s1, s2):
        super(StreamMerger, self).__init__()
        self.s1 = s1
        self.s2 = s2

    def flush(self):
        self.s1.flush()
        self.s2.flush()

    def write(self, *args, **kwargs):
        self.s1.write(*args, **kwargs)
        self.s2.write(*args, **kwargs)

    def writeln(self, *args, **kwargs):
        self.s1.writeln(*args, **kwargs)
        self.s2.writeln(*args, **kwargs)
