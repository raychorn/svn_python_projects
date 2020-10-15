# State Machine example Program

from StateDefn import *

class MyMachine(object):

    # Create Statedefn object for each state you need to keep track of.
    # the name passed to the constructor becomes a StateVar member of the current class.
    # i.e. if myObj is a MyMachine object, myObj.gstate maintains the current Gstate
    Gstate = StateTable("gstate")
    Tstate = StateTable("turtle")

    def __init__(self, name):
        # must call init method of class's StateTable object. to initialize state variable
        self.Gstate.initialize(self)
        self.Tstate.initialize(self)
        self.mname = name
        self.Acount = 0
        self.Bcount = 0
        self.Ccount = 0

    # Decorate the Event Handler virtual functions -note Gstate parameter
    @EventHandler(Gstate)
    def EventA( self ): pass
    @EventHandler(Gstate)
    def EventB( self ): pass
    @EventHandler(Gstate)
    def EventC( self, val ): pass

    @EventHandler(Tstate)
    def Toggle(self): pass


    # define methods to handle events.
    def _eventAHdlr1(self):
        print "State 1, event A"
        self.Acount += 1
    def _eventBHdlr1(self):
        print "State 1, event B"
        self.Bcount += 1
    def _eventCHdlr1(self, val):
        print "State 1, event C"
        self.Ccount += 3*val

    def _eventAHdlr2(self):
        print "State 2, event A"
        self.Acount += 10
        # here we brute force the Tstate to on, leave & enter functions called if state changes.
        # turtle is object's state variable for Tstate, comes from constructor argument
        self.turtle.SetState(self, self._t_on )
    def _eventBHdlr2(self):
        print "State 2, event B"
        self.Bcount += 10
    def _eventCHdlr2(self, val):
        print "State 2, event C"
        self.Ccount += 2*val

    def _eventAHdlr3(self):
        self.Acount += 100
        print "State 3, event A"
    def _eventBHdlr3(self):
        print "State 3, event B"
        self.Bcount += 100
        # we decide here we want to go to state 2, overrrides spec in state table below.
        # transition to NextState is made after the method exits.
        self.gstate.NextState = self._state2 
    def _eventCHdlr3(self, val):
        print "State 3, event C"
        self.Ccount += 5*val
    
    # Associate the handlers with a state. The first argument is a list of methods.
    # One method for each EventHandler decorated function of Gstate. Order of methods
    # in the list correspond to order in which the Event Handlers were declared.
    # Second arg is the name of the state.  Third argument is to be come a list of the
    # next states. 
    # The first state created becomes the initial state.
    _state1 = Gstate.State("One",  (_eventAHdlr1, _eventBHdlr1, _eventCHdlr1 ), 
                                      ("Two", "Three", None ))
    _state2 = Gstate.State("Two",  (_eventAHdlr2, _eventBHdlr2, _eventCHdlr2 ),
                                     ("Three",        None,          "One"))
    _state3 = Gstate.State("Three",(_eventAHdlr3, _eventBHdlr3, _eventCHdlr3 ),
                                 (None,         "One",         "Two"))


    # Declare a function that will be called when entering a new Gstate.
    # Can also declare a leave function using @OnLeaveFunction(Gstate)
    @OnEnterFunction(Gstate)
    def _enterGstate(self):
        print "entering state ", self.gstate.Name() , "of ", self.mname
    @OnLeaveFunction(Tstate)
    def _leaveTstate(self):
        print "leaving state ", self.turtle.Name() , "of ", self.mname


    def _toggleOn(self):
        print "Toggle On"

    def _toggleOff(self):
        print "Toggle Off"

    _t_off = Tstate.State( "Off", [_toggleOn],
                         ["On"     ])
    _t_on =  Tstate.State( "On",  [_toggleOff],
                          ["Off"])
