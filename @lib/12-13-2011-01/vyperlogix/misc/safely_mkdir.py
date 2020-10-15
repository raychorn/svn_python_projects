def safely_mkdir(fpath='.',dirname='logs'):
    import os
    
    _log_path = os.path.abspath(os.sep.join([fpath,dirname]))
    if (not os.path.exists(_log_path)):
        os.mkdir(_log_path)
    return _log_path

