import compileall
import re
compileall.compile_dir('.', rx=re.compile('/[.]svn'), force=True)
