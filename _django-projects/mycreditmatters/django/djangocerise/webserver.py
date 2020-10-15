#!/usr/bin/env python
#
# Copyright 2006-2008, Loic d'Anterroches
#
# Released under the Python license.
#
# Daemon main loop based on Juergen Hermanns
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66012
# downloaded from: http://homepage.hispeed.ch/py430/python/daemon.py
# 

from vyperlogix.django.cherryPy import djangocerise

if __name__ == "__main__":
    # --conf myprojectconf --host 127.0.0.1:8888
    run = djangocerise.Runner()
    run.main()

