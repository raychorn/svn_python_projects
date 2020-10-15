import pefile

pe =  pefile.PE('eee.exe', fast_load=True)

#print 'pe=(%s)' % str(pe)

print 'pe.dump_info()=(%s)' % pe.dump_info()

#print [entry.id for entry in pe.DIRECTORY_ENTRY_RESOURCE.entries]

#print [entry.id for entry in pe.IMAGE_DIRECTORY_ENTRY_RESOURCE.entries]

#print [str(e) for entry in ]

if (False):
	for i in xrange(1000):
		try:
			print 'pe.parse_sections(%s)=(%s)' % (i,str(pe.parse_sections(i)))
		except Exception, details:
			print 'ERROR due to (%s)' % str(details)

if (False):
	print pe.parse_data_directories()
	
if (False):
	print pe.parse_resources_directory(0x29000)

res = pe.parse_resources_directory(0x29000)
for e in res.entries:
	print str(e)
	print 'e.id=(%s)' % e.id
	print 'e.name=(%s)' % e.name
	print 'e.struct=(%s)' % e.struct
	print 'e.struct.dump()=(%s)' % e.struct.dump()
	print 'e.directory=(%s)' % e.directory
	#print 'e.data=(%s)' % e.data
	
