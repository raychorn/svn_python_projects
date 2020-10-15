import time
import pyui
import traceback

from twisted.internet import reactor
from twisted.internet import main
from twisted.internet.app import Application
from twisted.enterprise import adbapi, row, sqlreflector, util
from twisted.enterprise.dbcred import *

"""This is an example of using PyUI with Twisted Enterprise.

Info on Twisted can be found at http://www.twistedmatrix.com. This code worked
with Twisted verion 0.99r4.

For more Row Classes to experiment with see the row* files in doc/examples
directory of the Twisted Distribution.

Note that this test requires a Postgresql Relational database called
"sean" on the local machine , and the schema that is created by the file
twisted/enterprise/schem.sql in the Twisted distribution.

"""

def tick():
    main.addTimeout(tick, 0.5)

if __name__ == '__main__':

    # init pyui
    pyui.init(800,600, "p3d")

    # init db stuff
    dbpool = adbapi.ConnectionPool("pyPgSQL.PgSQL", database="sean", host="localhost", port=5432)
    reflector = sqlreflector.SQLReflector(dbpool, [IdentityRow, PerspectiveRow])
    reflector._transPopulateSchema(None)
    
    # make sure we can be shut down on windows.
    main.addTimeout(tick, 0.5)

    # create the boat frame
    w = pyui.boat.BoatReflectorFrame(reflector, 0,0,790, 570)

    # run the main loop
    last = 0
    frame = 0
    try:
        while pyui.update():
            pyui.draw()
            main.iterate()
            frame += 1
            now = time.time()
            if now - last > 2:
                print "FPS: ", int(frame/2)
                frame=0
                last=now
    except:
        print "ERROR:"
        traceback.print_exc()

    # done. quit now.
    pyui.quit()
    reactor.stop()
    main.iterate()
    main.iterate()
    main.shutDown()
    print "done Twisted shutdown"
