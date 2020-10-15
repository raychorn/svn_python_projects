import UserList
import os.path,glob,copy,shutil,sys,time


class Set:
    "a class to manage sets. Duplicates are not taken into account"
    def __init__(self,vals=[]):
        self.vals=copy.copy(vals)
    def get(self):
        return self.vals
    def set(self,newset):
        self.vals=copy.copy(newset)
    def join(self,newset):
        result=[]
        for elem in self.vals:
            try:
                newset.index(elem)
                result.append(elem)
            except ValueError:
                pass
        self.vals=result
    def merge(self,newset):
        for elem in newset:
            try:
                self.vals.index(elem)
            except ValueError:
                self.vals.append(elem)
    def reduce(self,newset):
        self.merge(newset)
        for elem in newset:
            try:
                self.vals.remove(elem)
            except:
                pass
            
class Log:
    def __init__(self,output=None):
        self.setoutput(output)
    def setoutput(self,output):
        if output:
	    self.output=output
	else:
	    self.output=sys.stdout
    def format(self,txt):
        tts=time.strftime('%c')
        return '%s : %s\n' % (tts,txt)
    def info(self,txt):
        self.output.write(self.format(txt))

class Pickling:
    def __getstate__(self):
	dict=self.__dict__.copy()
	for elem in dict.keys():
	    if elem[0]=="_":
	        del dict[elem]
	return dict
    def __setstate__(self,dict):
	self.__class__.__init__(self,**dict)


class DirDesc(Pickling):
    def __init__(self,dir,include_patt=['.*','*'],include_dirs=[],exclude_patt=[],exclude_dirs=[],log=Log()):
        self.dir=dir
        self.include_patt=include_patt
        self.include_dirs=include_dirs
        self.exclude_patt=exclude_patt
        self.exclude_dirs=exclude_dirs
	self._log=log
    def _get_files(self,dir,patt):
        if patt=='': return []
        files=glob.glob(os.path.join(dir,patt))
        result=[]
        for file in files:
            if os.path.isfile(file):
                result.append(file)
        return result

    def _analysis(self,args,dirname,fnames):
        "based on inlcude and exclude, return a list of files"
	self._log.info('Analyzing directory %s' % dirname)
        to_skip=0
	for included_dir in self.include_dirs:
            if included_dir!='' and dirname.find(included_dir)<0:
	       to_skip=1
	for excluded_dir in self.exclude_dirs:
            if excluded_dir!='' and dirname.find(excluded_dir)>=0:
               to_skip=1
	       self._log.info('   because of excluded rules, this directory will be skipped')
        if to_skip: return
        to_include=Set()
        for inc in self.include_patt:
            to_include.merge(self._get_files(dirname,inc))
        to_exclude=Set()
        for exc in self.exclude_patt:
            to_exclude.merge(self._get_files(dirname,exc))
        to_include.reduce(to_exclude.get())
        self._result.extend(to_include.get())
    def getfiles(self):
        self._result=[]
        os.path.walk(self.dir,self._analysis,None)
        reslist=[]
        dir=os.path.join(self.dir,'')
        for res in self._result:
            reslist.append(res.replace(dir,''))
        return (dir,reslist)
            

class Job:
    def __init__(self,local,remote,options={}):
        #local and remote must be DirDesc objects
        self.local=local
        self.remote=remote
        self.options=options
    def getoptions(self):
        return self.options
    def getlocalfiles(self):
        return self.local.getfiles()
    def getremotefiles(self):
        return self.remote.getfiles()
    def getlocalinputs(self):
        return {'dir':self.local.dir,'include_patt':self.local.include_patt,'include_dirs':self.local.include_dirs,'exclude_patt':self.local.exclude_patt,'exclude_dirs':self.local.exclude_dirs}
    def getremoteinputs(self):
        return {'dir':self.remote.dir,'include_patt':self.remote.include_patt,'include_dirs':self.remote.include_dirs,'exclude_patt':self.remote.exclude_patt,'exclude_dirs':self.remote.exclude_dirs}
    

