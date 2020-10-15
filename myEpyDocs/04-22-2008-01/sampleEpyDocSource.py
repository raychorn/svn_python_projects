""" 
Process the creation od Interested partied list (default) and  
 
add them to the CR. 
 
""" 
 
sfUrl = 'https://na1.salesforce.com' 
 
import pprint 
import sys 
import textwrap 
import datetime 
from optparse import OptionParser 
 
from sfMagma import * 
from sfConstant import * 
from sfUtil import * 
 
class CaseWatcherList(SFMagmaTool): 
     
    logname = 'CaseWatherList' 
     
    def getCheckSince(self): 
        if (sys.platform == 'win32'): 
            tmp_root = os.sep.join([os.environ['TMP'],'processDates']) 
            if (os.path.exists(tmp_root) == False): 
                os.mkdir(tmp_root) 
        else: 
            tmp_root = '/home/sfscript/tmp/processDates' 
        filename = 'LastCheckedCRNotificationDate'   
        checksince = None 
                       
        curDirPath = os.getcwd() 
        tmpDirPath = tmp_root 
        os.chdir(tmpDirPath)        
         
        tmpPath = os.path.join(tmp_root,filename) 
        if os.path.isfile(tmpPath): 
            curFile=open(tmpPath, "rb", 0) 
            lines = [l for l in curFile.readlines() if len(l.strip()) > 0] 
            checksince = None 
            if (len(lines) > 0): 
                checksince = lines[-1] 
            curFile.close() 
            os.remove(tmpPath)             
         
        try: 
            #open file stream 
            #secsAgo=60*60*24 
            newfilename=os.path.join(tmp_root,filename) 
            file = open(newfilename, 'a') 
            file.write(timeStamp()) 
            file.close() 
        except IOError: 
            msg= "There was an error writing to %s" %filename 
            self.setLog(msg, 'warn') 
            pass 
         
        if checksince in [None,'',""]: 
            fromSecs = time.time() 
            fromSecs = datetime.datetime.fromtimestamp(fromSecs) 
            diff = datetime.timedelta(hours=-1) 
            previousHour=fromSecs + diff             
            previousHour=time.mktime(previousHour.timetuple())                     
            preHourStr = self.getAsDateTimeStr(previousHour)             
            checksince=preHourStr 
             
        os.chdir(curDirPath) 
        self.createNewNotifyObj(checksince) 
                               
        return      
     
    def createNewNotifyObj(self,checksince): 
         
        if checksince not in [None,'',""]:              
            soql=" Select OwnerId, CreatedDate, Id, LastModifiedDate,  Name  from Case_Watcher__c where LastModifiedDate > %s" %checksince 
            logPrint('soql=[%s]' % soql) 
                         
            ret1 = self.query('Case_Watcher__c', soql=soql)          
            logPrint('ret1=[%s]' % ret1) 
             
            if ret1  in BAD_INFO_LIST: 
                msg ="Could not find any records for Case_Watcher__c Object" 
                logPrint('msg=[%s]' % msg) 
                print msg 
                self.setLog(msg, 'warn') 
            else:                           
                for buildLink in ret1:    
                    userId = buildLink.get('OwnerId')                                                         
                    ipId = buildLink.get('Id')                                         
                    if userId not in BAD_INFO_LIST: 
                        self.createUserContact(userId,ipId) 
                    continue 
                pass     
        else: 
            msg = "No query need to be performed" 
            logPrint('msg=[%s]' % msg) 
            self.setLog(msg) 
                   
        return 
     
    def createUserContact(self,userId,ipId):                 
        idList = [] 
        idList.append(userId)          
        fields = ('Id','Email', 'FirstName','IsActive','LastName','User_Contact_Id__c') 
        ret = self.retrieve(idList, 'User', fieldList=fields) 
                 
        if ret in BAD_INFO_LIST:                         
            msg = "Could not find any records for User Id: %s" %teamId 
            logPrint('msg=[%s]' % msg) 
            print msg 
            self.setLog(msg, 'warn') 
            pass                 
        else: 
            for cont in ret: 
                contactId = cont.get('User_Contact_Id__c') 
                email = cont.get('Email')                  
                self.createCRNotificationObj(email,contactId,ipId,'User Alias','False') 
            pass 
        return  
     
    def getContactEmail(self, contactId):        
        email=None 
        idList = [] 
        idList.append(contactId)          
        fields = ('Id','Email') 
        ret = self.retrieve(idList, 'Contact', fieldList=fields) 
                 
        if ret in BAD_INFO_LIST:                         
            msg = "Could not find any records for Product team Id: %s" %teamId 
            logPrint('msg=[%s]' % msg) 
            print msg 
            self.setLog(msg, 'warn') 
            pass                 
        else: 
            for cont in ret: 
                email=cont.get('Email')                                                  
            pass 
         
        return email 
     
    def createCRNotificationObj(self,email,contactId,ipId, name,isEmailAlias):         
        newEmail=email 
        soql="Select Email__c, Id, Case_Watcher__c, Name from Case_Watcher_List__c   where Case_Watcher__c= '%s'" %ipId                 
        logPrint('soql=[%s]' % soql) 
        ret = self.query('Case_Watcher_List__c', soql=soql)         
        logPrint('ret=[%s]' % ret) 
        if ret in BAD_INFO_LIST:                         
            msg ="Could not find any Case_Watcher__c Object"             
            logPrint('msg=[%s]' % msg) 
            print msg 
            self.setLog(msg, 'warn')                         
            data = [{'Email__c':newEmail,'Contact__c':contactId,'Case_Watcher__c':ipId,'Name':name,'Alias_Email__c':isEmailAlias}]                         
            contactObjRes = self.create('Case_Watcher_List__c', data)               
        else: 
            emailExist=False 
            for ip in ret:                 
                existEmail=ip.get('Email__c')                 
                if newEmail==existEmail: 
                    msg= "Record with the same email Id alraedy exist:  %s" %existEmail 
                    logPrint('msg=[%s]' % msg) 
                    self.setLog(msg) 
                    emailExist=True 
                    self.setLog(msg) 
                    break 
                continue 
             
            if not emailExist:                 
                data = [{'Email__c':newEmail, 'Contact__c':contactId,'Case_Watcher__c':ipId,'Name':name}]                 
                contactObjRes = self.create('Case_Watcher_List__c', data)    
                pass         
            pass 
                 
        return 
     
    def getContactId(self,userId): 
        contId=None         
        idList = [] 
        idList.append(userId) 
         
        if userId is not None: 
            fields = ('Id', 'User_Contact_Id__c', 'Email', 'IsActive') 
            res = self.retrieve(idList, 'User', fieldList=fields) 
 
            if res not in BAD_INFO_LIST: 
                for user in res: 
                    contId = user.get('User_Contact_Id__c')                     
                    continue 
                pass 
            pass 
        return contId     
     
def main():     
    n=CaseWatcherList() 
    n.getCheckSince() 
 
if __name__ == "__main__": 
    main() 
 
