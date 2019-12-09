# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Final Round-Cold Storage
# https://www.facebook.com/hackercup/problem/2506463429376063/
#
# Time:  O(N^2)
# Space: O(N^2)
#

def cold_storage():
    N, M = map(int, raw_input().strip().split())
    F = map(int, raw_input().strip().split())
    H = map(int, raw_input().strip().split())

    for i in xrange(N-1):
        for j in xrange(i+1, N):
            max_H[i][j] = max(max_H[i][j-1], H[j-1])

    for i in xrange(N):
        for j in xrange(i, N):
            dp[i][j][L] = dp[i][j][R] = INF
    dp[0][N-1][L] = dp[0][N-1][R] = 0
    for i in xrange(N):
        for j in reversed(xrange(i+1, N)):
            max_h = max(max_H[i][j], min(dp[i][j][L], dp[i][j][R]))
            dp[i][j][L] = min(dp[i][j][L], max_h)
            dp[i][j][R] = min(dp[i][j][R], max_h)
            dp[i+1][j][L] = min(dp[i+1][j][L], max(H[i], dp[i][j][L]+H[i]-F[i]))
            dp[i][j-1][R] = min(dp[i][j-1][R], max(H[j-1], dp[i][j][R]+H[j-1]-F[j]))
        dp[i][i][L] = dp[i][i][R] = min(dp[i][i][L], dp[i][i][R])

    result = []
    for _ in xrange(M):
        X, Y = map(int, raw_input().strip().split())
        X -= 1
        result.append('Y' if dp[X][X][L] <= Y+F[X] else 'N')
    return "".join(result)

MAX_N = 8000
MAX_H = 100000
INF = (MAX_N-1)*MAX_H  # float("inf") costs more time to allocate
# large memory allocation costs lots of time, thus make them as global variables
dp = [[[INF for _ in xrange(2)] for _ in xrange(MAX_N)] for _ in xrange(MAX_N)]
max_H = [[0 for _ in xrange(MAX_N)] for _ in xrange(MAX_N)]
L, R = range(2)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, cold_storage())