#Jobs is a list of Job;you can do append, extend, insert, remove, get
class Jobs(UserList.UserList):
    def index(self,job):
        raise "not implemented"
    def reverse(self):
        raise "not implemented"
    def sort(self):
        raise "not implemented"
    

class FileComp:
    def __init__(self,jobcard,log=Log()):
        self.commands={}
        self.commands[0]=[]
        self.commands[1]=[]
        self.commands[2]=[]
        self.commands[3]=[]
        self.commands[4]=[]
	self.to_perform=[]
	self._log=log
        self.jobcard=jobcard
        (self.localdir,alllocalfiles)=jobcard.getlocalfiles()
        (self.remotedir,allremotefiles)=jobcard.getremotefiles()
        shared=Set(alllocalfiles)
        shared.join(allremotefiles)
        purelocalfiles=Set(alllocalfiles)
        purelocalfiles.reduce(shared.get())
        pureremotefiles=Set(allremotefiles)
        pureremotefiles.reduce(shared.get())
        self.purelocal=purelocalfiles.get()
        self.pureremote=pureremotefiles.get()
        self.shared=shared.get()
        self._log.info("Comparing directories via the methode : %s" % self.__class__.__name__ )
	self._log.info("Pure local %s " % purelocalfiles.get())
        self._log.info("Pure remote %s " % pureremotefiles.get())
        self._log.info("shared files %s " % shared.get())
    def analyze(self):
        #must return :
        # priority cmd           text
        #example:
        #   2     'copy a, b' 'copy to remote'
        #   2     'rm a'      'rmove from remote'
        #   3     'rmdir a'   'remove directory from remote'
        #   1     'mkdir a'   'make dir on local'
        #   0 None ''
        raise "Metha class. You should not call this one directly"
    def getresult(self):
        self.analyze()
        self.to_perform=[]
	for j in range(5):
	    if self.commands.has_key(j):
	        for card in self.commands[j]:
		    for file in card['list']:
                        self.to_perform.append([card['text'],file,card['from'],card['to'],card['cmd']])
	return self.to_perform
    def perform(self,actionslist=None):
        if actionslist==None:
	    actionslist=[1]*len(self.to_perform)
	i=0
	for rec in self.to_perform:
	    if actionslist[i]:
	        rec[4](rec[1],rec[2],rec[3])
	    i+=1


        
class DateComp(FileComp):
    def _copy(self,file,originaldir,destinationdir):
        fpath_dir=os.path.dirname(os.path.join(destinationdir,file))
        if not os.path.isdir(fpath_dir):
            os.makedirs(fpath_dir)
	self._log.info("copying %s from %s to %s" % (file, originaldir, destinationdir))
        shutil.copy2(os.path.join(originaldir,file),os.path.join(destinationdir,file))
	
    def _remove(self,file,dir,dummy):
	self._log.info("removing %s from %s" % (file, dir))
        os.remove(os.path.join(dir,file))
    def analyze(self):
        #validation of options (delete cannot be with local2remote AND remote2local
        #                      (max_delta cannot be <0
        if not self.jobcard.options.has_key('local2remote'):
            self.jobcard.options['local2remote']=1
        if not self.jobcard.options.has_key('remote2local'):
            self.jobcard.options['remote2local']=1
        if not self.jobcard.options.has_key('maxdelta'):
            self.jobcard.options['maxdelta']=0
        if not self.jobcard.options.has_key('delete'):
            self.jobcard.options['delete']=0
            
        self.commands[2]=[]
        if self.jobcard.options['local2remote']:
            local2remotelist=copy.copy(self.purelocal)
            for file in self.shared:
                fplfile=os.path.join(self.localdir,file)
                fprfile=os.path.join(self.remotedir,file)
                if (os.path.getmtime(fplfile)-os.path.getmtime(fprfile)) > self.jobcard.options['maxdelta']:
                    local2remotelist.append(file)
            if local2remotelist:
                self.commands[2].append({'cmd':self._copy,'from':self.localdir,'to':self.remotedir,'text':'copy to remote','list':local2remotelist})
		self._log.info(" to transfer to remote %s" % local2remotelist)
            if self.jobcard.options['delete']:
                self.commands[2].append({'cmd':self._remove,'from':self.remotedir,'to':'','text':'delete on remote','list':self.pureremote})
		self._log.info(" to deleted on remote %s" % self.pureremote)
                
        if self.jobcard.options['remote2local']:
            remote2locallist=copy.copy(self.pureremote)
            for file in self.shared:
                fplfile=os.path.join(self.localdir,file)
                fprfile=os.path.join(self.remotedir,file)
                if (os.path.getmtime(fprfile)-os.path.getmtime(fplfile)) > self.jobcard.options['maxdelta']:
                    remote2locallist.append(file)
            if remote2locallist:
                self.commands[2].append({'cmd':self._copy,'from':self.remotedir,'to':self.localdir,'text':'copy to local','list':remote2locallist})
		self._log.info(" to transfer to local %s" % remote2locallist)
            if self.jobcard.options['delete']:
                self.commands[2].append({'cmd':self._remove,'from':self.localdir,'to':'','text':'delete on local','list':self.purelocal})
		self._log.info(" to deleted on local %s" % self.pureremote)


        
