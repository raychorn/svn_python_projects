from vyperlogix.tar import tarutils

if (__name__ == '__main__'):
    tarutils.tar_to_file_or_folder(r'C:\@vm2','./test.tar.gz',compression=tarutils.TarCompressionTypes.gz)

    print 'Done !!'

