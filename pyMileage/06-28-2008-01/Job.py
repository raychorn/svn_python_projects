from vyperlogix.classes.SmartObject import *

class Job(SmartObject):
    def __init__(self,args):
        '''args must be of type dict and must specify the name of each object {'cw':cw,'item':item}'''
        super(Job, self).__init__(args)
        
if (__name__ == '__main__'):
    from vyperlogix.misc import _utils
    d_job = {'company': 'Indotronix aka SBC', 'start-date': _utils.getFromSimpleDateStr('08/15/2004'), 'end-date': _utils.getFromSimpleDateStr('06/15/2005'), 'miles':33}
    d_job['company'] = 'Magma Design Automation'
    d_job['start-date'] = _utils.getFromSimpleDateStr('01/1/2008')
    d_job['end-date'] = _utils.getFromSimpleDateStr('04/17/2008')
    job = Job({'job':d_job})
    print str(job)
    print ''
    print '='*80
    print ''
    