if (__name__ == '__main__'):
    import os
    import uuid
    
    from views.models import Environments

    envs = ['TESTMAN', 'PRETEST', 'PROD', 'VZWDEV', 'VZWSTAGE' ,'WMSVZWSTAGE', 'WMSVZWPREPROD', 'WMSVZWPROD']
    for env in envs:
        count = Environments.objects.filter(name=env).count()
        if (count == 0):
            _uuid = uuid.uuid4()
            print 'INFO :: Adding environment name of "%s" (%s).' % (env,_uuid)
            e = Environments(name=env,uuid=_uuid)
            e.save()
            print 'Done !'
        else:
            print 'INFO :: There are %d record%s for the environment name of "%s".' % (count,'s' if ( (count == 0) or (count > 1) ) else '',env)
        
    from views.models import Protocols

    protos = [['http','http://'],['https','https://']]
    for proto in protos:
        count = Protocols.objects.filter(name=proto[0]).count()
        if (count == 0):
            _uuid = uuid.uuid4()
            print 'INFO :: Adding protocol name of "%s" (%s).' % (proto,_uuid)
            p = Protocols(name=proto[0],value=proto[-1],uuid=_uuid)
            p.save()
            print 'Done !'
        else:
            print 'INFO :: There are %d record%s for the protocol name of "%s".' % (count,'s' if ( (count == 0) or (count > 1) ) else '',proto)
        
