""" Demonstration of basic CRUD operations in pyax

Demonstrates some CRUD operations, but there are other ways to make these calls as well

Demo is intended to be run against a developer edition org where the
Case object has not been modified significantly.
"""
import sys
from random import choice

from pyax.connection import Connection
from pyax.sobject.classfactory import ClassFactory

class TestData:
    @staticmethod
    def gen_cases(number=1):
        count = 0
        cases = []
        origin_list = ['Email', 'Phone', 'Web']
        status_list = ['New','Working','Escalated']
        priority_list = ['Low','Medium','High']
        desc_list = ['Hommina hommina hommina',
                     'Bippity boppity boo!',
                     'Tangible Bicycle Fruit',
                     'Psitticula Alexandri Fasciata',
                     'Far out in the uncharted backwaters']
        
        while len(cases) < number:
            subject = "!@#$%% Test Create Case Subject %s" %(len(cases) + 1)
            cases.append({'Subject': subject,
                          'Status': choice(status_list),
                          'Origin': choice(origin_list),
                          'Description': choice(desc_list),
                          'Priority': choice(priority_list)})
        return cases
        


def usage(msg=None):
    print "Usage: %s username password" %sys.argv[0]
    if msg is not None:
        print
        print msg
        pass
    print
    sys.exit(1)
    return

def single_object_demo(sfdc):
    """ Demonstrate operations on a single object """
    # Create the sObjectClass for the sObjectType we're going to work with
    Case = ClassFactory(sfdc, "Case")
    
    # populate a dictionary with the data to insert into a new Case, keyed by field names.
    # We'll use the TestData object to help with this later, but to illustrate the concept:
    my_case_data = {"Origin": "Web",
                    "Status": "New",
                    "Priority": "Low",
                    "Description": "This is the description of the test case",
                    "Subject": "!@#$% Test Case Subject 0"}
    
    # execute the create of this case in Salesforce.com
    print "Creating a single Case"
    my_save_result = Case.create(my_case_data)
    print
    
    # retrieve the object we just created using helper method which consumes the create method's SaveResult
    print "Retreiving the case we just created"
    print my_save_result
    my_case = Case.retrieveSaveResult(my_save_result)
    print type(my_case)
    print
    
    
    
    # access fields on the case as if it were a Dictionary. 
    print "Now that we've retrieved the newly created Case,\n\twe know its auto-generated number is %s" %my_case['CaseNumber']
    # grab the id for later
    my_case_id = my_case['Id']
    print "The object ID of that case is %s" %my_case_id
    print
    
    # update a field on the case
    print "Updating the case with a Priority of High and a Status of Working"
    my_case['Priority'] = "High"
    my_case['status'] = "Working" # the case of the field name shouldn't matter
    my_case['Type'] = "Other"
    my_case.update()
    print
    
    # re-fetching the case to see if the changes stuck
    print "Retrieving another instance of the Case from Salesforce" 
    my_case_2 = Case.retrieve(my_case_id) 
    if my_case['Priority'] == my_case_2['Priority']:
        print "Yup, the changes are committed in Salesforce now"
    else:
        print "Hrm, it doesn't look like the changes 'stuck.'"
        pass
    print
    
    print "try a refresh and check Type field"
    my_case.refresh()
    if my_case['Type'] == "Other":
        print "The updated Type field has the correct value!"
    print
    
    # since we have a Case instance handy (instead of just the case's ID), we can delete it by calling its delete method
    print "Deleting Case %s by calling its delete method" %my_case.get('CaseNumber')
    my_case.delete()
    print
    
    print "Now, try to retrieve the Case that we just deleted by its ID"
    my_case_3 = Case.retrieve(my_case_id)
    print "See - it's really gone: %s" %my_case_3
    
    return

def batch_demo(sfdc):
    """ Demonstrate operations on a batch of objects 
    
    A batch is a collection of like-typed sObjects. Queries and multiple ID
    retrieve operations return batches.
    """
    print "Getting the timestamp from the server - we'll use it a bit later"
    timestamp = sfdc.getServerTimestamp()
    print "\tCurrent server time is: %s" %timestamp
    print
    
    # Create the sObjectClass for the sObjectType we're going to work with
    Case = ClassFactory(sfdc, "Case")
    
    # create five cases at once.
    case_data_list = TestData.gen_cases(5)
    print "The source data for our cases is a %s of %s %s" \
    %(type(case_data_list), len(case_data_list), type(case_data_list[0]))
    print
    
    print "Create the list of objects in the same way as a single object"
    my_save_result = Case.create(case_data_list)
    print
    
    print "As before, retrieve the newly created objects with Case.retrieveSaveResult"
    my_cases = Case.retrieveSaveResult(my_save_result)
    print "This time, we got back a %s\n\tinstead of a single object" %type(my_cases)
    print 
    
    print "Sure, the retrieve worked, but how about querying for those objects"
    print "\t(using the timestamp we got earlier)" 
    qry = "SELECT Id, Subject, Priority FROM Case WHERE Subject LIKE '!@#$%%' AND CreatedDate >= %s" %timestamp
    # note: not a 100% guarantee we're going to get just those objects, but good enough to demonstrate usage.
    # no, it doesn't do prepared statements, but SOQL is only for querying anyhow, 
    # so potential damage is limited
    my_cases2 = sfdc.query(qry)
    print "query returned a %s with %s %s objects" %(type(my_cases2), 
                                                     len(my_cases2), 
                                                     my_cases2.type)
    
    print "Updating some of the Cases"
    # let's change values of some of the fields on some of the cases. 
    my_cases[0]['Priority'] = "Yikes" # use a priority value we know it's not set to
    my_cases[2]['Description'] = "I have changed the description of this case"
    # Now update changes to these objects in Salesforce.com
    my_cases.update()
    print
    
    print "Comparing one of the cases we retrieved against the same case that we queried"
    id = my_cases[0]['id']
    if my_cases[id]['Priority'] != my_cases2[id]['Priority']:
        print "Hey! They don't match. No surprise, though since the"
        print "\tqueried version doesn't know about the changes we've made"
        print "\tLet's refresh it and then try again"
        print
        my_cases2.refresh() # just a convenience method pyax provides
        if my_cases[id]['Priority'] == my_cases2[id]['Priority']:
            print "OK, now they match"
            print
        
    
    print "Deleting the batch of Cases in one fell swoop"
    my_cases.delete()
    
    return

def cleanup(sfdc):
    
    # query to get a batch of any outstanding test cases
    qry = "SELECT Id FROM Case WHERE Subject LIKE '!@#$%'"
    cleanup_cases = sfdc.query(qry)
    # note - cleanup_cases is an sObjectBatch!
    
    
    # now remove the batch
    cleanup_cases.delete()
    
    return
    

def main():
    if len(sys.argv) != 3:
        usage("Incorrect number of arguments")
    else:
        username = sys.argv[1]
        passwd = sys.argv[2]

    # log in to get an authenticated Connection object
    sfdc = Connection.connect(username, passwd)
        
    single_object_demo(sfdc)
    print
    batch_demo(sfdc)
    cleanup(sfdc)
    
    return

if __name__ == "__main__":
    main()
    pass
    