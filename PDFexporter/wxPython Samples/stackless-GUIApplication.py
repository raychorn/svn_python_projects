import uthread9, traceback
from wxPython.wx import *
from portals.ui.mainframe import MainFrame
from portals.portalserror import *

class GUIApplication( wxPySimpleApp ):
    applicationClass = None # need to override in sub-classes
    mainFrameClass = MainFrame
    TITLE = "GUI Application"
    mainloopThread = None
    MUTech = None
    def __init__( self, dataFile=None, *arguments, **namedarguments ):
        self.databaseLocation = dataFile
        apply( wxPySimpleApp.__init__, (self,)+arguments,namedarguments )
        EVT_END_SESSION( self, self.OnEndSession )
    def OnEndSession( self, event ):
        '''Override to provide handling of end-of-session events'''
        if self.MUTech:
            try:
                self.MUTech.close()
            except:
                pass
        if self.mainFrame:
            try:
                self.mainFrame.Close()
            except:
                pass
    def OnInit(self):
        log( 'Loading Image Handlers', INITIALISATIONDEBUG )
        wxImage_AddHandler(wxJPEGHandler())
        wxImage_AddHandler(wxPNGHandler())
        wxImage_AddHandler(wxGIFHandler())
        log( 'Creating Application Window', INITIALISATIONDEBUG )
        self.mainFrame = self.mainFrameClass(
            NULL,
            title = self.TITLE,
        )
        self.mainFrame.Show(true)
        self.SetTopWindow(self.mainFrame)
        log( 'GUI Initialisation Complete', INITIALISATIONDEBUG )
        return true
    def StartMUTech( self ):
        '''
                Override this in subclasses to use your MUTech sub-class
                (using the default application class is not possible, as it's
                an abstract class that doesn't provide the needed functions)
                '''
        try:
            log( 'MUTech Startup', INITIALISATIONDEBUG )
            self.MUTech = self.applicationClass( guiApplication = self, dataFile= self.databaseLocation )
            self.MUTech.start()
            log( 'MUTech Startup Complete', INITIALISATIONDEBUG)
        except:
            log( 'MUTech Startup Failed with an Exception!', INITIALISATIONDEBUG )
            traceback.print_exc()
            self.OnExit( None )
    def OnExit( self, event ):
        if self.MUTech:
            try:
                self.MUTech.close()
            except:
                pass
        try:
            event.Skip()
        except: # catches cases where a non-event is used to signal this shutdown
            pass
        if self.mainloopThread:
            try:
                self.mainloopThread.exit()
                print 'exited mainloop thread'
            except:
                pass
        sys.exit( 0)
    def MainLoop(self):
        self.mainloopThread = uthread9.newResistent( self.__mainLoop
)
        uthread9.new( self.StartMUTech )
        if not uthread9.microThreadsRunning():
            uthread9.run()
    def __mainLoop( self ):
        try:
            while 1:
                # This inner loop will process any GUI events until there
                # are no more waiting.
                while self.Pending():
                    try:
                        uthread9.atomic(self.Dispatch )
                    except:
                        traceback.print_exc()
                # Send idle events to idle handlers.  You may want to throtle
                # this back a bit so there is not too much CPU time spent in
                # the idle handlers.  For this example, I'll just snooze a
                # little...
                uthread9.switchContext()
                try:
                    uthread9.atomic( self.ProcessIdle )
                except:
                    traceback.print_exc()
                uthread9.wait( 0.01 ) # hack!
        except:
            traceback.print_exc()
    def ProcessMessage (self, message):
        print "ProcessMessage received message", message
        return None

    def getBaseWindow ( self ):
        '''Abstract interface for getting the top window pointer from the
                GUIApplication (as opposed to a wxPython interface)'''
        return self.mainFrame

