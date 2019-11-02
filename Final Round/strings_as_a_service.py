# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Final Round - Strings as a Service
# https://www.facebook.com/hackercup/problem/546199162815522/
#
# Time:  O(KlogK)
# Space: O(1)
#

from functools import partial

def check(K, x):
    return x*(x+1)//2 <= K

def binary_search_right(left, right, check):
    while left <= right:
        mid = left + (right-left)//2
        if not check(mid):
            right = mid-1
        else:
            left = mid+1
    return right

def strings_as_a_service():
    K = input()
    result = []
    while K > 0:
        l = binary_search_right(1, K, partial(check, K))
        K -= l*(l+1)//2
        result.append(chr(ord('A')+len(result)%3)*l)
    return "".join(result)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, strings_as_a_service())
