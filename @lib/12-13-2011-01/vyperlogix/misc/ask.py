def askList(question, aList, default=None):
    """Ask the user the given question and their answer.
    
    "question" is a string that is presented to the user.
    "aList" is a list of items from which the user must choose by entering the number of that item.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of a number of the index of the selected item.
    """
    import sys
    
    if (not str(default).isdigit()) or (default < 1) or (default > len(aList)):
        default = 1

    choices = ['%d' % (i) for i in xrange(0,len(aList)+1)]
    while 1:
        i = 1
        for item in aList:
            sys.stdout.write('%d :: %s' % (i,item))
        sys.stdout.write('\n%s %s' % (question,aList[default-1]))
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in choices:
            return aList[int(choice)]
        else:
            _str = '%s or %s' % (','.join(choices[0:-1]),choices[-1])
            sys.stdout.write('Please repond with one of "%s".\n' % (_str))

def askYesNo(question, default="yes"):
    """Ask the user the given question and their answer.
    
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    import sys
    
    valid = {"yes":"yes", "y":"yes", "ye":"yes", "1":"yes", "true":"yes",
             "no":"no",   "n":"no",  "0":"no",   "false":"no"}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise Error("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            y_list = []
            n_list = []
            for k,v in valid.iteritems():
                if (v.lower() == 'yes'):
                    y_list.append(k)
                elif (v.lower() == 'no'):
                    n_list.append(k)
            y_list = list(set(y_list))
            y_str = '%s or %s' % (','.join(y_list[0:-1]),y_list[-1])
            n_list = list(set(n_list))
            n_str = '%s or %s' % (','.join(y_list[0:-1]),y_list[-1])
            sys.stdout.write('Please repond with "%s" or "%s".\n' % (y_str,n_str))
