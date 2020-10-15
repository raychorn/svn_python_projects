def strip_tags(in_text,make_carriage_returns='\n'):
    """Description: Removes all HTML/XML-like tags from the input text.
	Inputs: s --> string of text
	Outputs: text string without the tags

	# doctest unit testing framework

	>>> test_text = "Keep this Text <remove><me /> KEEP </remove> 123"
	>>> strip_ml_tags(test_text)
	'Keep this Text  KEEP  123'
        
        make_carriage_returns defaults to '\n' however make this '' to by-pass this behavior.
	"""
    # convert in_text to a mutable object (e.g. list)
    if (len(make_carriage_returns) > 0):
        in_text = in_text.replace('<br>',make_carriage_returns).replace('<br/>',make_carriage_returns)
    s_list = list(in_text)
    i,j = 0,0

    while i < len(s_list):
        # iterate until a left-angle bracket is found
        if s_list[i] == '<':
            while s_list[i] != '>':
                # pop everything from the the left-angle bracket until the right-angle bracket
                s_list.pop(i)

            # pops the right-angle bracket, too
            s_list.pop(i)
        else:
            i=i+1

    # convert the list back into text
    join_char=''
    return join_char.join(s_list)

