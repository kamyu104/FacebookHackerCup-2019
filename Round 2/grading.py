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

    # min_discard[f][s]: min total discards for at most s context switches assuming first paper type is f
    min_discard = [[0 for _ in xrange(H+1)] for _ in xrange(2)]
    # dp[i][p][s]: min discards for at most s context switches in the first i papers in stack,
    #              with current paper type being p
    dp = [[[INF for _ in xrange(H+2)] for _ in xrange(2)] for _ in xrange(2)]  
    for f in xrange(2):
        for j in xrange(S):
            for p in xrange(2):
                for s in xrange(H+2):
                    dp[0][p][s] = INF
            for s in xrange(H+1):
                dp[0][f][s] = 0
            for i in xrange(H):
                p2 = P[i][j]
                for p in xrange(2):
                    for s in xrange(H+2):
                       dp[(i+1)%2][p][s] = INF
                for p in xrange(2):
                    for s in xrange(H+1):
                        d = dp[i%2][p][s]
                        dp[(i+1)%2][p2][s+int(p2 != p)] = min(dp[(i+1)%2][p2][s+int(p2 != p)], d)
                        dp[(i+1)%2][p][s] = min(dp[(i+1)%2][p][s], d+1)
            for s in xrange(H+1):
                min_discard[f][s] += min(dp[H%2][0][s], dp[H%2][1][s])
    
    # min_switch[d]: min total context switches for at most d discards
    min_switch = [INF for _ in xrange(S*H+1)]
    for f in xrange(2):
        for s in xrange(H+1):
            min_switch[min_discard[f][s]] = min(min_switch[min_discard[f][s]], s)
    for d in xrange(S*H):
        min_switch[d+1] = min(min_switch[d+1], min_switch[d])
    return " ".join(map(lambda d: str(min_switch[d]+1), L))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, grading())