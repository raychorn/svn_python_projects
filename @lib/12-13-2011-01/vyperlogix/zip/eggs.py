def unEgg(module_name,egg_path,top):
    '''module_name is the name of the module like paramiko,
    egg_path is the fully qualified path to the egg,
    top is the folder where the un-egg should be placed.
    '''
    import os, sys, zipfile
    from vyperlogix.misc import _utils
    
    _dirname = ''
    if (os.path.exists(egg_path)):
        dirname = top
        _dirname = _utils.safely_mkdir(fpath=dirname,dirname=module_name)
        z = zipfile.ZipFile(egg_path,'r')
        _files = z.filelist
        for f in _files:
            bytes = z.read(f.filename)
            _f = os.sep.join([_dirname,f.filename])
            _utils.safely_mkdir(fpath=os.path.dirname(_f),dirname='')
            _utils.writeFileFrom(_f,bytes,mode='wb')
        z.close()
    return _dirname
