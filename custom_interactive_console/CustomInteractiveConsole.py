'''
B{Interactive Console}
a generic Interactive Console
it is used for the console userinterface of semanticSBML


exmaple usage
create a main menu::
	self._locals	= {
			'l':(self.listFiles,'List Models'),
			'i2s':(Id2Sbml_view,'ID -> SBML'),
			'd':(self.openDirectory,'Open Directory')
		}
	self._help="
	<<< semanticSBML main menu >>>
	l		list all loaded models
	d <DIR>	open all models in the directory (without arguments last used) 
	i2s		ID -> SBML Generate SBML files from Database Identifiers"

	cc = CustomConsole(self._locals,self._help).run()


a submenu can be created like this::

	class Id2Sbml_view(QWidget):
		def __init__(self):
			help="<<< ID -> SBML >>>
	e <ID1 ID2>	Enter a List of KEGG Reaction Identifiers
	q		exit this menu"
			cc = CustomConsole({'e':(self.slotNext_l,'insert list'),'q':(self.exit,'exit')},help).run('...')

also user input can be returned directly without connecting it to a function::
	input = CustomConsole().raw_input('Are you sure you want to do this? y/n:')
this function should be used instead of the native python raw_input since its input is captured and can be replayed

The main class of this module is the L{CustomConsole}. Each instance of the L{CustomConsole} requests the L{Singleton_datastore} which stores the command-queue the play-queue the history, the flags: exit, recording and verbose. 
'''
import code,pickle,os
from os.path import expanduser, join

class Singleton_datastore(object):
	''' 
	this is a singleton class for storing data that needs to be consistent throughout different instances of the L{CustomConsole}
	'''
    	__instance = None

    	def __new__(cls, *args, **kargs): 
        	if cls.__instance is None:
            		cls.__instance = Singleton_datastore.Local(*args, **kargs)
        	return cls.__instance        

    	class Local:
		def __init__(self):
			self.verbose=0
			self.recording=0
			self.exit=0
			self.cmdqueue=[]
			self.play_cmdqueue=[]
			cmdqueue_fn=join(expanduser('~'), '.semanticSBML', 'cmdqueue')
			if os.path.exists(cmdqueue_fn):
				self.cmdqueue = pickle.load(open(cmdqueue_fn,'r'))
			else:
				pickle.dump(self.cmdqueue,open(cmdqueue_fn,'w'))
			self.history=[]
			cmdhist_fn=join(expanduser('~'), '.semanticSBML', 'cmdhist')
			if os.path.exists(cmdhist_fn):
				self.history = pickle.load(open(cmdhist_fn,'r'))
			else:
				pickle.dump(self.history,open(cmdhist_fn,'w'))
			self.help='''The console provides the following commands:
help 		redisplay the currents menu extended commands explanation  
rec		start/stop recording commands to a command queue
prec		display recorded commands 
hist		display/execute commands from the command history

the command-queue and the history are stored presistendly
''' 

