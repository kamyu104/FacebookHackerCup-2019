# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Final Round - Strings as a Service
# https://www.facebook.com/hackercup/problem/546199162815522/
#
# Time:  O(L^3)
# Space: O(K)
#

from itertools import imap

def strings_as_a_service():
    K = input()
    result = []
    for i, v in enumerate(LOOKUP[K]):
        result.append(chr(ord('A')+i)*v)
    return "".join(result)

def triangular_num(x):
    return x*(x+1)//2

MAX_L = 1000
MAX_K = 100000
LOOKUP = {}
for i in xrange(MAX_L):
    for j in xrange(i, MAX_L):
        for k in xrange(j, MAX_L-i-j+1):
            tmp = sum(imap(triangular_num, [i, j, k]))
            if tmp in LOOKUP or tmp > MAX_K:
                continue
            LOOKUP[tmp] = filter(lambda x: x != 0, [i, j, k])
assert(len(LOOKUP) == MAX_K+1)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, strings_as_a_service())
