
import os
os.chdir('pycoutput')

for i in os.listdir('.'):
    if i.endswith('.pyt'):
      f = open (i, 'r')
      for l in f:
          if l.find('\\wx\\') == -1:
              if l.find('Parameter (') > -1:
                  if l.find('(event)') > -1:
                      pass
                  else:
                      print l
              if l.find('No global') > -1:
                      print l
      f.close()
      #put to list and call unique
      #then output the list

os.chdir('..')
      