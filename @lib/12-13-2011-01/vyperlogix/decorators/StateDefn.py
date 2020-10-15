#
# Support for State Machines.  ref - Design Patterns by GoF
#  Many of the methods in these classes get called behind the scenes. 
#
#  Notable exceptions are methods of the StateVar class. 
#
#  See example programs for how this module is intended to be used.
#
import exceptions

class StateMachineError( exceptions.Exception):
    def __init__(self, args = None):
        self.args = args

class StateVar(object):
    def __init__(self, initialState):
        self._currentState = initialState
        self.NextState = initialState            # publicly settable in an event handling routine.

    def SetState( self, owner, newState):
        '''
        Forces a state change to newState
        '''
        self.NextState = newState
        self.__toNextState( owner )

    def __toNextState(self, owner):
        '''
        The low-level state change function which calls leave state & enter state functions as 
        needed.

        LeaveState and EnterState functions are called as needed when state transitions.
        '''
        if not (self.NextState is self._currentState):
            if ( hasattr( self._currentState, "leave")):
                leave = self._currentState.leave
                leave(owner)
            elif (hasattr( self, "leave")):
                self.leave(owner)
            self._currentState =  self.NextState
            if ( hasattr( self._currentState, "enter")):
                enter = self._currentState.enter
                enter(owner)
            elif (hasattr( self, "enter")):
                self.enter(owner)

    def __fctn( self, funcName ):
        ''' 
        Returns the owning class's method for handling an event for the current state.
        This method not for public consumption.
        '''
        vf = self._currentState.GetFE(funcName)
        return vf

    def Name(self):
        '''
        Returns the current state name.
        '''
        return self._currentState.name

class STState(object):
    def __init__(self, stateName):
        self.name = stateName
        self.fctnDict = {}

    def SetEvents( self, eventList, eventHdlrList, nextStates ):
        dictionary = self.fctnDict
        if not nextStates:
            def setRow( event, method ):
                dictionary[ event ] = [method, None]
            map( setRow, eventList, eventHdlrList)
        else:
            def setRow2( event, method, nextState ):
                dictionary[ event ] = [method, nextState]
            map( setRow2, eventList, eventHdlrList, nextStates)
        self.fctnDict = dictionary

    def GetFE( self, fctnName):
        return self.fctnDict[fctnName]

    def MapNextStates(self, stateDict):
        ''' Changes second dict value from name of state to actual state '''
        for de in self.fctnDict.values():
            nextStateName = de[1]
            if nextStateName:
                if stateDict.has_key( nextStateName ):
                    de[1] = stateDict[nextStateName]
                else:
                    raise StateMachineError( 'Invalid Name for next state: %s' % nextStateName )


class StateTable(object):
    '''
    Magical class to define a state machine, with the help of several decorator functions
    which follow.
    '''
    def __init__( self, declname):
        self.machineVar=declname
        self._initialState = None
        self._stateList = {}
        self._eventList = []
        self.needInitialize = 1

    def initialize(self, parent):
        '''
        Initializes the parent class's state variable for this StateTable class. 
        Must call this method in the parent' object's __init__ method.  You can have
        Multiple state machines within a parent class. Call this method for each
        '''
        statevar= StateVar( self._initialState)
        parent.__dict__[self.machineVar] =statevar
        if (hasattr( self, "enter")):
            statevar.enter = self.enter
        if (hasattr( self, "leave")):
            statevar.leave = self.leave
        #Magic happens here - in the 'next state' table, translate names into state objects.
        if  self.needInitialize:
            for xstate in list(self._stateList.values()):
                xstate.MapNextStates( self._stateList )
            self.needInitialize = 0

    def DefState( self, eventHdlrList, name ) :
        '''
        This is used to define a state. the event handler list is a list of functions that
        are called for corresponding events. name is the name of the state.
        '''
        stateTableRow = STState(name)
        if ( len(eventHdlrList) != len(self._eventList)):
            raise StateMachineError('Mismatch between number of event handlers and the methods specified for the state.')

        stateTableRow.SetEvents( self._eventList, eventHdlrList, None )

        if self._initialState is None:
            self._initialState = stateTableRow
        self._stateList[name] = stateTableRow
        return stateTableRow

    def State( self, name, eventHdlrList, nextStates ) :
        stateTableRow = STState(name)
        if ( len(eventHdlrList) != len(self._eventList)):
            raise StateMachineError('Mismatch between number of event handlers and the methods specified for the state.')
        if ( (not nextStates is None) and len(nextStates) != len(self._eventList)):
            raise StateMachineError('Mismatch between number of event handlers and the next states specified for the state.')

        stateTableRow.SetEvents( self._eventList, eventHdlrList, nextStates )

        if self._initialState is None:
            self._initialState = stateTableRow
        self._stateList[name] = stateTableRow
        return stateTableRow

    def __AddEvHdlr( self, funcName ):
        '''
        Informs the class of an event handler to be added. We just need the name here. The
        function name will later be associated with one of the functions in a list when a state is defined.
        '''
        self._eventList.append( funcName )

# Decorator functions ... 
def EventHandler( stateClass ):
    '''
    Declare a method that handles a type of event.
    '''
    def Wrapper( func ):
        stateClass._StateTable__AddEvHdlr( func.__name__ )
        def ObjCall( self, *args, **keywords ):
            stateVar = self.__dict__[ stateClass.machineVar ]
            funky, nextState = stateVar._StateVar__fctn( func.__name__ )
            if not nextState is None:
                stateVar.NextState = nextState
            rv = funky(self, *args, **keywords )
            stateVar._StateVar__toNextState( self)
            return rv
        return ObjCall
    return Wrapper

def OnEnterFunction( stateClass ):
    '''
    Declare that this method should be called whenever a new state is entered.
    '''
    def Wrapper(func):
        stateClass.enter = func
        return func
    return Wrapper

def OnLeaveFunction( stateClass ):
    '''
    Declares that this method should be called whenever leaving a state.
    '''
    def Wrapper(func):
        stateClass.leave = func
        return func
    return Wrapper
