# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Qualification Round - Leapfrog: Ch. 1
# https://www.facebook.com/hackercup/problem/656203948152907/
#
# Time:  O(N)
# Space: O(1)
#

from collections import Counter

def leapfrog1():
    L = raw_input()
    count = Counter(L)
    return "Y" if 1 <= count['.'] <= count['B'] else "N"

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, leapfrog1())
