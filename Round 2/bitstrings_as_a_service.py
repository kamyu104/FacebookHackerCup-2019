# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Round 2 - Bitstrings as a Service
# https://www.facebook.com/hackercup/problem/432000547357525/
#
# Time:  O(N * (M + N))
# Space: O(N * M)
#

from collections import Counter

class UnionFind(object):
    def __init__(self, n):
        self.set = range(n)

    def find_set(self, x):
        if self.set[x] != x:
            self.set[x] = self.find_set(self.set[x])  # path compression.
        return self.set[x]

    def union_set(self, x, y):
        x_root, y_root = map(self.find_set, (x, y))
        if x_root == y_root:
            return False
        self.set[min(x_root, y_root)] = max(x_root, y_root)
        return True
            
def bitstrings_as_a_service():
    N, M = map(int, raw_input().strip().split())
    union_find = UnionFind(N)
    for _ in xrange(M):
        i, j = map(int, raw_input().strip().split())
        i, j = i-1, j-1
        while i <= j:
            union_find.union_set(i, j)
            i += 1
            j -= 1

    comp = Counter(map(union_find.find_set, range(N)))
    dp = [[-1 for _ in xrange(N+1)] for _ in xrange(len(comp)+1)]  # dp[i][j] means the back link of 
                                                                   # the first i component with j nodes labeled 1,
                                                                   # -1 means impossible
    dp[0][0] = 0
    for i, count in enumerate(comp.itervalues()):
        for j in xrange(N):
            if dp[i][j] != -1:
                dp[i+1][j] = j  # the first i+1 component is possible with j nodes labeled 1
                dp[i+1][j+count] = j  # the first i+1 component is also possible with (j + (i+1)_th_comp_size) nodes labeled 1
    for i in xrange(N+1):  # find the min diff
        j = N//2+i
        if dp[-1][j] != -1:
            break
        j = N//2-i
        if dp[-1][j] != -1:
            break
    labels = {}
    for i, set_id in enumerate(reversed(comp.keys())):  # back tracing
        labels[set_id] = 1 if dp[-1-i][j] != j else 0
        j = dp[-1-i][j]

    result = []
    for i in xrange(N):
        result.append(labels[union_find.find_set(i)])
    return "".join(map(str, result))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, bitstrings_as_a_service())