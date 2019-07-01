# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Round 1 - Ladders and Snakes
# https://www.facebook.com/hackercup/problem/448364075989193/
#
# Time:  O(N^4)
# Space: O(N^2)
#

class Dinic(object):

    class Edge(object):
        def __init__(self, to, rev, c, f):
            self.to = to
            self.rev = rev
            self.c = c
            self.f = f

    def __init__(self, n, inf):
        self.adj = [[] for _ in xrange(n)]
        self.inf = inf
    
    def addEdge(self, a, b, c):
        self.adj[a].append(self.Edge(b, len(self.adj[b]), c, 0))
        self.adj[b].append(self.Edge(a, len(self.adj[a]) - 1, 0, 0))
    
    def calc(self, s, t):
        def dfs(adj, lvl, ptr, v, t, f):
            if v == t or not f:
                return f
            while ptr[v] < len(self.adj[v]):
                e = adj[v][ptr[v]]
                if lvl[e.to] == lvl[v] + 1:
                    p = dfs(adj, lvl, ptr, e.to, t, min(f, e.c - e.f))
                    if p:
                        e.f += p
                        adj[e.to][e.rev].f -= p
                        return p
                ptr[v] += 1
            return 0

        LIMIT = self.inf.bit_length()
        flow = 0
        adj = self.adj
        q = [0]*len(adj)
        q[0] = s
        for L in xrange(LIMIT+1):
            while True:
                lvl = [0]*(len(q))
                ptr = [0]*(len(q))
                qi, qe, lvl[s] = 0, 1, 1
                while qi < qe and not lvl[t]:
                    v = q[qi]
                    qi += 1
                    for i in xrange(len(adj[v])):
                        e = adj[v][i]
                        if not lvl[e.to] and (e.c - e.f) >> (LIMIT - L):
                            q[qe] = e.to
                            qe += 1
                            lvl[e.to] = lvl[v] + 1
                p = dfs(adj, lvl, ptr, s, t, INF)
                while p:
                    flow += p
                    p = dfs(adj, lvl, ptr, s, t, INF)
                if not lvl[t]:
                    break
        return flow

def ladders_and_snakes():
    N, H = map(int, raw_input().strip().split())
    X, A, B = [0]*N, [0]*N, [0]*N
    for i in xrange(N):
        X[i], A[i], B[i] = map(int, raw_input().strip().split())

    dinic = Dinic(N+2, INF)
    for i in xrange(N):
        if A[i] == 0:
            dinic.addEdge(N, i, MAX_COST)
        if B[i] == H:
            dinic.addEdge(i, N+1, MAX_COST)
        for j in xrange(N):
            if X[i] < X[j]:
                edges = []
                for k in xrange(N):
                    if X[i] <= X[k] <= X[j]:
                        edges.append((A[k], 1, k))
                        edges.append((B[k], 0, k))
                length = 0
                lookup = set()
                edges.sort()
                for k in xrange(len(edges)):
                    if edges[k][1]:  # start
                        lookup.add(edges[k][2])
                    else:  # end
                        lookup.remove(edges[k][2])
                    if (len(lookup)) == 2 and (i in lookup) and (j in lookup):
                        length += edges[k+1][0]-edges[k][0]
                if length:
                    dinic.addEdge(i, j, length)
                    dinic.addEdge(j, i, length)

    result = dinic.calc(N, N+1)
    return result if result < MAX_COST else -1

MAX_N = 50
MAX_H = 10**5
MAX_COST = 2*MAX_N*MAX_H
INF = 2*MAX_N*MAX_COST
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, ladders_and_snakes())
