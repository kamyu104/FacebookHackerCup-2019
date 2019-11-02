# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Final Round - Khajiit
# https://www.facebook.com/hackercup/problem/536189700557596/
#
# Time:  O(N * M)
# Space: O(1)
#

def khajiit():
    N, M = map(int, raw_input().strip().split())
    X = raw_input().strip()
    Y = raw_input().strip()
    result = 0
    for i in xrange(N):
        has_A, needs_A = 0, 0
        for j in reversed(xrange(M)):
            has_A += int(X[i*M+1+j] == 'A')
            needs_A += int(Y[i*M+1+j] == 'A')
            result += abs(has_A-needs_A)
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, khajiit())
