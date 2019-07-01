# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Round 1 - Class Treasurer
# https://www.facebook.com/hackercup/problem/2448144345414246/
#
# Time:  O(N)
# Space: O(N)
#

def class_treasurer():
    N, K = map(int, raw_input().strip().split())
    V = raw_input().strip()

    result = 0
    cnt = 0
    for i in reversed(xrange(len(V))):
        if V[i] == 'A':
            cnt = max(cnt-1, 0)
        else:
            cnt += 1
            if cnt > K:
                result = (result + POW[i]) % MOD
                cnt = max(cnt-2, 0)
    return result

MOD = 10**9+7
POW = [0]*10**6
POW[0] = 2
for i in xrange(1, len(POW)):
    POW[i] = POW[i-1]*2 % MOD
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, class_treasurer())
