'''
Copyright (C) 2002 GDS Software

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License as
published by the Free Software Foundation; either version 2 of
the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the Free
Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
MA  02111-1307  USA

See http://www.gnu.org/licenses/licenses.html for more details.
'''
CommandDecodeError = "CommandDecode error"

class CommandDecode:
    '''This class can be used to identify that a command is from a set
    of commands.  The class will try to complete the command if a
    whole command is not typed in.  Run this file as a script to
    get an interactive demo.

    Here's an example of its use.  cmd_dict is a dictionary of all 
    the commands you want recognized (the commands are the keys).

    # We'll initialize so that the command's case is ignored
    ignore_case = 1
    id_cmd = CommandDecode(cmd_dict, ignore_case)
    while not finished:
        user_string = GetUserString()
        command = id_cmd.identify_cmd(user_string)
        if command == None:
            print "\"%s\" not recognized" % user_string
        elif type(command) == type(""):
            print "\"%s\" is unique command '%s'" % (user_string, command)
            finished = ExecuteCommand(command)
        else:
            print "\"%s\" is ambiguous" % user_string
            print "It matched the following commands:"
            for cmd in command:
                print "  ", cmd

    This shows that the identify_cmd() method will return 
    None if the user's string is not recognized, a single
    string if it is recognized as a unique command, and a
    list if it matched more than one possible command.
    '''

    def __init__(self, commands, ignore_case = 0):
        import string
        self.ignore_case = ignore_case
        self.commands    = commands
        if len(commands) < 1:
            raise CommandDecodeError, "dictionary must have > 0 elements"
        if type(commands) != type({}):
            raise CommandDecodeError, "must pass in dictionary"
        # Build index dictionary; each key is the first letter of the 
        # command and each element is a list of commands that have that
        # first letter.
        self.index = {}
        for cmd in self.commands.keys():
            first_char = cmd[0]
            if self.ignore_case:
                first_char = string.lower(first_char)
            if first_char not in self.index.keys():
                self.index[first_char] = []
            self.index[first_char].append(cmd)
        self.first_char_list = self.index.keys()


    def identify_cmd(self, user_string):
        import re, string
        if type(user_string) != type(""):
            raise CommandDecodeError, "must pass in a string"
        str = user_string
        if len(str) < 1:
            return None
        if self.ignore_case:
            str = string.lower(str)
        if self.commands.has_key(str):
            return user_string
        first_char = str[0]
        if first_char not in self.first_char_list:
            return None
        possible_commands = self.index[first_char]
        regexp = re.compile("^" + str)
        matches = []
        for cmd in possible_commands:
            if regexp.match(cmd):
                matches.append(cmd)
        if len(matches) == 0:
            return None
        if len(matches) == 1:
            return matches[0]
        return matches

if __name__ == "__main__":
    # Test the class; use some typical UNIX program names.
    d = { "ar" : "", "awk" : "", "banner" : "", "basename" : "", "bc" : "",
          "cal" : "", "cat" : "", "cc" : "", "chmod" : "", "cksum" : "",
          "clear" : "", "cmp" : "", "compress" : "", "cp" : "", "cpio" : "",
          "crypt" : "", "ctags" : "", "cut" : "", "date" : "", "dc" : "",
          "dd" : "", "df" : "", "diff" : "", "dirname" : "", "du" : "",
          "echo" : "", "ed" : "", "egrep" : "", "env" : "", "ex" : "",
          "expand" : "", "expr" : "", "false" : "", "fgrep" : "", "file" : "",
          "find" : "", "fmt" : "", "fold" : "", "getopt" : "", "grep" : "",
          "gzip" : "", "head" : "", "id" : "", "join" : "", "kill" : "",
          "ksh" : "", "ln" : "", "logname" : "", "ls" : "", "m4" : "",
          "mailx" : "", "make" : "", "man" : "", "mkdir" : "", "more" : "",
          "mt" : "", "mv" : "", "nl" : "", "nm" : "", "od" : "", "paste" : "",
          "patch" : "", "perl" : "", "pg" : "", "pr" : "", "printf" : "",
          "ps" : "", "pwd" : "", "rev" : "", "rm" : "", "rmdir" : "",
          "rsh" : "", "sed" : "", "sh" : "", "sleep" : "", "sort" : "",
          "spell" : "", "split" : "", "strings" : "", "strip" : "",
          "stty" : "", "sum" : "", "sync" : "", "tail" : "", "tar" : "",
          "tee" : "", "test" : "", "touch" : "", "tr" : "", "true" : "",
          "tsort" : "", "tty" : "", "uname" : "", "uncompress" : "",
          "unexpand" : "", "uniq" : "", "uudecode" : "", "uuencode" : "",
          "vi" : "", "wc" : "", "which" : "", "who" : "", "xargs" : "",
          "zcat" : ""
        }

    ignore_case = 1
    c = CommandDecode(d, ignore_case)
    print "Enter some commands, 'q' to quit:"
    cmd = raw_input()
    while cmd != "q":
        x = c.identify_cmd(cmd)
        if x == None:
            print "'%s' unrecognized" % cmd
        elif type(x) == type(""):
            print "'%s' was an exact match to '%s'" % (cmd, x)
        else:
            x.sort()
            print "'%s' is ambiguous:  %s" % (cmd, `x`)
        cmd = raw_input()
            
