from vyperlogix.win.registry import get_program_files_registry_values

if (__name__ == '__main__'):
    # Find all the relevant keys.
    # Copy all the files from one folder to another.
    # Update the Registry once the files have been moved.
    targets = get_program_files_registry_values()
    for k,v in targets.asDict().iteritems():
        print '%s=%s' % (k,v)
    pass
