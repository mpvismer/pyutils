'''
@author Mark Vismer
Holds the ShadowedStream class.
'''

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