class CustomConsole:
	'''Create an interactive console for any applycation
	the console will list the available commands if the user inserted a wrong command
		- help: the command help will redisplay the help text
		- rec: start/stop recording commands
		- prec:	print command queue
		- play: run command queue
		- hist: print history
	'''

	def __init__(self,command_dict=None,help=None,verbose=-1):
		'''
		print the help text and get the singleton datastore L{Singleton_datastore}
		@param command_dictionary: mapping functions onto command strings 
		@type command_dictionary:{'c':(self.myfunction,'shortdescrition'),'q':(self.self.mysavesettings,'exit_and_run_fkt')}
		@param	help: help text listing and explaining all commands
		@type help: sting
		@param verbose: do not catch fatal exeptions created by the inserted functions, store in singleton class
		@type verbose: bool
		'''
		self._command_dict = command_dict
		self.on_exit_fkt=None
		self.exit=0#instance exit flag
            	self._local = Singleton_datastore()
		if verbose!=-1:#TODO this not good find a differntent solution
			self._local.verbose=verbose
		if help:
			self.help =help+'\ncommands: help, dir, rec, prec, play, hist, q, exit\nyou can use ctrl+D (win ctr+Z) to exit'
			print self.help
	def setCommandQueue(self,queue_str):
		'''
		put commands seperated by ";" on the commandqueue
		@param queue_str: commands as string 
		@type queue_str: str
		'''
		self._local.cmdqueue=queue_str.split(';')
		pickle.dump(self._local.cmdqueue,open(join(expanduser('~'), '.semanticSBML', 'cmdqueue'),'w'))

	def setOnExit(self,on_exit_fkt):
		'''
		set the exit function
		@param on_exit_fkt: the inserted function will be executed on exit of this custom console instance
		@type on_exit_fkt: function pointer
		'''
		self.on_exit_fkt=on_exit_fkt
	def play(self,prompt='>>>',b=0):
		'''this function acts like run but automatically loads the command queue into the play queue'''
		self._local.play_cmdqueue=self._local.cmdqueue
		self.run(prompt,b)

	def history(self,args):
		'''
		history functions
			- args empty: print history with counter before each command
			- args filled: execute commands from history though inserted counters
				counter ranges are allowed
				selected commands will be added to the play queue (not cmdqueue!)
		@param args:user inserted argumens (should be numbers)
		@type args: [str]
		'''
		#print args#DEBUG
		if not args:
			#print self._local.history
			out=''
			for i,c in enumerate(self._local.history):
				out+='['+str(i)+'] '+c+';'
			print out
			print 'you can execute commands from the history example:\nhist 0 5-7 9'
			return
		q=[]
		for a in args:
			if a.find('-')!=-1:
				a=a.split('-')
				q+=self._local.history[int(a[0]):int(a[1])]
			elif a:
				a=int(a)
				q+=[self._local.history[a]]
			
		print q
		try:
			if raw_input('execute the selected commands?(y/[n])').lower().strip()[0]=='y':
				self._local.play_cmdqueue=q
		except:
			pass
			
	def raw_input(self,prompt=None):#TODO test this function
		if prompt:
			self._prompt=prompt
			self._prompt0=prompt[0]
		while 1:
			#set the correct prompt (recording)
			if self._local.recording:
				self._prompt='r'+self._prompt[1:]
			elif self._prompt[0]!=self._prompt0:
				self._prompt=self._prompt0+self._prompt[1:]
			#get new command	
			try:
				cmd=''
				if self._local.play_cmdqueue:
					cmd=self._local.play_cmdqueue.pop(0)
					print '###executing### ',cmd
				else:
					try:
						cmd = raw_input(self._prompt).strip()
					except EOFError:
						print '<exit>'
						self._local.exit=1
				if cmd:#add command to the history
					if cmd.find('hist')==-1:
						if len(self._local.history)>20:
							self._local.history.pop(0)
						self._local.history+=[cmd]
						pickle.dump(self._local.history,open(join(expanduser('~'), '.semanticSBML', 'cmdhist'),'w'))
			#catch ctl+c
			except KeyboardInterrupt:
				print ''
				continue
			#if recording append it to the cmdqueue
			if self._local.recording:
				self._local.cmdqueue.append(cmd)
			return cmd

	def run(self,prompt='>>>',b=0):
		'''start the command loop

		if a command is mapped onto 'q' it will be executed before exiting the command loop

		a command queue can be recorded, it will be serialized into a file on the hd for new sessions

		@param prompt: prompt string the user will see (similar sys.ps1)
		@type prompt: string (min length 3)
		@param	b: if it is set to true the command loop will only run once
		@type b: bool'''
		#console = code.InteractiveConsole({})#TODO can I use the interactive console? code completion
		self._prompt=prompt
		self._prompt0=prompt[0]
		if len(self._prompt)<3:
			print 'prompt must be at least 3 characters long'
			return
		while 1:
			#check if exit flag is set, if the on exit function retruns True exit
			if self._local.exit or self.exit:
				if self.on_exit_fkt:
					if apply(self.on_exit_fkt,): 
						break
					else:
						self._local.exit=0
						self.exit=0
				else:
					break
			#get input from user or play queue
			cmd=self.raw_input()
			#cut command into parts and store only the main command in cmd
			cmd_args=cmd.split()
			if cmd:
				cmd=cmd_args[0].lower()
			else:
				continue
			if cmd =='help':
				print self.help
			elif cmd == 'rec':
				if not self._local.recording:
					print 'starting to record'
					self._local.cmdqueue=[]
					self._local.recording=1
				else:
					print 'stopped recording'
					self._local.cmdqueue=self._local.cmdqueue[:-1]
					pickle.dump(self._local.cmdqueue,open(join(expanduser('~'), '.semanticSBML', 'cmdqueue'),'w'))
					self._local.recording=0
			#show recorded commands
			elif cmd=='prec':
				print self._local.cmdqueue
			#play recorded commands, by pushing them on the play queue
			elif cmd=='play':
				self._local.play_cmdqueue=self._local.cmdqueue
			elif cmd=='dir':
				print self._local.help
			#history function, will be extended
			elif cmd=='hist':
				self.history(cmd_args[1:])
			#execute the command if it in the cmd dict
			elif self._command_dict.has_key(cmd):
				#print self._local.verbose
				#if verbose is on the function will crash the whole program and thus show the stacktrace
				if self._local.verbose:
					apply(self._command_dict[cmd][0],cmd_args[1:])
				else:
					try:
						apply(self._command_dict[cmd][0],cmd_args[1:])
					except TypeError ,e:#catches wrong programm input
						print e
						continue
					except:
						print ':-O the function crashed, please check your input (or run in verbose mode)'
						continue
				if b or cmd == 'q':
					self.exit=1
			elif cmd == 'quit' or cmd=='q':
				self.exit=1
			elif cmd == 'exit':
				self._local.exit=1
			else:
				print 'unknown command, the available commands are:'
				for c,(fkt,desc) in self._command_dict.iteritems():
					print '%-20s%s'%(c,desc)
				print '\n type help for more information'

if (__name__ == '__main__'):
	CustomConsole().raw_input('Are you sure you want to do this? y/n:')
	
