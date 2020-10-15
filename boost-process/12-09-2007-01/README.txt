boost.exe

--proclist             ... get process list.
--boost=process_name   ... boost this process by name.
--procWatcher          ... watches for the named process to boost.
--help                 ... displays this help text.
--verbose              ... output more stuff.

Typical usage:

This command performs the boost once and only once.

boost --boost=notepad.exe

This command performs the boost until the program is terminated.

boost --boost=notepad.exe --procWatcher

