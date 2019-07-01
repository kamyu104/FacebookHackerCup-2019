# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Round 1 - Graphs as a Service
# https://www.facebook.com/hackercup/problem/862237970786911/
#
# Time:  O(N^3)
# Space: O(N^2)
#

def floydWarshall(graph): 
    dist = map(lambda i : map(lambda j : j , i), graph) 
    for k in xrange(len(dist[0])): 
        for i in xrange(len(dist)): 
            for j in xrange((len(dist[i]))): 
                dist[i][j] = min(dist[i][j], dist[i][k]+dist[k][j]) 
    return dist

def check_graph(graph):
    dist = floydWarshall(graph)
    for i in xrange(len(dist)):
        for j in xrange((len(dist[i]))):
            if graph[i][j] != float("inf") and \
               graph[i][j] != dist[i][j]:
               return False
    return True

def graphs_as_a_service():
    N, M = map(int, raw_input().strip().split())
    result = [str(M)]
    graph = [[float("inf") for _ in xrange(N)] for _ in xrange(N)]
    for _ in xrange(M):
        result.append(raw_input().strip())
        X, Y, Z = map(int, result[-1].split())
        graph[X-1][Y-1] = Z
        graph[Y-1][X-1] = Z

    if check_graph(graph):
        return "\n".join(result)
    return "Impossible"

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, graphs_as_a_service())
