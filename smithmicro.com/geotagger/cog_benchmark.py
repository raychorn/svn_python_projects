import tempfile, shutil, os, time

from cog import db, base

from vyperlogix.classes.SmartObject import SmartFuzzyObject

from vyperlogix.misc import ObjectTypeName

import uuid

isSmartFuzzyObject = lambda target:ObjectTypeName.typeClassName(target) == 'vyperlogix.classes.SmartObject.SmartFuzzyObject'

class Persistent(object):
    """Persistent object.

    Notice that we need to call base.setDirty(self, 1) when making
    changes, to ensure the new version of the object will get
    saved to disk.
    """

    __persistent__ = 1

    def __init__(self):
        self.id = str(id(self)) * 4
        self.l = []

    def addObject(self, o):
        self.l.append(o)
        base.setDirty(self, 1) # mark object as dirty

class Benchmarker:
    
    def __init__(self):
        self.path = path = tempfile.mktemp()
        os.mkdir(path)
        self.db = db.openDatabase(path)

    def populate(self, batchSize=1, iterations=100):
        """Add items to the database."""
        root = Persistent()
        # as long as we add a persistent object to registry,
        # all its children will automatically be persisted.
        self.db.registry.set("root", root)
        l = xrange(iterations)
        obj = root
        del root
        for i in l:
            for j in xrange(batchSize):
                aPersistent = Persistent()
                aPersistent.__dict__['id'] = str(uuid.uuid4())
                obj.addObject(aPersistent)
            obj = obj.l[-1]
            # we call this periodically to save objects to disk:
            self.db.do_periodic_work()
            # we call this periodically to remove unused objects from memory:
            self.db.swapout()
        # force a flush of objects to disk:
        self.db.flush()

    def iterate(self):
        """Iterate over all items in the database."""
        stack = []
        stack.append(self.db.registry.get("root"))
        while stack:
            parent = stack.pop()
            for child in parent.l:
                stack.append(child)
    
    def delete(self):
        """Delete items from the database."""
        # when removing an object from database, all its children
        # will be removed as well if they are no longer referenced
        # in any other way. circular references won't go away though.
        self.db.registry.delete("root")
        self.db.flush()
    
    def cleanup(self):
        self.db.close()
        shutil.rmtree(self.path)


def main():
    b = Benchmarker()
    start = time.time()
    print "BEGIN!"
    b.populate()
    print "Elapsed populate time:", time.time() - start
    print "OIDs added:", b.db.io.db.get("next_oid")
    start = time.time()
    b.iterate()
    print "Elapsed iterate time:", time.time() - start
    start = time.time()
    b.iterate()
    print "Elapsed iterate from memory time:", time.time() - start
    start = time.time()
    b.delete()
    print "Elapsed delete time:", time.time() - start
    b.cleanup()
    print "END!"


if __name__ == "__main__":
    main()
