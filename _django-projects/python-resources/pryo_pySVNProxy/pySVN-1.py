import pysvn

fpath = r'Z:\@myFiles\@Python+near-by.info\Python'

client = pysvn.Client()
entry = client.info(fpath)
print 'Url:',entry.url

entry_list = client.ls(fpath)

print entry_list
