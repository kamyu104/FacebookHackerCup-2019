# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Round 3 - Light Show
# https://www.facebook.com/hackercup/problem/2272127393102980/
#
# Time:  O(N^2)
# Space: O(N)
#

def light_show():
    H, N = map(int, raw_input().strip().split())
    lasers = []
    for _ in xrange(N):
        lasers.append(map(int, raw_input().strip().split()))

    lasers.sort()
    dp = [0]*(N+1)
    for i in xrange(N):
        count = [0, 0]
        for j in xrange(i+1, N+1):
            count[lasers[j-1][1]-1] += 1
            c = max(count)
            dp[j] = max(dp[j], dp[i] + c*(c-1)//2)
    return dp[N]

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, light_show())