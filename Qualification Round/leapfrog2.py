# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Qualification Round - Leapfrog: Ch. 2
# https://www.facebook.com/hackercup/problem/2426282194266338/
#
# Time:  O(N)
# Space: O(1)
#

from collections import Counter

def leapfrog2():
    L = raw_input()
    count = Counter(L)
    return "Y" if 1 <= count['.'] and \
                  (count['.'] <= count['B'] or 2 <= count['B']) \
               else "N"

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, leapfrog2())
