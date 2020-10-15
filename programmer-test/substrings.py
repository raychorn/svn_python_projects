'''
#3
'''
def LongestCommonSubstring(S1, S2):
   '''This is the classic solution I did not code...'''
   M = [[0]*(1+len(S2)) for i in xrange(1+len(S1))]
   longest, x_longest = 0, 0
   for x in xrange(1,1+len(S1)):
      for y in xrange(1,1+len(S2)):
         if S1[x-1] == S2[y-1]:
            M[x][y] = M[x-1][y-1] + 1
            if M[x][y]>longest:
               longest = M[x][y]
               x_longest  = x
         else:
            M[x][y] = 0
   return S1[x_longest-longest: x_longest]

def compare(a, b):
   result = 0
   if (a < b):
      result = -1
   elif (a > b):
      result = 1
   return result

def _LongestCommonSubstring(S1, S2):
   '''This is my solution that seeks to find the longest possible common substrings common to both using brute force.'''
   l = []
   longest, shortest = (S1, S2)
   if (len(S1) < len(S2)):
      longest, shortest = (S2, S1)
   for n in xrange(1, len(shortest)+1):
      for i in xrange(0, len(shortest), n):
         ch = shortest[i:i+n]
         if (longest.find(ch) > -1):
            l.append(ch)
   d = {}
   for item in l:
      d[len(item)] = item
   keys = d.keys()
   keys.sort(compare)
   keys.reverse()
   _l_ = []
   for k in keys:
      _l_.append(d[k])
   return _l_[0]

if (__name__ == '__main__'):
   print LongestCommonSubstring('one', 'onetwotone')
   print _LongestCommonSubstring('one', 'onetwotone')
   print LongestCommonSubstring('onetwotone', 'one')
   print _LongestCommonSubstring('onetwotone', 'one')
   print LongestCommonSubstring('123213245678', '23213245')
   print _LongestCommonSubstring('123213245678', '23213245')
   