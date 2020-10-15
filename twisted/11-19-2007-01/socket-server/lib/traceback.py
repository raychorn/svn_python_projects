"""Extract, format and print information about Python stack traces."""
import linecache
__all__ = [
def _print(file, str='', terminator='\n'):
def print_list(extracted_list, file=None):
    if not file:
    for filename, lineno, name, line in extracted_list:
def format_list(extracted_list):
    list = []
def print_tb(tb, limit=None, file=None):
    If 'limit' is omitted or None, all entries are printed.  If 'file'
    if not file:
def format_tb(tb, limit = None):
def extract_tb(tb, limit = None):
def print_exception(etype, value, tb, limit=None, file=None):
    This differs from print_tb() in the following ways: (1) if
def format_exception(etype, value, tb, limit = None):
    The arguments have the same meaning as the corresponding arguments
def format_exception_only(etype, value):
    The arguments are the exception type and value such as given by
def _some_str(value):
def print_exc(limit=None, file=None):
def print_last(limit=None, file=None):
def print_stack(f=None, limit=None, file=None):
    The optional 'f' argument can be used to specify an alternate
def format_stack(f=None, limit=None):
def extract_stack(f=None, limit = None):
    The return value has the same format as for extract_tb().  The
def tb_lineno(tb):
    Even works with -O on.
    c = tb.tb_frame.f_code