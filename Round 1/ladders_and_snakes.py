# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Round 1 - Ladders and Snakes
# https://www.facebook.com/hackercup/problem/448364075989193/
#
# Time:  O(N^4)
# Space: O(N^2)
#

from collections import deque

# Time:  O(V^2 * E)
# Space: O(V + E)
class Dinic(object):

    def __init__(self, n):
        self.adj = [[] for _ in xrange(n)]
    
    def add_edge(self, i, j, c):
        self.adj[i].append([j, c, len(self.adj[j])])
        self.adj[j].append([i, 0, len(self.adj[i]) - 1])

    def max_flow(self, S, T):
        def bfs(S, T, adj, lev):  # levelize
            for i in xrange(len(adj)):
                lev[i] = -1
            lev[S] = 0
            q = deque([S])
            while q:
                v = q.popleft()
                for i in xrange(len(adj[v])):
                    to, cap, rev = adj[v][i]
                    if cap and lev[to] == -1:
                        lev[to] = lev[v] + 1
                        q.append(to)
            return lev[T] != -1

        def dfs(S, T, v, f, adj, lev, done):  # augment
            if v == T or not f:
                return f
            while done[v] < len(adj[v]):
                to, cap, rev = adj[v][done[v]]
                if lev[to] > lev[v]:
                    t = dfs(S, T, to, min(f, cap), adj, lev, done)
                    if t > 0:
                        adj[v][done[v]][1] -= t
                        adj[to][rev][1] += t
                        return t
                done[v] += 1
            return 0

        adj = self.adj
        V = len(self.adj)
        f = 0
        lev = [-1] * V
        while bfs(S, T, adj, lev):
            done = [0] * V
            t = float("inf")
            while t:
                t = dfs(S, T, S, float("inf"), adj, lev, done)
                f += t
        return f

def line_sweep(segments, i, j):
    points = []
    for k in xrange(i, j+1):
        points.append((segments[k][1], True, k))
        points.append((segments[k][2], False, k))
    points.sort()
    lookup = set()
    length = 0
    for k in xrange(len(points)):
        if points[k][1]:  # start
            lookup.add(points[k][2])
        else:  # end
            lookup.remove(points[k][2])
        if len(lookup) == 2 and i in lookup and j in lookup:
            length += points[k+1][0]-points[k][0]
    return length

def ladders_and_snakes():
    N, H = map(int, raw_input().strip().split())
    segments = []
    for i in xrange(N):
        segments.append(map(int, raw_input().strip().split()))

    dinic = Dinic(N+2)

    # Time: O(N^3 * logN)
    segments.sort()
    total = 0
    for i in xrange(N):
        for j in xrange(i+1, N):
            length = line_sweep(segments, i, j)  # Time: O(NlogN)
            if length:
                total += length
                dinic.add_edge(i, j, length)
                dinic.add_edge(j, i, length)
    assert(total <= (N-1)*H)
    for i in xrange(N):
        if segments[i][1] == 0:
            dinic.add_edge(N, i, total+1)
        if segments[i][2] == H:
            dinic.add_edge(i, N+1, total+1)

    result = dinic.max_flow(N, N+1)  # Time: O(N^4)
    return result if result <= total else -1

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, ladders_and_snakes())
