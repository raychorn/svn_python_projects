#!/bin/bash

git init
find * -size +50M -type f -print >> .gitignore
git add -A
git commit -m "first commit"
git branch -M main
git remote add origin https://raychorn:f0fa4230f7cb33c0abe033385d3edf0ddf83bf0e@github.com/raychorn/svn_python_projects.git
git push -u origin main
