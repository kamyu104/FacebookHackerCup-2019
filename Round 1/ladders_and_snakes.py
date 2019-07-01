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
    inf = 10**9

    def __init__(self, n):
        self.adj = [[] for _ in xrange(n)]
    
    def addEdge(self, i, j, c):
        self.adj[i].append([j, c, len(self.adj[j])])
        self.adj[j].append([i, 0, len(self.adj[i]) - 1])

    def calc(self, S, T):
        def levelize(V, S, T, adj, lev):
            for i in xrange(V):
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

        def augment(S, T, v, f, lev, adj, done):
            if v == T or not f:
                return f
            while done[v] < len(adj[v]):
                to, cap, rev = adj[v][done[v]]
                if lev[to] > lev[v]:
                    t = augment(S, T, to, min(f, cap), lev, adj, done)
                    if t > 0:
                        adj[v][done[v]][1] -= t
                        adj[to][rev][1] += t
                        return t
                done[v] += 1
            return 0

        adj = self.adj
        V = len(self.adj)
        f, t = 0, 0
        lev = [-1] * V
        while levelize(V, S, T, adj, lev):
            done = [0] * V
            t = float("inf")
            while t:
                t = augment(S, T, S, float("inf"), lev, adj, done)
                f += t
        return f

def ladders_and_snakes():
    N, H = map(int, raw_input().strip().split())
    X, A, B = [0]*N, [0]*N, [0]*N
    for i in xrange(N):
        X[i], A[i], B[i] = map(int, raw_input().strip().split())

    dinic = Dinic(N+2)

    # Time: O(N^3 * logN)
    for i in xrange(N):
        if A[i] == 0:
            dinic.addEdge(N, i, Dinic.inf)
        if B[i] == H:
            dinic.addEdge(i, N+1, Dinic.inf)
        for j in xrange(N):
            if not (X[i] < X[j]):
                continue
            points = []
            for k in xrange(N):
                if X[i] <= X[k] <= X[j]:
                    points.append((A[k], 1, k))
                    points.append((B[k], 0, k))
            points.sort()
            lookup = set()
            length = 0
            for k in xrange(len(points)):
                if points[k][1]:  # start
                    lookup.add(points[k][2])
                else:  # end
                    lookup.remove(points[k][2])
                if (len(lookup)) == 2 and (i in lookup) and (j in lookup):
                    length += points[k+1][0]-points[k][0]
            if length:
                dinic.addEdge(i, j, length)
                dinic.addEdge(j, i, length)

    result = dinic.calc(N, N+1)  # Time:  O(N^4)
    return result if result < Dinic.inf else -1

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, ladders_and_snakes())
