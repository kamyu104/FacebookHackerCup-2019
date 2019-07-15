# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Round 2 - Seafood
# https://www.facebook.com/hackercup/problem/404425766835121/
#
# Time:  O(NlogN)
# Space: O(N)
#

from bisect import bisect_right

def seafood():
    N = input()
    G = [[None for _ in xrange(N)] for _ in xrange(2)]
    for i in xrange(2):
        G[i][0], G[i][1], A, rightmost_harder_R, C, D = map(int, raw_input().strip().split())
        for j in xrange(2, N):
            G[i][j] = (A*G[i][j-2] + rightmost_harder_R*G[i][j-1] + C) % D + 1
    O = raw_input().strip()

    P = sorted((G[0][i], O[i], G[1][i]) for i in xrange(N))
    C = []
    for i in xrange(N):
        if P[i][1] == 'C':
            C.append(i)
    ascending_R_H_from_right = []
    for i in reversed(xrange(C[-1])):
        if (P[i][1] == 'R') and \
           (not ascending_R_H_from_right or (ascending_R_H_from_right[-1][0] < P[i][2])):
            ascending_R_H_from_right.append((P[i][2], P[i][0]))
    rightmost_harder_R = [-1]*len(C)  # rightmost_harder_R[i] = j:
                                      # rightmost rock j s.t. ascending_R_H_from_right[j] > P[C[i]][2]
    for i in xrange(len(C)):
        j = bisect_right(ascending_R_H_from_right, (P[C[i]][2], float("inf")))
        if j == len(ascending_R_H_from_right):
            break
        rightmost_harder_R[i] = ascending_R_H_from_right[j][1]

    suffix_min_R = [float("inf")]*(len(C)+1)
    suffix_max_H = [float("-inf")]*(len(C)+1)
    for i in reversed(xrange(len(C))):
        suffix_min_R[i] = min(suffix_min_R[i+1], rightmost_harder_R[i])
        suffix_max_H[i] = max(suffix_max_H[i+1], P[C[i]][2])
    ascending_R_H_after_rightmost_C = []
    for i in xrange(C[-1]+1, N):
        if not ascending_R_H_after_rightmost_C or \
           ascending_R_H_after_rightmost_C[-1][0] < P[i][2]:
            ascending_R_H_after_rightmost_C.append((P[i][2], P[i][0]))

    result = float("inf")
    stk = []
    for i in xrange(len(C)):
        if not i:
            d = 0
        else:
            p = P[C[i-1]][0]
            while len(stk) > 1:
                a = stk[-1][1]
                b = min(a, stk[-2][1])
                if stk[-2][0] + 2*max(0, p-b) > stk[-1][0] + 2*max(0, p-a):
                    break
                stk[-2][1] = b
                stk.pop()
            d = stk[-1][0] + 2*max(0, p-stk[-1][1])
        stk.append([d, rightmost_harder_R[i]])
        p = P[C[-1]][0]
        if suffix_min_R[i] >= 0:
           result = min(result, d+max(0, p-suffix_min_R[i]))
        j = bisect_right(ascending_R_H_after_rightmost_C, (suffix_max_H[i], float("inf")))
        if j != len(ascending_R_H_after_rightmost_C):
            result = min(result, d+(ascending_R_H_after_rightmost_C[j][1]-p))
        if rightmost_harder_R[i] == -1:
            break
    return -1 if result == float("inf") else result + P[C[-1]][0]

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, seafood())