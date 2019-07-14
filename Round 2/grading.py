# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Round 2 - Bitstrings as a Service
# https://www.facebook.com/hackercup/problem/432000547357525/
#
# Time:  O(S * H^2)
# Space: O(S * H)
#
           
def grading():
    H, S, K = map(int, raw_input().strip().split())
    P = []
    for _ in xrange(H):
        P.append(map(lambda x: ord(x)-ord('A'), raw_input().strip()))
    L = map(int, raw_input().strip().split())
    INF = S*H-1

    minD = [[0 for _ in xrange(H+1)] for _ in xrange(2)]
    dp = [[[INF for _ in xrange(2)] for _ in xrange(H+2)] for _ in xrange(2)]
    for f in xrange(2):
        for j in xrange(S):
            for s in xrange(H+2):
                for p in xrange(2):
                    dp[0][s][p] = INF
            for s in xrange(H+1):
                dp[0][s][f] = 0
            for i in xrange(H):
                for s in xrange(H+2):
                    for p in xrange(2):
                       dp[(i+1)%2][s][p] = INF
                for s in xrange(H+1):
                    for p in xrange(2):
                        d, p2 = dp[i%2][s][p], P[i][j]
                        dp[(i+1)%2][s+int(p2 != p)][p2] = min(dp[(i+1)%2][s+int(p2 != p)][p2], d)
                        dp[(i+1)%2][s][p] = min(dp[(i+1)%2][s][p], d+1)
            for s in xrange(H+1):
                minD[f][s] += min(dp[H%2][s][0], dp[H%2][s][1])
    
    result = [INF for _ in xrange(S*H+1)]
    for f in xrange(2):
        for s in xrange(H+1):
            result[minD[f][s]] = min(result[minD[f][s]], s)
    for c in xrange(S*H):
        result[c+1] = min(result[c+1], result[c])
    return " ".join(map(lambda c: str(result[c]+1), L))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, grading())