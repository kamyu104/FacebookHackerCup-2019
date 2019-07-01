# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Round 1 - Ladders and Snakes
# https://www.facebook.com/hackercup/problem/448364075989193/
#
# Time:  O(N^4)
# Space: O(N^2)
#

class Edge(object):
    def __init__(self, to, rev, c, f):
        self.to = to
        self.rev = rev
        self.c = c
        self.f = f

class Dinic(object):

    def __init__(self, n):
        self.lvl = [0]*n
        self.ptr = [0]*n
        self.q = [0]*n
        self.adj = [[] for _ in xrange(n)]
    
    def addEdge(self, a, b, c):
        self.adj[a].append(Edge(b, len(self.adj[b]), c, 0))
        self.adj[b].append(Edge(a, len(self.adj[a]) - 1, 0, 0))
    
    def dfs(self, v, t, f):
        if v == t or not f:
            return f
        while self.ptr[v] < len(self.adj[v]):
            e = self.adj[v][self.ptr[v]]
            if self.lvl[e.to] == self.lvl[v] + 1:
                p = self.dfs(e.to, t, min(f, e.c - e.f))
                if p:
                    e.f += p
                    self.adj[e.to][e.rev].f -= p
                    return p
            self.ptr[v] += 1
        return 0
    
    def calc(self, s, t):
        flow = 0
        self.q[0] = s
        for L in xrange(LIMIT+1):
            while True:
                self.lvl = [0]*(len(self.q))
                self.ptr = [0]*(len(self.q))
                qi, qe, self.lvl[s] = 0, 1, 1
                while qi < qe and not self.lvl[t]:
                    v = self.q[qi]
                    qi += 1
                    for i in xrange(len(self.adj[v])):
                        e = self.adj[v][i]
                        if not self.lvl[e.to] and (e.c - e.f) >> (LIMIT - L):
                            self.q[qe] = e.to
                            qe += 1
                            self.lvl[e.to] = self.lvl[v] + 1
                p = self.dfs(s, t, INF)
                while p:
                    flow += p
                    p = self.dfs(s, t, INF)
                if not self.lvl[t]:
                    break
        return flow

def ladders_and_snakes():
    N, H = map(int, raw_input().strip().split())
    X, A, B = [0]*N, [0]*N, [0]*N
    for i in xrange(N):
        X[i], A[i], B[i] = map(int, raw_input().strip().split())

    dinic = Dinic(N+2)
    for i in xrange(N):
        if A[i] == 0:
            dinic.addEdge(N, i, MAX_COST)
        if B[i] == H:
            dinic.addEdge(i, N+1 , MAX_COST)
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
LIMIT = INF.bit_length()
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, ladders_and_snakes())