class SizeComp(FileComp):
    def _copy(self,file,originaldir,destinationdir):
        fpath_dir=os.path.dirname(os.path.join(destinationdir,file))
        if not os.path.isdir(fpath_dir):
            os.makedirs(fpath_dir)
	self._log.info("copying %s from %s to %s" % (file, originaldir, destinationdir))
        shutil.copy2(os.path.join(originaldir,file),os.path.join(destinationdir,file))
	
    def _remove(self,file,dir,dummy):
	self._log.info("removing %s from %s" % (file, dir))
        os.remove(os.path.join(dir,file))
    def analyze(self):
        #validation of options (delete cannot be with local2remote AND remote2local
        #                      (max_delta cannot be <0
        if not self.jobcard.options.has_key('local2remote'):
            self.jobcard.options['local2remote']=1
        if not self.jobcard.options.has_key('remote2local'):
            self.jobcard.options['remote2local']=1
        if not self.jobcard.options.has_key('maxdelta'):
            self.jobcard.options['maxdelta']=0
        if not self.jobcard.options.has_key('delete'):
            self.jobcard.options['delete']=0
            
        self.commands[2]=[]
        if self.jobcard.options['local2remote']:
            local2remotelist=copy.copy(self.purelocal)
            for file in self.shared:
                fplfile=os.path.join(self.localdir,file)
                fprfile=os.path.join(self.remotedir,file)
                if (os.path.getsize(fplfile)-os.path.getsize(fprfile)) > self.jobcard.options['maxdelta']:
                    local2remotelist.append(file)
            if local2remotelist:
                self.commands[2].append({'cmd':self._copy,'from':self.localdir,'to':self.remotedir,'text':'copy to remote','list':local2remotelist})
		self._log.info(" transfer to remote %s" % local2remotelist)
            if self.jobcard.options['delete']:
                self.commands[2].append({'cmd':self._remove,'from':self.remotedir,'to':'','text':'delete on remote','list':self.pureremote})
		self._log.info(" deleted on remote %s" % self.pureremote)
                
        if self.jobcard.options['remote2local']:
            remote2locallist=copy.copy(self.pureremote)
            for file in self.shared:
                fplfile=os.path.join(self.localdir,file)
                fprfile=os.path.join(self.remotedir,file)
                if (os.path.getsize(fprfile)-os.path.getsize(fplfile)) > self.jobcard.options['maxdelta']:
                    remote2locallist.append(file)
            if remote2locallist:
                self.commands[2].append({'cmd':self._copy,'from':self.remotedir,'to':self.localdir,'text':'copy to local','list':remote2locallist})
		self._log.info(" transfer to local %s" % remote2locallist)
            if self.jobcard.options['delete']:
                self.commands[2].append({'cmd':self._remove,'from':self.localdir,'to':'','text':'delete on local','list':self.purelocal})
		self._log.info(" deleted on local %s" % self.pureremote)


