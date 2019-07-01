# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Round 1 - Connect the Dots
# https://www.facebook.com/hackercup/problem/2390352741015547/
#
# Time:  O(NlogN)
# Space: O(N)
#

from heapq import heappush, heappop

def convert(p):
    return (-p[0], -p[1])

def connect_the_dots():
    N, H, V = map(int, raw_input().strip().split())
    X1, X2, Ax, Bx, Cx, Dx = map(int, raw_input().strip().split())
    Y1, Y2, Ay, By, Cy, Dy = map(int, raw_input().strip().split())
    if N > H+V:
        return -1

    dots = [(X1, Y1), (X2, Y2)]
    for i in xrange(2, N):
        dots.append((((Ax * dots[i-2][0] + Bx * dots[i-1][0] + Cx) % Dx) + 1,
                     ((Ay * dots[i-2][1] + By * dots[i-1][1] + Cy) % Dy) + 1))
    dots.sort()

    suffix_max_Y = [0]*(N+1)
    for i in reversed(xrange(N)):
        suffix_max_Y[i] = max(suffix_max_Y[i+1], dots[i][1])

    result = float("inf")
    max_heap, min_heap = [], []
    heappush(max_heap, convert((0, -1)))
    for i in xrange(N+1):
        if i:
            if (dots[i-1][1], i) < convert(max_heap[0]):
                heappush(min_heap, convert(heappop(max_heap)))
                heappush(max_heap, convert((dots[i-1][1], i)))
            else:
                heappush(min_heap, (dots[i-1][1], i))
        f = N-i
        if V-f < 0:
            continue
        g = max(0, min(N-H, V)-f)
        while len(max_heap) > g+1:
            heappush(min_heap, convert(heappop(max_heap)))
        while len(max_heap) < g+1:
            heappush(max_heap, convert(heappop(min_heap)))
        result = min(result, \
                     (dots[i-1][0] if i else 0) + \
                     max(convert(max_heap[0])[0], suffix_max_Y[i]))
    return result

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, connect_the_dots())
