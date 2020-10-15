def plural(noun):
    import re
    rule_tuple = (
    ('[ml]ouse$', '([ml])ouse$', '\\1ice'), 
    ('child$', 'child$', 'children'), 
    ('booth$', 'booth$', 'booths'), 
    ('foot$', 'foot$', 'feet'), 
    ('ooth$', 'ooth$', 'eeth'), 
    ('l[eo]af$', 'l([eo])af$', 'l\\1aves'), 
    ('sis$', 'sis$', 'ses'), 
    ('man$', 'man$', 'men'), 
    ('ife$', 'ife$', 'ives'), 
    ('eau$', 'eau$', 'eaux'), 
    ('lf$', 'lf$', 'lves'), 
    ('[sxz]$', '$', 'es'), 
    ('[^aeioudgkprt]h$', '$', 'es'), 
    ('(qu|[^aeiou])y$', 'y$', 'ies'), 
    ('$', '$', 's')
    )
    def regex_rules(rules=rule_tuple):
        for line in rules:
            pattern, search, replace = line
            yield lambda word: re.search(pattern, word) and re.sub(search, replace, word)
     
    for rule in regex_rules():
        result = rule(noun)
        if result: 
            return result
    return noun
