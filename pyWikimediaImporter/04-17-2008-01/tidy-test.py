import tidy
options = dict(output_xhtml=1, add_xml_decl=1, indent=1, tidy_mark=0)
print tidy.parseString('<Html>Hello Tidy!', **options)
