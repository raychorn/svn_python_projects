# Use the Singleton to see if the class can be created more than once.
from singleton1 import Singleton
from singleton1 import test

s1 = Singleton()
print __name__, id(s1), s1.spam()

s2 = Singleton()
print __name__, id(s2), s2.spam()

test()