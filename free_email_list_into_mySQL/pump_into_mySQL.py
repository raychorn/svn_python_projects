# Reads the Free Email List and pumps it into mySQL using SQLAlchemy Models.

from vyperlogix.misc import _utils
from vyperlogix.hash import lists

import sqlalchemy_models

def begin():
    print 'Begin Transaction...'
    try:
        sqlalchemy_models.agent.session.begin()
    finally:
        print sqlalchemy_models.agent.lastError
        print 'Ok !'

def commit():
    print 'Committing...'
    try:
        sqlalchemy_models.agent.commit()
    finally:
        print sqlalchemy_models.agent.lastError
        print 'Done !'

def main():
    d = lists.HashedLists2()
    fname = r'Z:\@myMagma\!Free EMail List\freemaildomains.txt'
    fIn = open(fname,'r')
    try:
        while (1):
            line = fIn.readline()
            if (line == ''):
                break
            line = line.strip()
            d[line] = line
    finally:
        fIn.close()
    items = []
    n = len(d)
    begin()
    for k,v in d.iteritems():
        print 'Inserting %d of %d.' % (len(items),n)
        sqlalchemy_models.insert_item(k)
        items.append(k)
    commit()

if (__name__ == '__main__'):
    main()
