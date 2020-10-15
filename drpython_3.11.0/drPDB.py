import bdb
import sys

class drPdb(bdb.Bdb):
    """ Subclass of bdb that sends output to the prompt window """

    def __init__(self, drFrame):
        """ Set up for debugging """
        bdb.Bdb.__init__(self)

        self.save_stdout = sys.stdout
        self.save_stderr = sys.stderr

        self.lineno = None
        self.stack = []
        self.curindex = 0
        self.curframe = None

        self.drFrame = drFrame

    def start(self,debugfile,globals=None,locals=None):
        """ Start debugging """

        # redirect output to prompt window
        sys.stdout = sys.stderr = self.drFrame.txtPrompt
        cmd = 'execfile("' + debugfile + '")'
        self.run(cmd,globals,locals)

        # get output back to original
        sys.stdout = self.save_stdout
        sys.stderr = self.save_stderr

