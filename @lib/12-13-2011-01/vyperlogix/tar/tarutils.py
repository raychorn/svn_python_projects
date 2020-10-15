from vyperlogix.enum.Enum import Enum

class TarCompressionTypes(Enum):
    none = 0
    gz = 1
    bz2 = 2
    
__valid_compression_types__ = [
    TarCompressionTypes.gz,
    TarCompressionTypes.bz2
]

def tar_to_file_or_folder(source,dest,compression=TarCompressionTypes.none):
    import os
    import tarfile
    
    dest = os.path.abspath(dest)
    __compression__ = None
    __compression__ = ''
    if (compression in __valid_compression_types__):
        __compression__ = 'w:%s' % (compression.name)
    out = tarfile.TarFile.open(dest, __compression__)
    __arcname__ = os.path.basename(source)
    print 'DEBUG: %s --> %s --> %s' % (source,__arcname__,dest)
    out.add(source, arcname=__arcname__)
    out.close()
    
